from django.contrib import admin
from .models import Project,Image,My_Investment,My_income,Profile

# Register your models here.
admin.site.register(Project)
admin.site.register(Image)
admin.site.register(My_Investment)
admin.site.register(My_income)
admin.site.register(Profile)