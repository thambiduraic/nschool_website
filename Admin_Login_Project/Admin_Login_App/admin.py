from django.contrib import admin
from .models import AdminLogin, courses
# Register your models here.

class LoginAdmin(admin.ModelAdmin):
    
    list_display = ['username', 'email', 'password', 'ph_no']

admin.site.register(AdminLogin, LoginAdmin)
admin.site.register(courses)