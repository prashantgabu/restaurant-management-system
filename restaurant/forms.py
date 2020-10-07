from .models import Restaurant
from django import forms

class Restaurant_form(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = "__all__"
