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

from .models import Ribbon, OrderInfo, OrderItem, PreOrder
from .forms import OrderItemForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from .serializers import RibbonSerializer, OrderItemSerializer
from django.http import JsonResponse
from django.http import Http404


class RibbonList(ListView):
    model = Ribbon
    template_name = 'ribbon/index.html'
    context_object_name = 'ribbons'


class OrderInfoCreate(CreateView): 
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
    template_name = 'ribbon/single_purchase.html'
    success_url = reverse_lazy('index')

    def create_order_item(self, request, order_info):
        pk = self.kwargs.get(self.pk_url_kwarg)
        ribbon = Ribbon.objects.get(id=pk)
        quantity = self.request.POST.get('quantity')
        order_item = OrderItem(
            order_info=order_info,
            ribbon_name=ribbon.ribbon_name,
            image=ribbon.image,
            price=ribbon.price,
            quantity=quantity,
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
            id_order = order_info.id
            messages.success(request, f"Поздравляем! Ваш заказ номер '{id_order}' успешно оформлен!")
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


# class OrderAPI(APIView):
#     def get_ribbon(self, pk):
#         ribbon = Ribbon.objects.get(id=pk)
#         return ribbon

#     def post(self, request):
#         user = request.user
#         order_info = OrderInfo(user=user)
#         order_info.save()
#         print('ORDERITEM: ', order_info)
#         pk = request.data['ribbonId']
#         ribbon = self.get_ribbon(pk)
#         print('ribbon_test', ribbon)

        # order_item = OrderItemForm(instance=ribbon)
        # if order_item.is_valid():
        #     order_item.save()
        # print('order_item', order_item.data)
        # print('order_item', order_item.ribbon_name)
        # print('order_item', order_item.image)
        # print('order_item', order_item.price)
        # print('errors', order_item.error_class)
        # print('order_item', order_item)

        # order_item = OrderItem(
        #     order_info=order_info,
        #     ribbon_name=ribbon.ribbon_name,
        #     image=ribbon.image,
        #     price=ribbon.price,
        #     # quantity=quantity,
        #     )
        # order_item.quantity = order_item.quantity + 6
        # order_item.item_total = order_item.get_total
        # order_item.save()
        # print('order_item: ', order_item.quantity)

        # serializer = OrderItemSerializer(order_item)
        # print('serializer: ', serializer.data)
        # return Response(serializer.data)


class RibbonAPI(APIView):
    def get(self, request):
        all_preorder = PreOrder.objects.all()
        print('PREORDER_ALL: ', all_preorder)
        if not all_preorder: 
            return Response({'item_quantity':0}) 
        else:
            preorder = PreOrder.objects.all().order_by('-created')[0]
            return Response({'item_quantity':preorder.get_quantity_total})

    def post(self, request):
        user = request.user

        try:
            preorder, created = PreOrder.objects.get_or_create(user=user)
            if created:
                preorder.save()
            print('FIRST_PREORDER: ', preorder) 
        except:
            preorder = PreOrder.objects.all().order_by('-created')[0]
            print('LAST_PREORDER: ', preorder)
        
        # new_preorder = PreOrder(user=user)
        # new_preorder.save()
        # print('NEW_PREORDER: ', new_preorder)
        # print('PREORDER: ', preorder)
        preorders = PreOrder.objects.all()
        print('ALL_PREORDERS: ', preorders)
        # preorders = PreOrder.objects.all().delete()
        # print('DELETED!!!')

        ribbon_id = request.data['ribbonId']
        print("RIBBON_ID: ", ribbon_id)
        ribbon = Ribbon.objects.get(id=ribbon_id)
        print("RIBBON: ", ribbon)

        order_item, created = OrderItem.objects.get_or_create(
            preorder=preorder,
            ribbon_name=ribbon.ribbon_name,
            image=ribbon.image,
            price=ribbon.price,
        )
        order_item.quantity = order_item.quantity + 1
        print("QUANTITY: ", order_item.quantity)
        order_item.item_total = order_item.get_total
        print("ITEM_TOTAL: ", order_item.item_total)
        order_item.save()
        print("ORDER_ITEM: ", order_item)
            


        # if request.data['submit']:
        #     last_order_info = OrderInfo.objects.all().order_by('-created')[0]
        #     new_order_info_id = last_order_info.id + 1
        #     new_order_info = OrderInfo(id=new_order_info_id, user=user)
        #     new_order_info.save()
        #     order_info, created = OrderInfo.objects.get_or_create(id=new_order_info.id, user=user)
        # else:
        #     order_info, created = OrderInfo.objects.get_or_create(user=user)



        # order_info, created = OrderInfo.objects.get_or_create(id=155, user=user)
        # if created:
        #     order_info.save()
        # print('ORDER_INFO: ', order_info)

        # ribbon = Ribbon.objects.get(id=ribbon_id)
        # print("RIBBON: ", ribbon)

        # order_item, created = OrderItem.objects.get_or_create(
        #     order_info=order_info,
        #     ribbon_name=ribbon.ribbon_name,
        #     image=ribbon.image,
        #     price=ribbon.price,
        # )
        # print("ORDER_ITEM: ", order_item)
        # print("ORDER_ITEM_QUANTITY: ", order_item.quantity)
        # print('ORDER_INFO: ', order_info.get_quantity_total)
        return Response({'item_quantity':preorder.get_quantity_total})



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


    