from django.views.generic import TemplateView, UpdateView
from django.views.generic.list import ListView
from patient_corner.forms import LocationCreateForm, PatientCreateForm, VisitCreateForm
from patient_corner.models import Patient, Location, Visit
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


class Editpatient(UpdateView): #Note that we are using UpdateView and not FormView
    model = Patient
    form_class = PatientCreateForm
    template_name = "patient_corner/edit_patient.html"

    def get_object(self, *args, **kwargs):
        patient = get_object_or_404(Patient, pk=self.kwargs['patient'])
        return patient

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('patients')

class Editvisit(UpdateView):
    model = Visit
    form_class = VisitCreateForm
    template_name = "patient_corner/edit_visit.html"

    def get_object(self, *args, **kwargs):
        visit = get_object_or_404(Visit, pk=self.kwargs['visit'])
        return visit

    def get_success_url(self, *args, **kwargs):
        number = self.kwargs['visit']
        visit = get_object_or_404(Visit, pk=number)
        patient = Patient.objects.get(pk = visit)
        print(patient)
        patient = patient.pk
        print(patient)
        return reverse_lazy('patient_visit',args = {patient,number})

class Editlocation(UpdateView):
    model = Location
    form_class = LocationCreateForm
    template_name = "patient_corner/edit_location.html"

    def get_object(self, *args, **kwargs):
        location = get_object_or_404(Location, pk=self.kwargs['location'])
        return location

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('locations')

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
            form_of_visits = form.save(commit=False)
            form_of_visits.patient = Patient.objects.get(pk = patient)
            form.save()
        form = VisitCreateForm()
        return redirect(reverse_lazy('patient_visit',args =[patient]))

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
            return redirect(reverse_lazy('patients'))

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
            return redirect(reverse_lazy('locations'))
