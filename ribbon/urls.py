from django.urls import path
from .views import RibbonList, RegisterPage, RibbonLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', RibbonList.as_view(), name='index'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', RibbonLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]