from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.simple_login, name='simple_login'),
    path('register/', views.register_user, name='register_user'),
    path('contact/', views.contact_form, name='contact_form'),
]