# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 13:03
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
                ('name', models.CharField(max_length=100, verbose_name='Название города')),
            ],
            options={
                'verbose_name_plural': 'Города',
                'ordering': ('name',),
                'verbose_name': 'Город',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'Заказы',
                'verbose_name': 'Заказ',
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
                'ordering': ('city', 'shop_name'),
                'verbose_name': 'Магазин',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='entry',
            field=models.ManyToManyField(to='orders.Shop'),
        ),
        migrations.AlterUniqueTogether(
            name='shop',
            unique_together=set([('city', 'shop_name')]),
        ),
    ]
