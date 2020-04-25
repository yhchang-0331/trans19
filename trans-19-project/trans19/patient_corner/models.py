from django.db import models

class Patient(models.Model):
    caseId = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    Id_doc_num = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    confirmed_date = models.DateField()
    
    def __str__(self):
        return f'{self.last_name} {self.first_name}'
    
class Location(models.Model):
    location_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    x_coord = models.BigIntegerField()
    y_coord = models.BigIntegerField()
    district_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.location_name
        
class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
    detail = models.CharField(max_length=50)
    category_name = models.CharField(max_length=15)
    
    def __str__(self):
        return self.category_name
