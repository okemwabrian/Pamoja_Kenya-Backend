from django.urls import path
from . import views

urlpatterns = [
    path('', views.BeneficiaryListCreateView.as_view(), name='beneficiaries'),
    path('<int:pk>/', views.BeneficiaryDetailView.as_view(), name='beneficiary_detail'),
    path('list/', views.beneficiary_list_view, name='beneficiary_list'),
    path('request/', views.BeneficiaryChangeRequestView.as_view(), name='beneficiary_change_request'),
    path('requests/', views.BeneficiaryChangeRequestListView.as_view(), name='beneficiary_change_requests'),
]