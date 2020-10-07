# Generated by Django 3.0.6 on 2020-10-07 12:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_remove_food_item_cuisine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=100)),
                ('customer_name', models.CharField(max_length=100)),
                ('createdAt', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('item_price_total', models.CharField(max_length=10)),
                ('food_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Food_item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Order')),
            ],
            options={
                'db_table': 'order_details',
            },
        ),
    ]
