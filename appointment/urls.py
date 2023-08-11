from django.urls import path
from .import views

urlpatterns = [
    path('add/patient',views.add_patient.as_view()),
    path('add/doctor/non-availability/<str:pk>',views.add_doc_non_availability.as_view()),
    path('view-all/patient',views.view_all_patient.as_view()),
    path('add/appointment/<str:pk>',views.add_appoitment.as_view()),
    path('view-all/appointments',views.viewall_appointments.as_view()),
    path('view/doctor-self/appointments',views.doctor_patient_appoiment_list.as_view()),
    path('update/patient/<str:pk>',views.patient_update.as_view()),
    path('view-all/doctor/non-availability',views.view_all_non_availability_dates.as_view()),
    path('delete/doctor/non-availability/<str:pk>',views.doc_non_availability_delete.as_view()),
    path('view/doctor/non-availability/<str:pk>',views.Doctor_non_availability_views.as_view()),
    path('add/medicine',views.add_medicine.as_view()),
    path('view-all/medicine',views.viewall_medicine.as_view()),
    path('view/doctor-self/patient',views.doctor_self_patient.as_view()),
    path('doctor/deshbord-data',views.Doctor_DashboardData.as_view()),
    # path('add/prescription',views.add_prescription.as_view()),
]