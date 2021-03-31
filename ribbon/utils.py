# pylint: disable=E1101
from django.contrib import messages
from .models import OrderItem


def success_message(request, id_order):
    messages.success(request, f"Спасибо! Ваш заказ номер '{id_order}' успешно оформлен!")

