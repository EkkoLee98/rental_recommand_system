from django.contrib import admin
from .models import *


class NotifyAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "content",
        "createTime",
    ]
    search_fields = [
        "title",
    ]


class ReserveAdmin(admin.ModelAdmin):
    list_display = [
        "userId",
        "title",
        "price_text",
        "structure",
        "tags",
        "area_text",
        "city",
        "floor",
    ]
    search_fields = [
        "userId",
        "title",
        "price_text",
        "area_text",
    ]


class Admin(admin.ModelAdmin):
    list_display = [
        # "cover",
        "type",
        "title",
        # "url",
        "location",
        "area_text",
        # "area",
        "orientation",
        "structure",
        "price_text",
        "tags",
        # "price",
        "level",
        "floor",
        "province",
        "city",
        # "imgs",
        # "detail",
    ]
    list_filter = [
        # "cover",
        "type",
        "orientation",
        "structure",
        "level",
        "province",
        "city",
    ]
    list_search = [
        "title",
    ]
    list_per_page = 10
    list_max_show_all = 200


admin.site.register(Rental, Admin)
admin.site.register(Notify, NotifyAdmin)
admin.site.register(Reserve, ReserveAdmin)
