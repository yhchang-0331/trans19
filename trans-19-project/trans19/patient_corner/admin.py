from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Patient)
admin.site.register(Location)
admin.site.register(Visit)
admin.site.register(User)
