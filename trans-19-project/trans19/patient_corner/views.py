from django.views.generic import TemplateView, UpdateView, FormView
from django.views.generic.list import ListView
from patient_corner.forms import LocationCreateForm, PatientCreateForm, VisitCreateForm, SearchConnectionForm
from patient_corner.models import Patient, Location, Visit
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
import datetime
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.hashers import check_password
from django.core.exceptions import PermissionDenied

class Addpatient(LoginRequiredMixin,FormView):
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
            return redirect(reverse_lazy('patients'))
        return render(request,self.template_name,{'form':form})

class Addlocation(LoginRequiredMixin,FormView):
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
            return redirect(reverse_lazy('locations'))
        return render(request,self.template_name,{'form':form})

class Addvisit(LoginRequiredMixin,FormView):
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
            form_of_visits = form.save(commit=False)
            form_of_visits.patient = Patient.objects.get(pk = patient)
            form.save()
            return redirect(reverse_lazy('patient_visit',args =[patient]))
        return render(request,self.template_name,{'form':form,'patient':patient})


class Editpatient(LoginRequiredMixin,UpdateView):
    model = Patient
    form_class = PatientCreateForm
    template_name = "patient_corner/edit_patient.html"

    def get_object(self, *args, **kwargs):
        patient = get_object_or_404(Patient, pk=self.kwargs['patient'])
        return patient

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('patients')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class Editvisit(LoginRequiredMixin,UpdateView):
    model = Visit
    form_class = VisitCreateForm
    template_name = "patient_corner/edit_visit.html"

    def get_object(self, *args, **kwargs):
        visit = get_object_or_404(Visit, pk=self.kwargs['visit'])
        return visit

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self, *args, **kwargs):
        number = self.kwargs['visit']
        visit = get_object_or_404(Visit, pk=number)
        patient = visit.patient.caseId
        return reverse_lazy('patient_visit',args=[patient])

class Editlocation(LoginRequiredMixin,UpdateView):
    model = Location
    form_class = LocationCreateForm
    template_name = "patient_corner/edit_location.html"

    def get_object(self, *args, **kwargs):
        location = get_object_or_404(Location, pk=self.kwargs['location'])
        return location

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('locations')

class PatientVisitData(LoginRequiredMixin,TemplateView):
    template_name = "patient_corner/visit_list.html"

    def get_context_data(self, **kwargs):
        patient = self.kwargs['patient']
        context = super().get_context_data(**kwargs)
        context['visit_list'] = Visit.objects.filter(patient__pk = patient)
        context['patient'] = Patient.objects.get(pk = patient)
        return context

    def post(self,request,patient):
        tbd = request.POST.getlist('visit_to_be_deleted')
        if tbd != []:
            request.session['visit_to_be_deleted'] = tbd
        return redirect(reverse_lazy('deletevisit',args = [patient]))

class ViewPatients(LoginRequiredMixin,ListView):
    template_name = "patient_corner/patient_list.html"
    model = Patient

    def post(self,request):
        tbd = request.POST.getlist('patient_to_be_deleted')
        if tbd != []:
            request.session['patient_to_be_deleted'] = tbd
        return redirect(reverse_lazy('deletepatient'))


class DeletePatient(LoginRequiredMixin,TemplateView):
    template_name = 'patient_corner/delete_patient.html'
    def get(self,request):
        patient_nos = request.session['patient_to_be_deleted']
        patients = Patient.objects.filter(caseId__in=patient_nos)
        args = {'patients':patients}
        return render(request,self.template_name,args)

    def post(self,request):
        if 'delete_entry' in request.POST:
            patient_nos = request.session['patient_to_be_deleted']
            Patient.objects.filter(caseId__in=patient_nos).delete()
            del request.session['patient_to_be_deleted']
        return redirect(reverse_lazy('patients'))

class DeleteVisit(LoginRequiredMixin,TemplateView):
    template_name = 'patient_corner/delete_visit.html'
    def get(self,request,patient):
        visit_nos = request.session['visit_to_be_deleted']
        visit = Visit.objects.filter(pk__in=visit_nos)
        args = {'visits':visit}
        return render(request,self.template_name,args)

    def post(self,request,patient):
        if 'delete_entry' in request.POST:
            visit_nos = request.session['visit_to_be_deleted']
            Visit.objects.filter(pk__in=visit_nos).delete()
        return redirect(reverse_lazy('patient_visit',args = [patient]))

class DeleteLocation(LoginRequiredMixin,TemplateView):
    template_name = 'patient_corner/delete_location.html'
    def get(self,request):
        location_nos = request.session['location_to_be_deleted']
        locations = Location.objects.filter(pk__in=location_nos)
        args = {'locations':locations}
        return render(request,self.template_name,args)

    def post(self,request):
        if 'delete_entry' in request.POST:
            location_nos = request.session['location_to_be_deleted']
            Location.objects.filter(pk__in=location_nos).delete()
            del request.session['location_to_be_deleted']
        return redirect(reverse_lazy('locations'))

class ViewLocations(LoginRequiredMixin,ListView):
    template_name = "patient_corner/location_list.html"
    model = Location
    def post(self,request):
        tbd = request.POST.getlist('location_to_be_deleted')
        if tbd != []:
            request.session['location_to_be_deleted'] = tbd
        print(request.session['location_to_be_deleted'])
        return redirect(reverse_lazy('deletelocation'))

class Home(LoginRequiredMixin,ListView):
    template_name = "patient_corner/homepage.html"
    model = Patient # Though we don't need this we must declare else it won't compile

class SearchConnection(UserPassesTestMixin,LoginRequiredMixin,FormView):
    model = Visit
    form_class = SearchConnectionForm
    template_name = "patient_corner/searchconnection.html"
    permission_denied_message = 'You cannot access this page. Please contact admin for more information.'
    raise_exception = True

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.permission_denied_message)

    def test_func(self):
        return self.request.user.is_epidemiologist == True

    def post(self,request,**kwargs):
        form = SearchConnectionForm(request.POST)
        patient = request.POST.get('patient')
        Window_day = request.POST.get('Window_day')
        return redirect(reverse_lazy('view_connections',args = [patient,Window_day]))

class ViewConnections(UserPassesTestMixin,LoginRequiredMixin,TemplateView):
    template_name = "patient_corner/view_connections.html"
    permission_denied_message = 'You cannot access this page. Please contact admin for more information.'
    raise_exception = True

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.permission_denied_message)

    def test_func(self):
        return self.request.user.is_epidemiologist == True

    def get(self,request,*args,**kwargs):
        patient_id = int(self.kwargs['patient'])
        patient = Patient.objects.get(pk = self.kwargs['patient'])
        Window_day = self.kwargs['Window_day']
        #selected_visits = Visit.objects.filter(Q(patient_id = patient_id)&((Q(date_from__gte = date_from)&Q(date_from__lte = date_to))|(Q(date_to__gte = date_from)&Q(date_to__lte = date_to)))).order_by('date_from')
        selected_visits = Visit.objects.filter(Q(patient_id = patient_id)).order_by('date_from')
        sv_count = selected_visits.count()
        location_list = []
        for sv in selected_visits:
            location_list.append(sv.location)
        location_set = set(location_list)
        location_count = sum(1 for location in location_set)
        result = []

        for sv in selected_visits:
            date_from = sv.date_from-datetime.timedelta(days=Window_day)
            date_to = sv.date_to+datetime.timedelta(days= Window_day)
            location = sv.location
            visit_list = Visit.objects.filter(Q(location = location)&((Q(date_from__gte = date_from)&Q(date_from__lte = date_to))|(Q(date_to__gte = date_from)&Q(date_to__lte = date_to)))).exclude(patient_id = patient_id).order_by('date_from')
            for v in visit_list:
                result.append(v)

        '''
        connected_visits = Visit.objects.filter(((Q(date_from__gte = date_from)&Q(date_from__lte = date_to))|(Q(date_to__gte = date_from)&Q(date_to__lte = date_to)))).exclude(patient_id = patient_id).order_by('date_from')
        result = []
        for cv in connected_visits:
            for sv in selected_visits:
                if cv.location == sv.location and ((sv.date_from >= cv.date_from and sv.date_from <= cv.date_to) or (sv.date_from >= cv.date_from and sv.date_to <= cv.date_to)):
                    result.append(cv)
        '''

        args = {'patient': patient, 'distinct_locations': location_set, 'num_of_distinct_locations': location_count, 'sv_count': sv_count, 'selected_visits': selected_visits, 'connected_visits': result}

        return render(request, self.template_name, args)
