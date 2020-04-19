from django.urls import path
from patient_corner import views

urlpatterns = [
    path('patientVisits/<int:patient>',views.PatientVisitData.as_view(),
    name='patient-visits'),
    path('patients',views.PatientsViewAll.as_view(),
    name='patients'),
]