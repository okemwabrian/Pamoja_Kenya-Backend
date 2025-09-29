from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.create_application, name='create_application'),
    path('my-applications/', views.my_applications, name='my_applications'),
]