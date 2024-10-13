import os
import django
from django.db import connection
import pandas as pd
import numpy as np
from datetime import date, timedelta
from collections import Counter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rental_recommand_system.settings")
django.setup()
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from rental.models import *

# 1. 首先同时选择用户表(auth_user)与房源表(rantal)，这样将会得到一个笛卡尔积(意思是1,2与3,4做笛卡尔积，会得到1-3、1-4、2-3、2-4)
# 即 SELECT au.id user_id, td.id rental_id FROM auth_user au, rantal td;

# 2. 然后第一步的结果作为子查询与房源浏览细节表(view_history)做一个左外连接
# (( SELECT au.id user_id, td.id rental_id FROM auth_user au, rantal td ) ud
# 		LEFT JOIN view_history rc ON ud.rental_id = rc.rentalId
# 		AND ud.user_id = rc.userId )

# 3. 再将第二步结果进行分组，这里是为了计算出某用户对某房源的浏览总数，即最终得到如下SQL语句
# 结果是所有用户对所有房源的浏览数，作为协同过滤算法计算的矩阵数据

sql = """
	SELECT
		ud.user_id AS user_id,
		ud.rental_id AS rental_id,
		count(rc.id) as rate
	FROM
		(( SELECT au.id user_id, td.id rental_id FROM auth_user au, rental td ) ud
		LEFT JOIN view_history rc ON ud.rental_id = rc.rentalId 
		AND ud.user_id = rc.userId )
	GROUP BY
		ud.user_id,
		ud.rental_id
	"""

# https://zhuanlan.zhihu.com/p/80069337
def collaborative_filtering(uid, topK=10, minSim=0.45):
    """
    基于用户的协同过滤推荐算法
        参数
            topK 取多少个推荐物品
            minSim 用户最小相似度>=0.45
        返回
            与目标用户最相似的用户喜欢的标的物的id(列表)
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    raw = cursor.fetchall()
    columns = ("user_id", "rental_id", "rate")
    df = pd.DataFrame(raw, columns=columns)
    pi = pd.pivot(df, index="rental_id", columns="user_id")
    pi.columns = pi.columns.droplevel(0)
    pi = pi.astype(float)
    # pi = pd.DataFrame(np.random.random(size=(100, 10)))
    # pi = pd.DataFrame([[-1, 1], [-1, 1]])
    # pi = pd.DataFrame(np.array([[1, 2, 3, 4], [5, 6, 7, 8]]).T)

    # user_id        1  2  3  4
    # rental_id
    # 1              0  0  0  0
    # 2              0  0  0  0
    # 3              0  0  0  0
    # 4              0  0  0  0
    # 5              0  0  0  1

    # 得到每个列向量的模(长度)
    norm = (pi * pi).sum(axis=0).apply(np.sqrt)
    # 目标用户的列向量
    umat = pi[uid]
    # 其他所有用户的列向量
    oumat = pi[[i for i in pi.columns if i != uid]]
    # 目标用户的向量模
    unorm = norm[uid]
    # 其他所有用户的向量模
    ounorm = norm[[i for i in pi.columns if i != uid]]
    # 计算余弦相似度
    # 1. 计算目标用户与其他所有用户的向量积
    dotmat = oumat.apply(np.dot, args=(umat,))
    dotmat = dotmat.apply(float)
    # 2. 得到目标用户向量模与其他所有用户的向量模的乘积
    rantal = ounorm.apply(lambda x: x * unorm)
    # 3. 将向量积除以向量模的乘积，即得到两两向量的余弦值(相似度)，这里意思是得到了和目标用户最相似的一组用户
    sim_users = dotmat / rantal
    sim_users = sim_users.dropna()
    # 排除掉不符合最小相似度的用户，减少计算量
    if minSim is not None:
        sim_users = sim_users[sim_users >= minSim]
    # print(f"和目标用户id为{uid}最相似的用户", sim_users)
    # 得到所有相似用户对所有房源的评分与相似度乘积的和，然后按评分倒序排列，取其前N个，推荐给用户
    rantal_scores = (
        (pi[sim_users.index] * sim_users).sum(axis=1).sort_values(ascending=False)
    )
    rantal_scores = rantal_scores[:topK]
    # print(f"与目标用户id为{uid}最相似的用户喜欢的房源", rantal_scores[:topK])
    return rantal_scores[:topK].index.to_list()

    # 0.8-1.0 极强相关
    # 0.6-0.8 强相关
    # 0.4-0.6 中等程度相关
    # 0.2-0.4 弱相关
    # 0.0-0.2 极弱相关或无相关


def collaborative_filtering_recommend(uid, topK=10, minSim=0.45):
    """
    协同过滤推荐房源
    """
    rental_ids = collaborative_filtering(uid, topK * 2, minSim)
    # 打乱顺序，取topK
    rantales = list(Rental.objects.filter(id__in=rental_ids).order_by("?")[:topK])
    user = User.objects.get(pk=uid)
    rantal_names = ", ".join([f"{i.title}({i.id})" for i in rantales])
    # print(f"根据协同过滤算法结果给用户<{user.username}>推荐房源: {rantal_names}")
    return rantales


if __name__ == "__main__":
    collaborative_filtering(1)
    # collaborative_filtering_recommend(1)
