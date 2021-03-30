from django.forms import ModelForm
from django import forms
from .models import Ribbon, OrderItem, OrderInfo


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['ribbon_name', 'image', 'price',]


class OrderInfoForm(ModelForm):
    class Meta:
        model = OrderInfo
        fields = [
            'customer_name',
            'phone',
            'city',
            'street',
            'building',
            'apartment',
            'region',
            'zip_code',
        ]