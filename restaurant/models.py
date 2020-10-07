from django.db import models
import datetime


class Owner(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=15)

    class Meta:
        db_table = 'owner'


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    contact_number = models.CharField(max_length=13)
    cuisine = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="opened")

    class Meta:
        db_table = 'restaurant'


class Food_item(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    counter = models.IntegerField(default=0)
    # cuisine= models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        db_table = 'food_item'


class Order(models.Model):
    transaction_id = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    createdAt = models.DateTimeField(default=datetime.datetime.now)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        db_table = "order"


class OrderDetails(models.Model):
    quantity = models.IntegerField(default=1)
    item_price_total = models.CharField(max_length=100)
    food_item = models.ForeignKey(Food_item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    class Meta:
        db_table = 'order_details'