from django.apps import AppConfig


class RentalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rental"
    verbose_name: str = "房源数据管理"
