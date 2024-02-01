from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from django.db.models import Sum

from .models import Attendance, Document, Equipment, Event, GymClass, Member, MembershipPlan, Payment, Subscription, UserProfile


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['phone_number'] = user.userprofile.phone_number
        token['position'] = user.userprofile.position
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'username': self.user.username})
        data.update({'first_name': self.user.first_name})
        data.update({'last_name': self.user.last_name})
        data.update({'phone_number': self.user.userprofile.phone_number})
        data.update({'position': self.user.userprofile.position})
        return data
    

class MemberSerializer(serializers.ModelSerializer):
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Member
        exclude = 'date_of_birth', 'join_date'

    def get_subscription(self, obj):
        subscription = Subscription.objects.filter(member=obj, expiry_date__gte=timezone.now()).first()
        return SubscriptionSerializer(subscription).data if subscription else None


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
    reason = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    def get_member_name(self, obj):
        return obj.member.__str__()
        
    def get_reason(self, obj):
        if obj.subscription is not None:
            return f'{obj.subscription.membership_plan.name} Subscription'
        elif obj.gym_class is not None:
            return f'{obj.gym_class.name} Class'
        else:
            return None


class SubscriptionSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()
    membership_plan_name = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = '__all__'

    def get_member_name(self, obj):
        return obj.member.__str__()
        
    def get_membership_plan_name(self, obj):
        return obj.membership_plan.__str__()

    def get_balance(self, obj):
        payments = Payment.objects.filter(subscription=obj).aggregate(total=Sum('amount'))
        total_paid = payments.get('total') or 0
        balance = obj.membership_plan.price - total_paid
        return str(balance)


class EquipmentSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Equipment
        fields = '__all__'
        

class GymClassSerializer(serializers.ModelSerializer):
    instructor_name = serializers.SerializerMethodField()

    class Meta:
        model = GymClass
        fields = '__all__'

    def get_instructor_name(self, obj):
        return f'{obj.instructor.first_name} {obj.instructor.last_name}'
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'position']


class EmployeeSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='userprofile.phone_number')
    address = serializers.CharField(source='userprofile.address', allow_blank=True, allow_null=True)
    position = serializers.ChoiceField(source='userprofile.position', choices=UserProfile.POSITION_CHOICES, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'address', 'position']

    def create(self, validated_data):
        userprofile_data = validated_data.pop('userprofile', None)
        validated_data['username'] = userprofile_data.get('phone_number')
        user = User.objects.create(**validated_data)
        if userprofile_data is not None:
            UserProfile.objects.create(user=user, **userprofile_data)
        return user

    def update(self, instance, validated_data):
        if 'userprofile' in validated_data:
            userprofile_data = validated_data.pop('userprofile')
            validated_data['username'] = userprofile_data.get('phone_number')
            UserProfile.objects.update_or_create(user=instance, defaults=userprofile_data)

        return super(EmployeeSerializer, self).update(instance, validated_data)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value