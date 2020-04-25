from django.views.generic import TemplateView
from django.views.generic.list import ListView
from patient_corner.forms import LocationCreateForm, PatientCreateForm, VisitCreateForm
from patient_corner.models import Patient, Location, Visit
from django.shortcuts import render,redirect

class PatientVisitData(TemplateView):
    template_name = "patient_corner/visit_list.html"
    def get(self, request, **kwargs):
        form = VisitCreateForm() 
        patient = self.kwargs['patient']
        visit_list = Visit.objects.filter(patient__pk = patient)
        patient = Patient.objects.get(pk = patient)
        args = {'form':form,'visit_list': visit_list,'patient':patient}
        return render(request, self.template_name, args)

    # newly added code in the following    
    def post(self,request,patient):
        #print(type(patient))
        form = VisitCreateForm(request.POST)
        if form.is_valid():
            form_of_visits = form.save(commit=True)
            form_of_visits.patient = Patient.objects.get(pk = patient)
            form.save()
        form = VisitCreateForm()
        return redirect('patient_corner/patients/')

class ViewPatients(ListView):
    template_name = "patient_corner/patient_list.html"
    model = Patient
    # newly added code in the following
    def get(self,request):
            form = PatientCreateForm()
            patient = Patient.objects.all()
            args = {'form':form,'patient_list':patient}
            return render(request, self.template_name, args)

    def post(self,request):
            form = PatientCreateForm(request.POST)
            if form.is_valid():
                form.save()
            form = PatientCreateForm()
            return redirect('patient_corner/patients')

# newly added code in the following
class ViewLocations(ListView):
    template_name = "patient_corner/location_list.html"
    def get(self,request):
            form = LocationCreateForm()
            location = Location.objects.all()
            args = {'form':form,'location_list':location}
            return render(request, self.template_name, args)

    def post(self,request):
            form = LocationCreateForm(request.POST)
            if form.is_valid():
                form.save()
            form = LocationCreateForm()
            return redirect('patient_corner/locations')
