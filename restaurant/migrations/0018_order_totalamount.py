# Generated by Django 3.0.6 on 2020-10-08 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0017_order_invoicegenerated'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='totalAmount',
            field=models.CharField(default=0, max_length=50),
        ),
    ]
