from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_claim, name='submit_claim'),
    path('my-claims/', views.user_claims, name='user_claims'),
    path('admin/list/', views.admin_claims_list, name='admin_claims_list'),
    path('admin/review/<int:claim_id>/', views.admin_review_claim, name='admin_review_claim'),
    path('admin/beneficiaries/', views.beneficiaries_list, name='beneficiaries_list'),
]