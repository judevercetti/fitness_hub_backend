from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Attendance, Equipment, GymClass, Member, MembershipPlan, Payment, UserProfile

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = 'date_of_birth', 'join_date'


class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = '__all__'
        
        
class AttendanceSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = '__all__'
        
    def get_member_name(self, obj):
        return obj.member.__str__()
        

class PaymentSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    def get_member_name(self, obj):
        return obj.member.__str__()
        

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'
        

class GymClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymClass
        fields = '__all__'
        
        
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'userprofile']
#         depth = 1

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'position']


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='userprofile.phone_number', allow_blank=True, allow_null=True)
    address = serializers.CharField(source='userprofile.address', allow_blank=True, allow_null=True)
    position = serializers.ChoiceField(source='userprofile.position', choices=UserProfile.POSITION_CHOICES, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'address', 'position']

    def update(self, instance, validated_data):
        if 'userprofile' in validated_data:
            userprofile_data = validated_data.pop('userprofile')
            UserProfile.objects.update_or_create(user=instance, defaults=userprofile_data)

        return super(UserSerializer, self).update(instance, validated_data)