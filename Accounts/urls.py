from django.urls import path
from .import views

urlpatterns = [
    path('doctor/registration',views.Doc_Registartion_API.as_view()),
    path('staff/registration',views.Staff_Registartion_API.as_view()),
    path('login',views.ClinicLoginView.as_view()),
    path('clinic-update/information',views.clinic_update.as_view()),
    path('doctor-update/information',views.Doctor_update.as_view()),
    path('staff-update/information',views.Staff_update.as_view()),
    path('doctor-delete/<str:pk>',views.doctor_delete.as_view()),
    path('staff-delete/<str:pk>',views.staff_delete.as_view()),
    path('view/doctor/<str:pk>',views.Doctor_account_views.as_view()),
    path('view-all/doctor',views.Doctor_all_account_views.as_view()),
    path('view/staff/<str:pk>',views.Staff_account_views.as_view()),
    path('view-all/staff',views.Staff_all_account_views.as_view()),
    path('view-self/doctor',views.doctor_self_view.as_view()),
    path('view-self/clinic',views.clinic_self_view.as_view()),
    path('view-self/staff',views.staff_self_view.as_view()),
    path('view/dashboard-data',views.DashboardData.as_view()),
]





