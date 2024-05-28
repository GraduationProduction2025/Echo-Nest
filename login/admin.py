from django.contrib import admin

# Register your models here.

from .models import Users, Admins

class LoginAdmin(admin.ModelAdmin):
    list_display = ('Users', 'Admins')

admin.site.register(Users)
admin.site.register(Admins)