from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('addRestaurant', views.addRestaurant, name="addRestaurant"),
    path('viewRestaurant', views.viewRestaurant, name="viewRestaurant"),
    path('editRestaurant/<int:id>', views.editRestaurant, name="editRestaurant"),
    path('updateRestaurant/<int:id>', views.updateRestaurant, name="updateRestaurant"),
    path('deleteRestaurant/<int:id>', views.deleteRestaurant, name="deleteRestaurant"),
    path('addFooditem', views.addFooditem, name="addFooditem"),
    path('viewFooditem', views.viewFooditem, name="viewFooditem"),
    path('viewFooditem/<int:id>', views.viewFooditemByRestaurant, name="viewFooditemByRestaurant"),
    path('editFooditem/<int:id>', views.editFooditem, name="editFooditem"),
    path('updateFooditem/<int:id>', views.updateFooditem, name="updateFooditem"),
    path('deleteFooditem/<int:id>', views.deleteFooditem, name="deleteFooditem"),
    path('selectRestaurant', views.selectRestaurant, name="selectRestaurant"),
    path('selectFooditem/<int:id>', views.selectFooditem, name="selectFooditem"),
    path('addCustomer', views.addCustomer, name="addCustomer"),
    path('viewCustomer', views.viewCustomer, name="viewCustomer"),
    path('viewFoodItemToOrder/<int:id>', views.viewFoodItemToOrder, name="viewFoodItemToOrder"),
    path('addFoodItemToOrder/<int:id>', views.addFoodItemToOrder, name="addFoodItemToOrder"),
    path('generateInvoice', views.generateInvoice, name="generateInvoice"),


]
