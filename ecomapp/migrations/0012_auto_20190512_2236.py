# Generated by Django 2.2 on 2019-05-12 19:36

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0011_auto_20190512_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ForeignKey(default=datetime.datetime(2019, 5, 12, 19, 36, 3, 215046, tzinfo=utc), on_delete=django.db.models.deletion.CASCADE, to='ecomapp.Cart'),
        ),
    ]