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
    customer_name = models.CharField(max_length=200, null=True, blank=False)
    phone = models.CharField(max_length=200, null=True, blank=False)
    city = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    building = models.CharField(max_length=200, null=True, blank=True)
    apartment = models.CharField(max_length=200, null=True, blank=True)
    region = models.TextField(max_length=400, null=True, blank=True)
    zip_code = models.IntegerField(default=0, null=True, blank=True)
    order_total = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    status = models.CharField(max_length=200, default="Новый", null=True, blank=True, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created)
    # def __str__(self):
    #     return self.customer_name
    # def __str__(self):
    #     return self.user.username

    @property
    def get_order_total(self):
        item_totals = self.orderitem_set.all()
        total = sum([item.get_total for item in item_totals])
        return total

    @property
    def get_quantity_total(self): 
        quantity_totals = self.orderitem_set.all()
        quantity = sum([quantity.quantity for quantity in quantity_totals])
        return quantity

    @property
    def date_formated(self):
        d_formated = str(self.created.date())
        return d_formated


class PreOrder(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.user.username
    def __str__(self):
        return str(self.created)

    @property
    def get_quantity_total(self): 
        quantity_totals = self.orderitem_set.all()
        quantity = sum([quantity.quantity for quantity in quantity_totals])
        return quantity


class OrderItem(models.Model):
    order_info = models.ForeignKey(OrderInfo, null=True, blank=True, on_delete=models.CASCADE)
    preorder = models.ForeignKey(PreOrder, null=True, blank=True, on_delete=models.CASCADE)
    ribbon_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    item_total = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return self.ribbon_name

    @property
    def get_total(self):
        total = int(self.price) * int(self.quantity)
        return total



class Ribbon(models.Model):
    ribbon_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.ribbon_name
