from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from api.models import *

admin.site.site_header = "FITNESS HUB ADMIN"
admin.site.site_title = "FITNESS HUB"
admin.site.index_title = "ADMIN"

# Register your models here.
admin.site.register([])


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name','price','duration','features')


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'address')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'payment_method', 'created_at', 'print_button')

    def print_button(self, obj):
        url = reverse('payment_receipt', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">Print<a/>', url)
    
    print_button.short_description = ''

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'check_in_time', 'check_out_time')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'condition')
