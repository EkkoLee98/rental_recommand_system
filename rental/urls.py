from django.urls import path
from .views import *

urlpatterns = [
    path("rental/", get_list),  # 列表的路由地址
    path("rental/detail/", get_detail),  # 详情的路由地址
    path("rental/recommmand/", history_recommand),  # 详情的路由地址
    path("unique_fields/", unique_fields),
    path("rental/notify/get/", get_notify),
    path("rental/reserve/get/", get_resever_by_id),
    path("rental/reserve/", save_reserve),
    path("type_pie/", type_pie),
    path("orientation_map/", orientation_map),
    path("level_bar/", level_bar),
    path("province_map/", province_map),
    path("price_bar/", price_bar),
]
