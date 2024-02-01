from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    POSITION_CHOICES = (
        ('trainer', 'Trainer'),
        ('manager', 'Manager'),
        ('receptionist', 'Receptionist'),
        ('cleaner', 'Cleaner'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, blank=True, null=True)


class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    join_date = models.DateField(auto_now_add=True)
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='subscriptions')
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.start_date and self.membership_plan:
            self.expiry_date = self.start_date + timedelta(days=self.membership_plan.duration)
        super().save(*args, **kwargs)


class GymClass(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    schedule = models.DateTimeField(blank=True, null=True)
    max_capacity = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, blank=True, null=True)
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, default='cash')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Equipment(models.Model):
    CONDITION_CHOICES = [
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    purchase_date = models.DateField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_all_day = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Document(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)