from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.contrib.auth import views as auth_views

from .views import AttendanceViewSet, DashboardView, EmployeeViewSet, GymClassViewSet, MemberViewSet, MembershipPlanViewSet, MyTokenObtainPairView, PaymentReceiptView, PaymentViewSet, EquipmentViewSet

router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'membershipplans', MembershipPlanViewSet)
router.register(r'attendances', AttendanceViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'equipments', EquipmentViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'gymclasses', GymClassViewSet)


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('payment/<int:payment_id>/receipt/',
         PaymentReceiptView.as_view(), name='payment_receipt'),

    path('', include(router.urls)),
]
