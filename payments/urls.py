from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentListCreateView.as_view(), name='payments'),
    path('<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('stats/', views.payment_stats_view, name='payment_stats'),
]