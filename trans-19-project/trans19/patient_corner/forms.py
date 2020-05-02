from django import forms
from patient_corner.models import Patient, Location, Visit
#from django.core.validators import MaxValueValidator, MinValueValidator

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

class PatientCreateForm(forms.ModelForm):
    #first_name = forms.CharField(label='First Name')
    #last_name = forms.CharField(max_length=15)
    #Id_doc_num = forms.CharField(max_length=15)
    date_of_birth = forms.DateField(widget = forms.SelectDateWidget(years=range(1940,2021)))
    confirmed_date = forms.DateField(widget = forms.SelectDateWidget(years = range(2019,2021)))
    
    class Meta:
        model = Patient
        fields = '__all__'

class LocationCreateForm(forms.ModelForm):
    #location_name = forms.CharField(max_length=50)
    #address = forms.CharField(max_length=50)
    #x_coord = forms.BigIntegerField()
    #y_coord = forms.BigIntegerField()
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
