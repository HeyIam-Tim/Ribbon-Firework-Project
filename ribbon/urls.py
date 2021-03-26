from django.urls import path
from .views import RibbonList, RegisterPage, RibbonLoginView, OrderInfoCreate, OrderInfoList, OrderInfoDetail, OrderAPI
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', RibbonList.as_view(), name='index'),
    # path('api-address/', OrderInfoAPI.as_view(), name='api-address'),
    path('order-api/', OrderAPI.as_view(), name='order-api'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', RibbonLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('ribbon-create/<int:pk>/', OrderInfoCreate.as_view(), name='ribbon-create'),
    path('orderinfo-list/', OrderInfoList.as_view(), name='orderinfo-list'),
    path('orderinfo-detail/<int:pk>/', OrderInfoDetail.as_view(), name='orderinfo-detail'),
]