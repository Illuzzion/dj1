# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 08:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='orderentry',
            unique_together=set([('order', 'invoice_number')]),
        ),
    ]
