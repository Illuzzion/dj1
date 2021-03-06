# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 07:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название города')),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Города',
                'verbose_name': 'Город',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Создано')),
            ],
            options={
                'verbose_name_plural': 'Заказы',
                'verbose_name': 'Заказ',
            },
        ),
        migrations.CreateModel(
            name='OrderEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.PositiveSmallIntegerField(verbose_name='Номер накладной')),
                ('place', models.PositiveSmallIntegerField(default=1, verbose_name='Количество мест')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name_plural': 'Элементы заказа',
                'verbose_name': 'Элемент заказа',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=200, verbose_name='Название магазина')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.City', verbose_name='Название города')),
            ],
            options={
                'verbose_name_plural': 'Магазины',
                'verbose_name': 'Магазин',
                'ordering': ('city', 'shop_name'),
            },
        ),
        migrations.AddField(
            model_name='orderentry',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Shop', verbose_name='Магазин'),
        ),
        migrations.AlterUniqueTogether(
            name='shop',
            unique_together=set([('city', 'shop_name')]),
        ),
    ]
