from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib.auth import authenticate, login
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Count
from django.contrib import messages
from . models import *
import string
import random
import json
import calendar


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

    # order= Order.objects.all().values_list('createdAt__month').annotate(Sum('totalAmount')).order_by('createdAt__month')
    order = Order.objects.values('createdAt__month').order_by(
        'createdAt__month').annotate(sum=Sum('totalAmount'))
    month_lists = []
    total_amount_monthly = []
    print('order', order)
    for item in order:
        month_lists.append(calendar.month_name[item['createdAt__month']])
        total_amount_monthly.append(item['sum'])

    fooditem_list = Food_item.objects.all().order_by('-counter')[:10]
    # for item in fooditem_list:
    #     print(item.name)

    total_customers_served_today = Order.objects.filter(
        createdAt__date=datetime.date.today()).count()

    earnings_till_date = Order.objects.aggregate(Sum('totalAmount'))

    earnings_today = Order.objects.filter(
        createdAt__date=datetime.date.today()).aggregate(Sum('totalAmount'))

    total_customers_served = Order.objects.all().count()
    month_list=json.dumps(month_lists)
    total_amount_monthly2=json.dumps(total_amount_monthly)
    context = {'total_customers_served': total_customers_served,
               'total_customers_served_today': total_customers_served_today,
               'earnings_till_date': earnings_till_date['totalAmount__sum'],
               "earnings_today": earnings_today['totalAmount__sum'],
               'fooditem_list': fooditem_list,
               "month_list": month_list,
               "total_amount_monthly": total_amount_monthly2}

    return render(request, 'restaurant/dashboard.html', context)


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
    order_list = Order.objects.filter(createdAt__date=datetime.date.today())
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
    order.totalAmount = total_amount
    order.invoiceGenerated = 1
    order.save()
    context = {'invoice_details': 'invoice_details', 'order': order,
               'total_amount': total_amount, 'order_details': orderdetails}
    return render(request, 'restaurant/invoice.html', context)


def logout(request):
    try:
        del request.session['transaction_id']
        del request.session['owner_id']

    except KeyError:
        pass
    return redirect('login')
