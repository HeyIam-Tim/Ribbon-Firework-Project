from django.urls import path
from .views import RibbonList 

urlpatterns = [
    path('', RibbonList.as_view(), name='index'),
]