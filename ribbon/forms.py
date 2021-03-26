from django.forms import ModelForm
from django import forms
from .models import Ribbon, OrderItem


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['ribbon_name', 'image', 'price',]