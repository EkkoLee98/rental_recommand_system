# Generated by Django 3.2.12 on 2022-09-21 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.TextField(verbose_name='封面图')),
                ('type', models.CharField(max_length=255, verbose_name='租房类型')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('url', models.TextField(verbose_name='原链接')),
                ('location', models.CharField(max_length=255, verbose_name='位置')),
                ('area_text', models.CharField(max_length=255, verbose_name='面积')),
                ('area', models.FloatField(verbose_name='面积')),
                ('orientation', models.CharField(max_length=255, verbose_name='朝向')),
                ('structure', models.CharField(max_length=255, verbose_name='构造')),
                ('price_text', models.CharField(max_length=255, verbose_name='价格')),
                ('price', models.FloatField(verbose_name='价格')),
                ('tags', models.TextField(verbose_name='标签,逗号分隔')),
                ('level', models.CharField(max_length=255, null=True, verbose_name='楼层类别')),
                ('floor', models.IntegerField(null=True, verbose_name='楼层')),
                ('province', models.CharField(max_length=255, verbose_name='省份')),
                ('city', models.CharField(max_length=255, verbose_name='城市')),
                ('imgs', models.TextField(verbose_name='图片,逗号分隔')),
                ('detail', models.TextField(verbose_name='正文详情')),
            ],
            options={
                'verbose_name': '租房数据',
                'verbose_name_plural': '租房数据',
                'db_table': 'rental',
            },
        ),
    ]