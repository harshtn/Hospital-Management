from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.shortcuts import render

def api_documentation_view(request):
    return render(request, 'api/docs.html')

router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet, basename='api-department')
router.register(r'rooms', views.RoomViewSet, basename='api-room')
router.register(r'doctors', views.DoctorViewSet, basename='api-doctor')
router.register(r'patients', views.PatientViewSet, basename='api-patient')
router.register(r'appointments', views.AppointmentViewSet, basename='api-appointment')
router.register(r'medical-records', views.MedicalRecordViewSet, basename='api-medical-record')
router.register(r'invoices', views.InvoiceViewSet, basename='api-invoice')

urlpatterns = [
    path('docs/', api_documentation_view, name='api_docs'),
    path('analytics/summary/', views.AnalyticsSummaryView.as_view(), name='api_analytics_summary'),
    path('', include(router.urls)),
]
