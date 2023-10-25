from rest_framework import serializers
from .models import Attendance, Member, MembershipPlan, Payment

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = 'date_of_birth', 'join_date'


class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = '__all__'
        
        
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        
        
class PaymentSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    def get_member_name(self, obj):
        return obj.member.__str__()
        