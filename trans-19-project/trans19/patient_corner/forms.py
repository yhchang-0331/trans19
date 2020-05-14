from django import forms
from patient_corner.models import Patient, Location, Visit
from django.db.models import Count, Min, Sum, Avg
import datetime

district_name_choices = [
    ('Hong Kong Island CW', 'Central and Western'),
    ('Hong Kong Island E', 'Eastern'),
    ('Hong Kong Island S', 'Southern'),
    ('Hong Kong Island W', 'Wanchai'),
    ('Kowloon KC', 'Kowloon City'),
    ('Kowloon KT', 'Kwun Tong'),
    ('Kowloon SSP', 'Sham Shui Po'),
    ('Kowloon WTS', 'Wong Tai Sin'),
    ('Kowloon YTM', 'Yau Tsim Mong'),
    ('New Territories I', 'Islands'),
    ('New Territories KT', 'Kwai Tsing'),
    ('New Territories N', 'North'),
    ('New Territories SK', 'Sai Kung'),
    ('New Territories ST', 'Sha Tin'),
    ('New Territories TP', 'Tai Po'),
    ('New Territories TW', 'Tsuen Wan'),
    ('New Territories TM', 'Tuen Mun'),
    ('New Territories YL', 'Yuen Long'),
]

window_day_choices = [
    (0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),
    (8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14)
]

class PatientCreateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget = forms.SelectDateWidget(years=range(1940,2021)))
    confirmed_date = forms.DateField(widget = forms.SelectDateWidget(years = range(2019,2021)))
    
    class Meta:
        model = Patient
        fields = '__all__'

class LocationCreateForm(forms.ModelForm):
    district_name = forms.ChoiceField(choices=district_name_choices, required=True )
    
    class Meta:
        model = Location
        fields = '__all__'

class VisitCreateForm(forms.ModelForm):
    date_from = forms.DateField(widget = forms.SelectDateWidget(years=range(2019,2021)))
    date_to = forms.DateField(widget = forms.SelectDateWidget(years=range(2019,2021)))
    
    class Meta:
        model = Visit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.all().order_by('caseId')
        self.fields['location'].queryset = Location.objects.all().order_by('location_name')

class SearchConnectionForm(forms.ModelForm):
    date = forms.DateField(widget = forms.SelectDateWidget(years=range(1940,2021)),initial=datetime.date.today)
    #date = forms.ChoiceField(choices=date_choices, required=True)
    Window_day = forms.ChoiceField(choices=window_day_choices, required=True)
    
    def clean_date(self):
        selected_date = self.cleaned_data['date']
        if selected_date > datetime.date.today():
            raise forms.ValidationError("Date cannot be later than today")
            return super(SearchConnectionForm, self).clean()

    class Meta:
        model = Visit
        fields = ['patient']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.all().order_by('caseId')
        
    
        