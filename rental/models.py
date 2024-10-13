from django.db import models

[
    "cover",
    "type",
    "title",
    "url",
    "location",
    "area_text",
    "area",
    "orientation",
    "structure",
    "price_text",
    "tags",
    "price",
    "level",
    "floor",
    "province",
    "city",
    "imgs",
    "detail",
]


class History(models.Model):
    userId = models.IntegerField("用户id")
    rentalId = models.IntegerField("房源id")
    createTime = models.DateTimeField("浏览时间", auto_now_add=True)

    class Meta:
        db_table = "view_history"
        verbose_name = "房源浏览记录"
        verbose_name_plural = verbose_name


class Notify(models.Model):
    title = models.TextField("标题")
    content = models.TextField("内容")
    createTime = models.DateTimeField("浏览时间", auto_now_add=True)

    class Meta:
        db_table = "notify"
        verbose_name = "公告管理"
        verbose_name_plural = verbose_name


class Reserve(models.Model):
    userId = models.IntegerField("用户id", null=True)
    title = models.TextField("标题")
    price_text = models.CharField("租金", max_length=255)
    structure = models.CharField("户型", max_length=255)
    tags = models.TextField("标签,逗号分隔")
    area_text = models.CharField("面积", max_length=255)
    city = models.CharField("所在城市", max_length=255)
    location = models.CharField("位置", max_length=255)
    floor = models.IntegerField("楼层", null=True)

    class Meta:
        db_table = "reserve"
        verbose_name = "预定记录"
        verbose_name_plural = verbose_name


class Rental(models.Model):
    cover = models.TextField("封面图")
    type = models.CharField("租房类型", max_length=255)
    title = models.CharField("标题", max_length=255)
    oid = models.CharField("原id", max_length=100, unique=True)
    url = models.TextField("原链接")
    location = models.CharField("位置", max_length=255)
    area_text = models.CharField("面积", max_length=255)
    area = models.FloatField("面积")
    orientation = models.CharField("朝向", max_length=255)
    structure = models.CharField("构造", max_length=255)
    price_text = models.CharField("价格", max_length=255)
    price = models.FloatField("价格")
    tags = models.TextField("标签,逗号分隔")
    level = models.CharField("楼层类别", max_length=255, null=True)
    floor = models.IntegerField("楼层", null=True)
    province = models.CharField("省份", max_length=255)
    city = models.CharField("城市", max_length=255)
    imgs = models.TextField("图片,逗号分隔")
    detail = models.TextField("正文详情")

    class Meta:
        db_table = "rental"
        verbose_name = "租房数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
