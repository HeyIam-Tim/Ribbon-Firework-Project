from django.contrib import admin
from .models import Ribbon, OrderInfo, OrderItem


class RibbonAdmin(admin.ModelAdmin):
    list_display = ('ribbon_name', 'price')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    exclude = ['image']
    extra = 1

class OrderInfoAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': [
        'customer_name',
        'phone',
        'city',
        'street',
        'building',
        'apartment',
        'region',
        'zip_code',
        'order_total',
        'status']}),]
    inlines = [OrderItemInline]
    list_display = (
        'customer_name',
        'phone',
        'created',
        'order_total',
        'status'
        )


admin.site.register(Ribbon, RibbonAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)