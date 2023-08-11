from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

admin.site.register(UserAccount)
# admin.site.register(Doctor)
# admin.site.register(Clinic)
# admin.site.register(Staff)


class ClinicAdmin(UserAdmin):
    list_display = ('email','is_clinic','clinic_Name','Owner_First_Name','Owner_Last_Name','Block','contact')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'password','last_login')}),
        ('Personal info', {'fields': ('is_clinic','clinic_Name','Owner_First_Name','Owner_Last_Name','Block','contact','image_and_logo')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('is_clinic','clinic_Name','Owner_First_Name','Owner_Last_Name','Block','contact','image_and_logo')}),
    )
    readonly_fields=('last_login',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Clinic,ClinicAdmin)


class DocAd(UserAdmin):
    list_display = ('email','is_doctor','first_Name','last_Name','clinic','contact')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'password','last_login','clinic')}),
        ('Personal info', {'fields': ('is_doctor','first_Name','last_Name','image_and_logo','contact')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2','clinic')}),
        ('Personal info', {'fields': ('is_doctor','first_Name','last_Name','image_and_logo',"contact")}),
    )
    readonly_fields=('last_login',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Doctor,DocAd)


class StaffAd(UserAdmin):
    list_display = ('email','is_staff','first_Name','last_Name','clinic')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'password','last_login','clinic')}),
        ('Personal info', {'fields': ('is_staff','first_Name','last_Name','contact','image_and_logo')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2','clinic')}),
        ('Personal info', {'fields': ('is_staff','first_Name','last_Name','contact','image_and_logo')}),
    )
    
    readonly_fields=('last_login',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Staff,StaffAd)


