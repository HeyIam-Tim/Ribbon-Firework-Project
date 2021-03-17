# pylint: disable=E1101
from django.db import models
from django.contrib.auth.models import User


class OrderInfo(models.Model):
    STATUS = (
    ('Новый', 'Новый'),
    ('Обработан', 'Обработан'),
    ('Доставлен', 'Доставлен'),
    )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    building = models.CharField(max_length=200, null=True, blank=True)
    apartment = models.CharField(max_length=200, null=True, blank=True)
    region = models.TextField(max_length=400, null=True, blank=True)
    zip_code = models.IntegerField(default=0, null=True, blank=True)
    order_total = models.FloatField(default=0)
    status = models.CharField(max_length=200, default="Новый", null=True, blank=True, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

    @property
    def get_order_total(self):
        item_totals = self.orderitem_set.all()
        total = sum([item.get_total for item in item_totals])
        return total


class OrderItem(models.Model):
    order_info = models.ForeignKey(OrderInfo, null=True, blank=True, on_delete=models.CASCADE)
    ribbon_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField()
    quantity = models.IntegerField(default=0, null=True, blank=True)
    item_total = models.FloatField(default=0)


    def __str__(self):
        return self.ribbon_name

    @property
    def get_total(self):
        total = self.price * self.quantity
        return total



class Ribbon(models.Model):
    ribbon_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField()

    def __str__(self):
        return self.ribbon_name
