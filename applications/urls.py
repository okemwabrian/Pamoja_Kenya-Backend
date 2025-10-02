from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_applications, name='applications_list'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('submit/', views.submit_application, name='submit_application'),
    path('<int:application_id>/documents/', views.application_documents, name='application_documents'),
]