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

#date_choices = []

window_day_choices = [
    (0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),
    (8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14)
]

class PatientCreateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget = forms.SelectDateWidget(years=range(1940,2021)))
    confirmed_date = forms.DateField(widget = forms.SelectDateWidget(years = range(2019,2021)))

    def clean(self):
        confirmed_date = self.cleaned_data['confirmed_date']
        date_of_birth = self.cleaned_data['date_of_birth']
        errors = []
        if confirmed_date > datetime.date.today():
            errors.append(forms.ValidationError("Confirmed date cannot be later than today"))
        if date_of_birth > datetime.date.today():
            errors.append(forms.ValidationError("Date of birth cannot be later than today"))
        if errors:
            raise forms.ValidationError(errors)
        return super(PatientCreateForm, self).clean()

    class Meta:
        model = Patient
        fields = '__all__'

class LocationCreateForm(forms.ModelForm):
    district_name = forms.ChoiceField(choices=district_name_choices, required=True )
    def clean(self):
        print(self.cleaned_data)
        x_coordinate = self.cleaned_data['x_coord']
        y_coordinate = self.cleaned_data['y_coord']
        errors = []
        if x_coordinate > 99999:
            errors.append(forms.ValidationError("X coordinate cannot be greater than 99999"))
        if y_coordinate > 99999:
            errors.append(forms.ValidationError("Y coordinate cannot be greater than 99999"))
        if errors:
            raise forms.ValidationError(errors)
        return super(LocationCreateForm, self).clean()
    class Meta:
        model = Location
        fields = '__all__'

class VisitCreateForm(forms.ModelForm):
    date_from = forms.DateField(widget = forms.SelectDateWidget(years=range(2019,2021)))
    date_to = forms.DateField(widget = forms.SelectDateWidget(years=range(2019,2021)))

    def clean(self):
        date_from = self.cleaned_data['date_from']
        date_to = self.cleaned_data['date_to']
        if date_from > date_to:
            raise forms.ValidationError('"Date from" must not be earlier than "Date to"')
            return super(VisitCreateForm, self).clean()

    class Meta:
        model = Visit
        exclude = ['patient']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.all().order_by('location_name')


class SearchConnectionForm(forms.ModelForm):
    #date = forms.DateField(widget = forms.SelectDateWidget(years=range(1940,2021)),initial=datetime.date.today)
    #date = forms.ChoiceField(choices=date_choices, required=True)
    Window_day = forms.ChoiceField(choices=window_day_choices, required=True)

    class Meta:
        model = Visit
        fields = ['patient']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.all().order_by('caseId')
