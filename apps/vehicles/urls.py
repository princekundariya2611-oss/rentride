from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    path('', views.vehicle_list_view, name='list'),
    path('<int:pk>/', views.vehicle_detail_view, name='detail'),
]
