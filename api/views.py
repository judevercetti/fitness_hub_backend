from django.shortcuts import render
from rest_framework import viewsets, filters
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum

from .models import Attendance, Equipment, Member, MembershipPlan, Payment
from .serializers import AttendanceSerializer, EquipmentSerializer, MemberSerializer, MembershipPlanSerializer, PaymentSerializer


class DashboardView(APIView):
    def get(self, request, format=None):
        member_count = Member.objects.count()
        payment_count = Payment.objects.count()
        enrollment_count = 0
        attendance_count = Attendance.objects.count()
        payment_amount = Payment.objects.aggregate(total=Sum('amount'))['total']
        

        data = {
            'member_count': member_count,
            'payment_count': payment_count,
            'enrollment_count': enrollment_count,
            'attendance_count': attendance_count,
            'payment_amount': payment_amount,
        }

        return Response(data)
    

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by('-id')
    serializer_class = MemberSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'address', 'contact_number'] 


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-id')
    serializer_class = PaymentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['member__first_name', 'member__last_name'] 


class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['member__first_name', 'member__last_name'] 


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all().order_by('-id')
    serializer_class = EquipmentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class PaymentReceiptView(View):
    def get(self, request, payment_id):
        payment = Payment.objects.get(id=payment_id)
        receipt_html = f"<h1>Payment Receipt</h1><p>Amount: ${payment.amount}</p>"  # Replace with your receipt content
        return render(request, 'payments/payment_receipt.html', {'payment': payment})