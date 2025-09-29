from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Beneficiary, BeneficiaryChangeRequest
from .serializers import BeneficiarySerializer, BeneficiaryChangeRequestSerializer

class BeneficiaryListCreateView(generics.ListCreateAPIView):
    serializer_class = BeneficiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Beneficiary.objects.filter(user=self.request.user)

class BeneficiaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BeneficiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Beneficiary.objects.filter(user=self.request.user)

@api_view(['GET'])
def beneficiary_list_view(request):
    """Public view for displaying masked beneficiary data"""
    beneficiaries = Beneficiary.objects.filter(is_active=True)[:10]  # Limit for demo
    data = []
    for b in beneficiaries:
        data.append({
            'name': b.name,
            'phone': b.phone,
            'email': b.email
        })
    return Response(data)

class BeneficiaryChangeRequestView(generics.CreateAPIView):
    serializer_class = BeneficiaryChangeRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class BeneficiaryChangeRequestListView(generics.ListAPIView):
    serializer_class = BeneficiaryChangeRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BeneficiaryChangeRequest.objects.filter(user=self.request.user)