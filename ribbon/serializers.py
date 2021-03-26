from rest_framework import serializers
from .models import Ribbon, OrderItem


class RibbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ribbon
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['ribbon_name', 'image', 'price',]