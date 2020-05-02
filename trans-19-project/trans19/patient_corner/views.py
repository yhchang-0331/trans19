from django.views.generic import TemplateView, UpdateView, FormView
from django.views.generic.list import ListView
from patient_corner.forms import LocationCreateForm, PatientCreateForm, VisitCreateForm
from patient_corner.models import Patient, Location, Visit
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy

class Addpatient(FormView): 
    model = Patient
    form_class = PatientCreateForm
    template_name = "patient_corner/add_patient.html"

    def get(self,request):
        form = PatientCreateForm()
        patient = Patient.objects.all()
        args = {'form':form,'add_patient':patient}
        return render(request, self.template_name, args)

    def post(self,request):
            form = PatientCreateForm(request.POST)
            if form.is_valid():
                form.save()
            form = PatientCreateForm()
            return redirect(reverse_lazy('patients'))

class Addlocation(FormView):
    model = Location
    form_class = LocationCreateForm
    template_name = "patient_corner/add_location.html"

    def get(self,request):
        form = LocationCreateForm()
        location = Location.objects.all()
        args = {'form':form,'add_location':location}
        return render(request, self.template_name, args)

    def post(self,request):
        form = LocationCreateForm(request.POST)
        if form.is_valid():
            form.save()
        form = LocationCreateForm()
        return redirect(reverse_lazy('locations'))

class Addvisit(FormView):
    model = Visit
    form_class = VisitCreateForm
    template_name = "patient_corner/add_visit.html"

    def get(self, request, **kwargs):
        form = VisitCreateForm() 
        patient = Patient.objects.get(pk = self.kwargs['patient'])
        visit = Visit.objects.filter(patient_id = patient)
        args = {'form': form,'add_visit': visit,'patient': patient}
        return render(request, self.template_name, args)

    def post(self,request,patient):
        form = VisitCreateForm(request.POST)
        if form.is_valid():
            form.save()
        form = VisitCreateForm()
        return redirect(reverse_lazy('patient_visit',args =[patient]))

class Editpatient(UpdateView): 
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
        patient = visit.patient.caseId
        return reverse_lazy('patient_visit',args=[patient])
        
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
    
    def get_context_data(self, **kwargs):
        patient = self.kwargs['patient']
        context = super().get_context_data(**kwargs)
        context['visit_list'] = Visit.objects.filter(patient__pk = patient)
        context['patient'] = Patient.objects.get(pk = patient)
        return context

class ViewPatients(ListView):
    template_name = "patient_corner/patient_list.html"
    model = Patient

class ViewLocations(ListView):
    template_name = "patient_corner/location_list.html"
    model = Location

class Home(ListView):
    template_name = "patient_corner/homepage.html"
    model = Patient # Though we don't need this we must declare else it won't compile
