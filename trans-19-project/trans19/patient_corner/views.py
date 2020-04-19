from django.views.generic import TemplateView
from django.views.generic.list import ListView
from patient_corner.models import Patient, Location, Visit

class PatientVisitData(TemplateView):
    template_name = "patient_corner/visit_list.html"
    
    def get_context_data(self, **kwargs):
        patient = self.kwargs['patient']
        context = super().get_context_data(**kwargs)
        context['visit_list'] = Visit.objects.filter(patient__pk = patient)
        context['patient'] = Patient.objects.get(pk = patient)
        return context
 
class PatientsViewAll(ListView):
    template_name = "patient_corner/patient_list.html"
    model = Patient
