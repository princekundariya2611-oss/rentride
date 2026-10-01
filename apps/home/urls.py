from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home_view, name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/<int:message_id>/', views.contact_success_view, name='contact_success'),
    path('about/', views.about_view, name='about'),
]
