from django.shortcuts import render, redirect

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView

from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Ribbon, OrderInfo


class RibbonList(ListView):
    model = Ribbon
    template_name = 'ribbon/index.html'
    context_object_name = 'ribbons'


class RibbonCreate(CreateView):
    model = OrderInfo
    fields = '__all__'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(RibbonCreate, self).form_valid(form)



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


    