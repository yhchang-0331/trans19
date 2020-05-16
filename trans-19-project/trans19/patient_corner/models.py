from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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

class UserManager(BaseUserManager):
    def create_user(self, email, username, staff_num, is_epidemiologist, password=None):
        if not email:
            raise ValueError("Users must have an email")
        if not username:
            raise ValueError("Users must have a username")
        if not staff_num:
            raise ValueError("Users must have a staff number")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            staff_num=staff_num,
            is_epidemiologist=is_epidemiologist,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, staff_num, is_epidemiologist, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            staff_num=staff_num,
            is_epidemiologist=is_epidemiologist,          
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    is_epidemiologist = models.BooleanField(default=False)
    email = models.EmailField(verbose_name="email", max_length=30, unique=True)
    username = models.CharField(verbose_name="username", max_length=20, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    staff_num = models.CharField(verbose_name="staff number",max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'staff_num','is_epidemiologist']

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

