# pylint: disable=E1101
from django.shortcuts import render, redirect
from django.contrib import messages

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, DeleteView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Ribbon, OrderInfo, OrderItem, PreOrder
from .forms import OrderItemForm, OrderInfoForm
from .utils import success_message


class RibbonList(ListView):
    model = Ribbon
    template_name = 'ribbon/index.html'
    context_object_name = 'ribbons'


class OrderInfoCreate(CreateView): 
    form_class = OrderInfoForm
    template_name = 'ribbon/single_purchase.html'
    success_url = reverse_lazy('index')

    def create_order_item(self, request, order_info):# create a single purchase
        pk = self.kwargs.get(self.pk_url_kwarg)
        ribbon = Ribbon.objects.get(id=pk)
        quantity = self.request.POST.get('quantity')
        order_item = OrderItem(
            order_info = order_info,
            ribbon_name=ribbon.ribbon_name,
            image=ribbon.image,
            price=ribbon.price,
            quantity = quantity,
        )
        order_item.item_total = order_item.get_total
        order_item.save()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if self.request.user.is_authenticated:
                form.instance.user = self.request.user
            else:
                form.instance.user = None
            order_info = form.save()
            self.create_order_item(request, order_info)
            order_info.order_total = order_info.get_order_total
            success_message(request, order_info.id)# pops on index page
            return self.form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        ribbon = Ribbon.objects.get(id=pk)
        context['ribbon'] = ribbon
        return context


class OrderInfoList(LoginRequiredMixin, ListView):
    model = OrderInfo
    context_object_name = 'orderinfos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orderinfos'] = context['orderinfos'].filter(user=self.request.user).order_by('-created')
        return context


class OrderInfoDetail(LoginRequiredMixin, DetailView):
    model = OrderInfo
    context_object_name = 'orderinfo'


class RibbonAPI(LoginRequiredMixin, APIView):
    def create_or_update_order_item(self, ribbon_id, pk):
        preorder = PreOrder.objects.get(id=pk)
        ribbon = Ribbon.objects.get(id=ribbon_id)
        # create a new or update an existent orderitem based on the given ribbon and preorder
        order_item, created = OrderItem.objects.get_or_create(
            preorder=preorder,
            ribbon_name=ribbon.ribbon_name,
            image=ribbon.image,
            price=ribbon.price,
        )
        if created:
            order_item.save()
        order_item.quantity = order_item.quantity + 1 #increase qunatity on each click
        order_item.item_total = order_item.get_total
        order_item.save()

    def get(self, request):
        # check if logged in user has preorders
        all_preorder = PreOrder.objects.all().filter(user=self.request.user)
        if not all_preorder: 
            return Response({'item_quantity':0}) 
        else:# if user has preorders grab a last one and return its total quantity 
            preorder = PreOrder.objects.all().filter(user=self.request.user).order_by('-created')[0]
            return Response({'item_quantity':preorder.get_quantity_total})

    def post(self, request):
        user = request.user
        try:
            preorder, created = PreOrder.objects.get_or_create(user=user)
            if created:
                preorder.save()
        except:# if there are multiple preorders, grab a last one
            preorder = PreOrder.objects.all().filter(user=self.request.user).order_by('-created')[0]

        ribbon_id = request.data['ribbonId']# from the fetch

        # create a new or update an existent orderitem based on the given ribbon and preorder
        self.create_or_update_order_item(ribbon_id=ribbon_id, pk=preorder.id)

        return Response({'item_quantity':preorder.get_quantity_total})


class CartPage(LoginRequiredMixin, CreateView):
    form_class = OrderInfoForm
    template_name = 'ribbon/cart_page.html'
    success_url = reverse_lazy('index')

    def create_orderinfo(self, request, orderinfo):# mapping preorder to infoorder
        preorder =  PreOrder.objects.all().filter(user=request.user).order_by('-created')[0]
        orderitems = preorder.orderitem_set.all()
        for orderitem in orderitems:
            orderitem.order_info = orderinfo# preorder's orderitems now orderinfo's
            orderitem.save()
        orderinfo.order_total = orderinfo.get_order_total
        orderinfo.save()
        success_message(request, orderinfo.id)# pops on index page 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            last_preorder = PreOrder.objects.all().filter(user=self.request.user).order_by('-created')[0]
            context['preorder'] = last_preorder
        except:
            last_preorder = None #empty cart
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.user = request.user
            orderinfo = form.save()
            self.create_orderinfo(request, orderinfo)
            new_preorder = PreOrder(user=request.user) #prep cart for next purchase
            new_preorder.save()
            return self.form_valid(form)


class DeletePreorder(LoginRequiredMixin, DeleteView):
    model = PreOrder
    context_object_name = 'preorder'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        new_preorder = PreOrder(user=request.user) #prep cart for next purchase
        new_preorder.save()
        return self.delete(request, *args, **kwargs)


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


    