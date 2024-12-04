from django.shortcuts import render
from rest_framework import viewsets, filters, status
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
from django.db.models.functions import Lower

from .models import Attendance, Document, Equipment, Event, GymClass, Member, MembershipPlan, Payment, Event, Subscription
from .serializers import (AttendanceSerializer, ChangePasswordSerializer, DocumentSerializer, EmployeeSerializer, EquipmentSerializer, EventSerializer, GymClassSerializer,
                          MemberSerializer, MembershipPlanSerializer, MyTokenObtainPairSerializer, PaymentSerializer, SubscriptionSerializer)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ChangePasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')
        if not check_password(old_password, request.user.password):
            return Response({"old_password": ["Your old password is incorrect."]}, status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(new_password)
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class DashboardView(APIView):
    def get(self, request, format=None):
        today = timezone.now().date()
        
        member_count = Member.objects.count()
        payment_count = Payment.objects.count()
        event_count = Event.objects.filter(start_time__gte=timezone.now()).count()
        enrollment_count = 0
        attendance_count = Attendance.objects.count()
        documents = Document.objects.all()
        payment_amount = Payment.objects.filter(created_at__date=today).aggregate(
            total=Sum('amount'))['total']
        # fetch sum of daily payments to be used in a line chart for the past 7days, list object should be name of day and total
        daily_payments = Payment.objects.extra(select={'day': 'date( created_at )'}).values('day').annotate(
            total=Sum('amount')).order_by('-day')[:7]
        
        # fetch sum of monthly payments to be used in a line chart for the past 12months, list object should be name of month and total
        # monthly_payments = Payment.objects.extra(select={'month': 'date_trunc( \'month\', created_at )'}).values('month').annotate(
        #     total=Sum('amount')).order_by('-month')[:12]


        seven_days_ago = timezone.now() - timezone.timedelta(days=6)
        last_7_days = [(seven_days_ago + timezone.timedelta(days=x)).strftime("%a") for x in range(7)]

        payments_by_day = {datetime.strptime(payment['day'], '%Y-%m-%d').strftime("%a"): payment['total'] for payment in daily_payments}
        payments_list = [{'date': day, 'total': payments_by_day.get(day, 0)} for day in last_7_days]


        current_attendance = Attendance.objects.filter(created_at__date=today)
        current_attendance_list = [{
            'name': attendance.member.__str__(),
            'time_in': attendance.check_in_time,
        } for attendance in current_attendance]
        

        data = {
            'member_count': member_count,
            'payment_count': payment_count,
            'event_count': event_count,
            'enrollment_count': enrollment_count,
            'attendance_count': attendance_count,
            'payment_amount': payment_amount,
            'payments_list': payments_list,
            'documents': documents,
            'current_attendance_count': current_attendance.count(),
            'current_attendance_list': current_attendance_list,
        }

        return Response(data)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by(Lower('first_name'), Lower('last_name'))
    serializer_class = MemberSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'address', 'contact_number']

    @action(detail=True, methods=['get'])
    def subscriptions(self, request, pk=None):
        member = self.get_object()
        subscriptions = Subscription.objects.filter(member=member)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-id')
    serializer_class = PaymentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['member__first_name', 'member__last_name']

    @action(detail=False, methods=['get'])
    def total(self, request, *args, **kwargs):
        total_payments = Payment.objects.aggregate(total=Sum('amount')).get('total') or 0
        return Response({'total_payments': total_payments})

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all().order_by('-id')
    serializer_class = SubscriptionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['member__first_name', 'member__last_name']


class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all().order_by('-id')
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


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'userprofile__phone_number']


class GymClassViewSet(viewsets.ModelViewSet):
    queryset = GymClass.objects.all().order_by('-id')
    serializer_class = GymClassSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'instructor__first_name', 'instructor__last_name']


class PaymentReceiptView(View):
    def get(self, request, payment_id):
        payment = Payment.objects.get(id=payment_id)
        # Replace with your receipt content
        receipt_html = f"<h1>Payment Receipt</h1><p>Amount: ${payment.amount}</p>"
        return render(request, 'payments/payment_receipt.html', {'payment': payment})


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-id')
    serializer_class = EventSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-id')
    serializer_class = DocumentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']