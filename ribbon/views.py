from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Ribbon


class RibbonList(ListView):
    model = Ribbon
    template_name = 'ribbon/index.html'
    context_object_name = 'ribbons'