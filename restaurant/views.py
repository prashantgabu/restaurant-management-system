from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib.auth import authenticate, login
from django.contrib import messages
from . models import *
import string
import random


def login(request):
    try:
        if request.method == "POST":
            email1 = request.POST.get('email')
            password = request.POST.get('password')
            owner = Owner.objects.get(email=email1)
            check_auth = owner.email == email1 and owner.password == password
            request.session['owner_id'] = owner.id
            if (check_auth):
                return redirect('dashboard')
            else:
                messages.error(request, 'Password incorrect.')
                return redirect('login')
        else:
            return render(request, 'restaurant/login.html')
    except Owner.DoesNotExist:
        restaurant = None
        return render(request, 'restuarant/login.html')


def dashboard(request):
    return render(request, 'restaurant/dashboard.html')


def addRestaurant(request):
    # if not request.session.get('owner_id'):
    #     return redirect('login')

    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        cuisine = request.POST.get('cuisine')
        restaurant = Restaurant(name=name, contact_number=contact_number,
                                address=address, status="opened", cuisine=cuisine)
        restaurant.save()
        return redirect('viewRestaurant')
    else:
        return render(request, "restaurant/addRestaurant.html")


def viewRestaurant(request):
    restaurant_list = Restaurant.objects.all()
    context = {'restaurant_list': restaurant_list}
    return render(request, "restaurant/viewRestaurant.html", context)


def editRestaurant(request, id):
    restaurant_list = Restaurant.objects.get(id=id)
    context = {'restaurant_list': restaurant_list}
    return render(request, "restaurant/editRestaurant.html", context)


def updateRestaurant(request, id):
    restaurant = Restaurant.objects.get(id=id)
    # if not request.session.get('owner_id'):
    #     return redirect('login')

    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        cuisine = request.POST.get('cuisine')
        status = request.POST.get('status')

        restaurant.name = name
        restaurant.contact_number = contact_number
        restaurant.address = address
        restaurant.cuisine = cuisine
        restaurant.status = status
        restaurant.save()

        return redirect('viewRestaurant')


def deleteRestaurant(request, id):
    restaurant = Restaurant.objects.get(id=id)
    restaurant.delete()
    return redirect('viewRestaurant')


def addFooditem(request):
    # if not request.session.get('owner_id'):
    #     return redirect('login')

    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        restaurant_id = request.POST.get('restaurant')
        restaurant = Restaurant.objects.get(id=int(restaurant_id))
        fooditem = Food_item(name=name, price=price, restaurant=restaurant)
        fooditem.save()
        return redirect('viewFooditem')
    else:
        restaurant_list = Restaurant.objects.all()
        context = {'restaurant_list': restaurant_list}
        return render(request, "restaurant/addFooditem.html", context)


def viewFooditem(request):
    fooditem_list = Food_item.objects.all()
    context = {'fooditem_list': fooditem_list}
    return render(request, "restaurant/viewFooditem.html", context)


def viewFooditemByRestaurant(request, id):
    fooditem_list = Food_item.objects.filter(restaurant=id)
    context = {'fooditem_list': fooditem_list}
    return render(request, "restaurant/viewFooditem.html", context)


def editFooditem(request, id):
    restaurant_list = Restaurant.objects.all()
    fooditem_list = Food_item.objects.get(id=id)
    context = {'fooditem_list': fooditem_list,
               'restaurant_list': restaurant_list}
    return render(request, "restaurant/editFooditem.html", context)


def updateFooditem(request, id):
    fooditem = Food_item.objects.get(id=id)
    # if not request.session.get('owner_id'):
    #     return redirect('login')

    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        restaurant_id = request.POST.get('restaurant')
        restaurant = Restaurant.objects.get(id=int(restaurant_id))
        fooditem.name = name
        fooditem.price = price
        fooditem.restaurant = restaurant
        fooditem.save()
        return redirect('viewFooditem')


def deleteFooditem(request, id):
    fooditem = Food_item.objects.get(id=id)
    fooditem.delete()
    return redirect('viewFooditem')


def selectRestaurant(request):
    restaurant_list = Restaurant.objects.all()
    context = {'restaurant_list': restaurant_list}
    return render(request, "restaurant/selectRestaurant.html", context)


def selectFooditem(request, id):
    fooditem_list = Food_item.objects.filter(restaurant=id)
    context = {'fooditem_list': fooditem_list}
    return render(request, "restaurant/selectFooditem.html", context)


def addCustomer(request):
    # if not request.session.get('owner_id'):
    #     return redirect('login')
    transaction_id = ''.join([random.choice(string.ascii_letters
                                            + string.digits) for n in range(10)])
    print(transaction_id)
    if request.method == "POST":
        customer_name = request.POST.get('name')
        restaurant_id = request.POST.get('restaurant')
        restaurant = Restaurant.objects.get(id=int(restaurant_id))
        request.session['transaction_id'] = transaction_id
        order = Order(transaction_id=transaction_id,
                      customer_name=customer_name, restaurant=restaurant)
        order.save()
        return redirect('viewCustomer')
    else:
        restaurant_list = Restaurant.objects.all()
        context = {'restaurant_list': restaurant_list}
        return render(request, "restaurant/addCustomer.html", context)


def viewCustomer(request):
    order_list = Order.objects.all()
    context = {'order_list': order_list}
    return render(request, "restaurant/viewCustomer.html", context)


def viewFoodItemToOrder(request, id):

    order = Order.objects.get(id=id)
    restaurant_id = order.restaurant.id

    fooditem_list = Food_item.objects.filter(restaurant=restaurant_id)
    order_id = order.id
    context = {'fooditem_list': fooditem_list, 'order_id': order_id}
    return render(request, "restaurant/viewFoodItemToOrder.html", context)


def addFoodItemToOrder(request, id):
    transaction_id = request.session['transaction_id']
    quantity = request.POST.get('quantity')

    food_item = Food_item.objects.get(id=id)
    price = food_item.price

    item_price_total = int(price)*int(quantity)
    print("::::::::::::::::::transaction_id", transaction_id)
    order = Order.objects.get(
        transaction_id=transaction_id)
    orderDetails = OrderDetails(
        quantity=quantity, food_item=food_item, item_price_total=item_price_total, order=order)
    orderDetails.save()
    return redirect('viewFoodItemToOrder', id=order.id)


def generateInvoice(request):
    transaction_id = request.session['transaction_id']
    order = Order.objects.get(
        transaction_id=transaction_id)
    orderdetails = OrderDetails.objects.filter(order=order)
    food_items = []
    total_amount = 0
    for item in orderdetails:
        total_amount += int(item.item_price_total)
    context = {'invoice_details': 'invoice_details', 'order': order,
               'total_amount': total_amount, 'order_details': orderdetails}
    return render(request, 'restaurant/invoice.html', context)
