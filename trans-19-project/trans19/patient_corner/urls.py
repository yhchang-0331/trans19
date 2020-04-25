from django.urls import path
from patient_corner import views

urlpatterns = [
    path('patients/<int:patient>',
        views.PatientVisitData.as_view(),
        name = 'patient_visit'),
    path('patients',
        views.ViewPatients.as_view(),
        name = 'patients'),
    path('locations',
        views.ViewLocations.as_view(),
        name = 'locations')
]