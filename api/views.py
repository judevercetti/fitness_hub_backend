from django.shortcuts import render
from rest_framework import viewsets, filters
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View

from .models import Attendance, Member, MembershipPlan, Payment
from .serializers import AttendanceSerializer, MemberSerializer, MembershipPlanSerializer, PaymentSerializer

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


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer



class PaymentReceiptView(View):
    def get(self, request, payment_id):
        # payment_id = kwargs['payment_id']
        payment = Payment.objects.get(id=payment_id)
        # Add logic to generate the receipt HTML here or render a template
        receipt_html = f"<h1>Payment Receipt</h1><p>Amount: ${payment.amount}</p>"  # Replace with your receipt content
        return render(request, 'payments/payment_receipt.html', {'payment': payment})
        # payment = Payment.objects.get(id=payment_id)

        # template = get_template('payments/payment_receipt.html')
        # context = {'payment': payment}
        # html = template.render(context)

        # pdf = BytesIO()
        # pisa.CreatePDF(BytesIO(html.encode('utf-8')), pdf)

        # response = HttpResponse(pdf, content_type='application/pdf')
        # response['Content-Disposition'] = 'filename="payment_receipt.pdf"'
        # return html