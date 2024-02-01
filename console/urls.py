from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.contrib.auth import views as auth_views

from .views import AttendanceViewSet, ChangePasswordView, DashboardView, DocumentViewSet, EmployeeViewSet, EventViewSet, GymClassViewSet, MemberViewSet, MembershipPlanViewSet, MyTokenObtainPairView, PaymentReceiptView, PaymentViewSet, EquipmentViewSet, SubscriptionViewSet

router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'membershipplans', MembershipPlanViewSet)
router.register(r'attendances', AttendanceViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'equipments', EquipmentViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'gymclasses', GymClassViewSet)
router.register(r'events', EventViewSet)
router.register(r'documents', DocumentViewSet)


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('payment/<int:payment_id>/receipt/',
         PaymentReceiptView.as_view(), name='payment_receipt'),

    path('', include(router.urls)),
]
