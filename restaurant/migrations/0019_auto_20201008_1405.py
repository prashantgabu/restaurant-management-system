# Generated by Django 3.0.6 on 2020-10-08 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0018_order_totalamount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='totalAmount',
            field=models.IntegerField(default=0),
        ),
    ]