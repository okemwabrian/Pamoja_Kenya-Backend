from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_claims, name='user_claims'),  # GET /api/claims/
    path('submit/', views.submit_claim, name='submit_claim'),  # POST /api/claims/submit/
    path('<int:claim_id>/documents/', views.claim_documents, name='claim_documents'),  # GET /api/claims/{id}/documents/
    path('admin/list/', views.admin_claims_list, name='admin_claims_list'),
    path('admin/review/<int:claim_id>/', views.admin_review_claim, name='admin_review_claim'),
    path('admin/beneficiaries/', views.beneficiaries_list, name='beneficiaries_list'),
]