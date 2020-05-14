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
        name = 'locations'),
    path('editpatient/<int:patient>',
        views.Editpatient.as_view(),
        name='editpatient'),
    path('<int:patient>/editvisit/<int:visit>',
        views.Editvisit.as_view(),
        name='editvisit'),
    path('editlocation/<int:location>',
        views.Editlocation.as_view(),
        name='editlocation'),
    path('addpatient',
        views.Addpatient.as_view(),
        name='addpatient'),
    path('addlocation',
        views.Addlocation.as_view(),
        name='addlocation'),
    path('<int:patient>/addvisit',
        views.Addvisit.as_view(),
        name='addvisit'),
    path('home',
        views.Home.as_view(),
        name='home'),
    path('deletepatient',
        views.DeletePatient.as_view(),
        name = 'deletepatient'),
    path('deletelocation',
        views.DeleteLocation.as_view(),
        name = 'deletelocation'),
    path('deletevisit/<int:patient>',
        views.DeleteVisit.as_view(),
        name = 'deletevisit'),
    path('searchconnection',
        views.SearchConnection.as_view(),
        name = 'searchconnection'),
    path('connections/patientid=<str:patient>/window=<int:Window_day>',
        views.ViewConnections.as_view(),
        name = 'view_connections')
]