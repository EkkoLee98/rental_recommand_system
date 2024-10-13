from .models import *
import json
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, time
from django.core.paginator import Paginator
from django.db.models import Q
import simplejson
from collections import Counter
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Map, Grid, Bar, Line, Pie, TreeMap
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode
from pyecharts.options.charts_options import MapItem
from django.db.models import Q, Count, Avg, Min, Max
from .recommend import collaborative_filtering_recommend


def to_dict(l, exclude=tuple()):
    # 将数据库模型 变为 字典数据 的工具类函数
    def transform(v):
        if isinstance(v, datetime):
            return v.strftime("%Y-%m-%d %H:%M:%S")
        return v

    def _todict(obj):
        j = {
            k: transform(v)
            for k, v in obj.__dict__.items()
            if not k.startswith("_") and k not in exclude
        }
        return j

    return [_todict(i) for i in l]


def unique_fields(request):
    body = request.json
    field = body.get("field")
    data = [i[0] for i in Rental.objects.values_list(field).distinct()]
    return JsonResponse(data, safe=False)


def get_list(request):
    # 列表
    body = request.json
    pagesize = body.get("pagesize", 10)
    page = body.get("page", 1)
    orderby = body.get("orderby", "-id")
    notin = ["pagesize", "page", "total", "orderby"]
    query = {
        k: v for k, v in body.items() if k not in notin and (v != "" and v is not None)
    }
    q = Q(**query)
    objs = Rental.objects.filter(q).order_by(orderby)
    paginator = Paginator(objs, pagesize)
    pg = paginator.page(page)
    result = to_dict(pg.object_list)
    return JsonResponse(
        {
            "total": paginator.count,
            "result": result,
        }
    )


def get_notify(request):
    notifyList = Notify.objects.all()
    # res = []
    # print(notifyList)
    # for i in notifyList:
    #     res.append(to_dict(i))

    if notifyList:
        return JsonResponse({"list": to_dict(notifyList)}, safe=False)
    else:
        return JsonResponse([])


def get_resever_by_id(request):
    user_id = request.user.id
    result = Reserve.objects.filter(userId=user_id)
    return JsonResponse(to_dict(result), safe=False)


def save_reserve(request):
    user_id = request.user.id
    data = dict(request.json)
    data["userId"] = user_id
    if Reserve.objects.filter(title=data["title"], userId=user_id):
        return JsonResponse({'success': False, 'message': '您已预约过此房源！'})
    else:
        Reserve.objects.create(**data)
        return JsonResponse({'success': True, 'message': '预约成功！'})


def get_detail(request):
    # 详情
    body = request.json
    id = body.get("id")
    o = Rental.objects.get(pk=id)
    his = History.objects.filter(
        userId=request.user.id).order_by("-createTime").first()
    if not (his and his.rentalId == o.id):
        History(userId=request.user.id, rentalId=o.id).save()
    return JsonResponse(to_dict([o])[0])


def history_recommand(request):
    topK = 5
    try:
        rentals = collaborative_filtering_recommend(request.user.id, topK)
    except:
        rentalIds = (
            History.objects.filter(userId=request.user.id)
            .values_list("rentalId")
            .distinct()
        )
        rentals = []
        # 根据历史查看记录推荐
        if rentalIds:
            rentalIds = [i[0] for i in rentalIds]
            location = [
                i[0]
                for i in Rental.objects.filter(id__in=rentalIds).values_list("location")
            ]
            locations = ["-".join(i.split("-")[:2]) for i in location]
            most_common_cates = list(
                dict(Counter(locations).most_common(2)).keys())
            q = Q()
            for i in most_common_cates:
                q |= Q(location__icontains=i)
            rentals = Rental.objects.filter(q).order_by("?")[:topK]
        # 没有记录则随机推荐
        else:
            rentals = Rental.objects.order_by("?")[:topK]
    return JsonResponse(to_dict(rentals), safe=False)


def type_pie(request):
    data = {
        i["type"]: i["count"]
        for i in Rental.objects.values("type").annotate(count=Count("id"))
        if "租" in i["type"]
    }
    # 用饼图展示数据
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add(
            "",
            list(data.items()),
            label_opts=opts.LabelOpts(is_show=False),
            radius=["40%", "75%"],
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="租房类型统计", pos_left="40%"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_right="80%", orient="vertical"
            ),
        )
    )
    # 返回数据
    return HttpResponse(c.dump_options(), content_type="application/json")


def orientation_map(request):
    data = [
        {"name": i["orientation"], "value": i["count"]}
        for i in Rental.objects.values("orientation").annotate(count=Count("id"))
    ]

    # 用饼图展示数据
    c = (
        TreeMap(init_opts=opts.InitOpts(width="1280px", height="720px"))
        .add(
            series_name="option",
            data=data,
            visual_min=300,
            leaf_depth=1,
            # 标签居中为 position = "inside"
            label_opts=opts.LabelOpts(position="inside"),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="房屋朝向分析", pos_left="leafDepth"),
        )
    )
    # 返回数据
    return HttpResponse(c.dump_options(), content_type="application/json")


def level_bar(request):
    data = {
        i["level"]: i["count"]
        for i in Rental.objects.values("level").annotate(count=Count("id"))
        if i["level"]
    }

    # 用柱状图展示统计数据
    c = (
        Bar()
        .add_xaxis([i[0] for i in data.items()])
        .add_yaxis(
            "",
            [i[1] for i in data.items()],
            label_opts=opts.LabelOpts(is_show=False),
            bar_max_width=50,
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="楼层类型分析"),
            # datazoom_opts=opts.DataZoomOpts(orient="vertical"),
            yaxis_opts=opts.AxisOpts(
                type_="category",
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True, type_="shadow"),
            ),
        )
    )
    # 返回数据
    return HttpResponse(c.dump_options(), content_type="application/json")


def price_bar(request):
    data = {}
    data["1000以下"] = Rental.objects.filter(price__lte=1000).count()
    data["1000-2000"] = Rental.objects.filter(
        price__gte=1000, price__lte=2000).count()
    data["2000-3000"] = Rental.objects.filter(
        price__gte=2000, price__lte=3000).count()
    data["3000-4000"] = Rental.objects.filter(
        price__gte=3000, price__lte=4000).count()
    data["4000-5000"] = Rental.objects.filter(
        price__gte=4000, price__lte=5000).count()
    data["5000-6000"] = Rental.objects.filter(
        price__gte=5000, price__lte=6000).count()
    data["6000-7000"] = Rental.objects.filter(
        price__gte=6000, price__lte=7000).count()
    data["7000以上"] = Rental.objects.filter(price__gte=7000).count()

    # 用柱状图展示统计数据
    c = (
        Bar()
        .add_xaxis([i[0] for i in data.items()])
        .add_yaxis(
            "",
            [i[1] for i in data.items()],
            label_opts=opts.LabelOpts(is_show=False),
            bar_max_width=50,
            color="#5689ff",
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="房源价格分布"),
            # datazoom_opts=opts.DataZoomOpts(orient="vertical"),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True, type_="shadow"),
            ),
        )
    )
    # 返回数据
    return HttpResponse(c.dump_options(), content_type="application/json")


def province_map(request):
    data = {
        i["province"] + "省": i["count"]
        for i in Rental.objects.values("province").annotate(count=Count("id"))
    }
    dd = [MapItem(name=i[0], value=i[1]) for i in data.items()]
    m = (
        Map()
        .add("房源数量", dd, "china", is_roam=False, is_map_symbol_show=False)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="房源数量分布",
            ),
            visualmap_opts=opts.VisualMapOpts(
                max_=1000,
                is_piecewise=False,
            ),
            legend_opts=opts.LegendOpts(
                is_show=False, textstyle_opts=opts.TextStyleOpts(color="white")
            ),
        )
    )
    return HttpResponse(m.dump_options(), content_type="aplication/text")
