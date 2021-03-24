# pylint: disable=E1101
from django.shortcuts import render, redirect
from django.contrib import messages

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView

from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Ribbon, OrderInfo, OrderItem
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from .serializers import RibbonSerializer

# class RibbonList(ListView):
#     model = Ribbon
#     template_name = 'ribbon/index.html'
#     context_object_name = 'ribbons'


class RibbonList(ListView):
    model = Ribbon
    template_name = 'ribbon/index.html'
    context_object_name = 'ribbons'


class RibbonListApi(APIView):
    def get(self, request):
        ribbons = Ribbon.objects.all()
        serializer = RibbonSerializer(ribbons, many=True)
        return Response(serializer.data)


class OrderInfoCreate(CreateView):
    model = OrderInfo
    template_name = 'ribbon/single_purchase.html'
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
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if self.request.user.is_authenticated:
                form.instance.user = self.request.user
            else:
                form.instance.user = None
            order_info = form.save() 
            print('ORDERINFO: ', order_info)
            pk = self.kwargs.get(self.pk_url_kwarg)
            ribbon = Ribbon.objects.get(id=pk)
            print('RIBBON: ', ribbon)
            quantity = self.request.POST.get('quantity')
            order_item = OrderItem(
                order_info=order_info,
                ribbon_name=ribbon.ribbon_name,
                image=ribbon.image,
                price=ribbon.price,
                quantity=quantity
                )
            order_item.item_total = order_item.get_total
            order_item.save()
            print('ITEMTOTAL: ', order_item.item_total)
            print('ORDERITEM: ', order_item)
            order_info.order_total = order_info.get_order_total
            id_order = order_info.id
            messages.success(request, f"Поздравляем! Ваш заказ номер '{id_order}' успешно оформлен!")
            print('ORDERTOTAL: ', order_info.order_total)
            return self.form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        ribbon = Ribbon.objects.get(id=pk)
        context['ribbon'] = ribbon
        return context


class OrderInfoList(ListView):
    model = OrderInfo
    context_object_name = 'orderinfos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orderinfos'] = context['orderinfos'].filter(user=self.request.user).order_by('-created')
        return context


class OrderInfoDetail(DetailView):
    model = OrderInfo
    context_object_name = 'orderinfo'



class RegisterPage(FormView):
    template_name = 'ribbon/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(RegisterPage, self).get(*args, **kwargs)


class RibbonLoginView(LoginView):
    template_name = 'ribbon/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


    