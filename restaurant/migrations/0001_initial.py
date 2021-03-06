# Generated by Django 3.0.6 on 2020-10-07 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'owner',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(max_length=200)),
                ('contact_number', models.CharField(max_length=13)),
                ('cuisine', models.CharField(max_length=100)),
                ('status', models.CharField(default='opened', max_length=100)),
                ('logo', models.ImageField(default='None', upload_to='restaurant')),
            ],
            options={
                'db_table': 'restaurant',
            },
        ),
        migrations.CreateModel(
            name='Food_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('counter', models.IntegerField()),
                ('cuisine', models.CharField(max_length=50)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Restaurant')),
            ],
            options={
                'db_table': 'food_item',
            },
        ),
    ]
