from django.db import models
from Accounts.models import Clinic,Staff,Doctor,UserAccount

# Create your models here.



class patient_information(models.Model):
    class gender(models.TextChoices):
        Male = "Male", "male"
        Female = "Female", "female"
    
    
    patient_First_Name=models.CharField(max_length=25)
    patient_Last_Name=models.CharField(max_length=25)
    clinc=models.ForeignKey(Clinic,on_delete=models.DO_NOTHING,related_name='appointment_patient_clinic')
    staff=models.ForeignKey(Staff,on_delete=models.DO_NOTHING,blank=True,null=True,related_name='appointment_patient_staff')
    contect=models.CharField(max_length=10)
    date_of_creation=models.DateTimeField(auto_now_add=True)
    gender=models.CharField(max_length=8,choices=gender.choices,default=gender.Male)
    address=models.TextField(default="")
    DOB=models.DateField()
    medical_Conditions=models.TextField(default="")
    past_Surgeries_or_Hospitalizations=models.TextField(default="") 
    known_allergies=models.TextField(default="") 
    currently_medications_or_supplements=models.TextField(default="") 
    current_Symptoms_or_issue=models.TextField(default="") 
    current_symptoms_started=models.DateField(default=None,blank=True,null=True) 
    current_symptoms_detail=models.TextField(default="") 
    smokeing_or_tobacco_or_alcohol=models.BooleanField(default=False) 
    physically_Activety=models.TextField(default="") 
    diet=models.TextField(default="") 
    mental_Health=models.TextField(default="")
    Immunization_History=models.TextField(default="")
    women_Health=models.TextField(default="")
    other_Health_Concerns=models.TextField(default="")
    weight=models.CharField(max_length=5,default="")
    class Meta :
        db_table="patient_information"
   
   
   
class doc_non_availability(models.Model):
    date_of_creation=models.DateTimeField(auto_now_add=True)
    doctor_non_availability_date=models.DateField()
    doctor=models.ForeignKey(Doctor,on_delete=models.DO_NOTHING)
    clinic=models.ForeignKey(Clinic,on_delete=models.DO_NOTHING,related_name='doc_patient_clinic',blank=True,null=True)
    staff=models.ForeignKey(Staff,on_delete=models.DO_NOTHING,blank=True,null=True,related_name='doc_patient_staff')
    slots=models.TextField()
    closed=models.BooleanField(default=False)
    class Meta:     
        db_table="doc_non_availability"
        
        
        
class appointments(models.Model):
    choise=[
        ('10:00:00','10:00:00'),
        ('10:15:00','10:15:00'),
        ('10:30:00','10:30:00'),
        ('10:45:00','10:45:00'),
        ('11:00:00','11:00:00'),
        ('11:15:00','11:15:00'),
        ('11:30:00','11:30:00'),
        ('11:45:00','11:45:00'),
        ('12:00:00','12:00:00'),
        ('12:15:00','12:15:00'),
        ('12:30:00','12:30:00'),
        ('12:45:00','12:45:00'), 
        ('13:00:00','13:00:00'),
        ('13:15:00','13:15:00'),
        ('13:30:00','13:30:00'),
        ('13:45:00','13:45:00'),
        ('14:00:00','14:00:00'),
        ('14:15:00','14:15:00'),
        ('14:30:00','14:30:00'),
        ('14:45:00','14:45:00'), 
        ('15:00:00','15:00:00'),
        ('15:15:00','15:15:00'),
        ('15:30:00','15:30:00'),
        ('15:45:00','15:45:00'), 
        ('16:00:00','16:00:00'),
        ('16:15:00','16:15:00'),
        ('16:30:00','16:30:00'),
        ('16:45:00','16:45:00'), 
        ('17:00:00','17:00:00'),
        ('17:15:00','17:15:00'),
        ('17:30:00','17:30:00'), 
        ('17:45:00','17:45:00'), 
        ('18:00:00','18:00:00'),
        ('18:15:00','18:15:00'),
        ('18:30:00','18:30:00'),
        ('18:45:00','18:45:00')
        ]
    add_by=models.ForeignKey(UserAccount,on_delete=models.DO_NOTHING)
    clinc=models.ForeignKey(Clinic,on_delete=models.DO_NOTHING,related_name='app_patient_clinic',blank=True,null=True)
    doctor=models.ForeignKey(Doctor,on_delete=models.DO_NOTHING,related_name='patient_clinic')
    date_of_creation=models.DateTimeField(auto_now_add=True)
    date_of_appointment=models.DateField()
    patient_id=models.ForeignKey(patient_information,on_delete=models.DO_NOTHING)
    close=models.BooleanField(default=False)
    slots=models.TimeField(choices=choise)
    class Meta:
        db_table="appointments"
    

    
class medicine(models.Model):
    class Drug(models.TextChoices):
        Antibiotic = "Antibiotic", "antibiotic"
        Biotic = "Biotic", "biotic"
    
    class Formulation(models.TextChoices):
        Tablet = "tablet", "tablet"
        Capsule = "Capsule", "Capsule"
        Syrup = "Syrup", "syrup"
        Injection = "Injection", "injection"
    
    name_of_medicine=models.CharField(max_length=50)
    manufacturer=models.CharField(max_length=50)
    strength=models.CharField(max_length=6)
    formulation=models.CharField(choices=Formulation.choices,default=Formulation.Tablet,max_length=100)
    drug_Class=models.CharField(choices=Drug.choices,default=Drug.Antibiotic,max_length=100)
    clinic=models.ForeignKey(Clinic,on_delete=models.DO_NOTHING)
    add_by=models.ForeignKey(UserAccount,on_delete=models.DO_NOTHING,related_name='medicines')
    date_of_creation=models.DateField(auto_now_add=True)
    class Meta:
        db_table="medicine"
        
   
        
# class prescription(models.Model):
#     date_of_creation=models.DateField(auto_now_add=True)
#     medicines=models.ManyToManyField(medicine,through='extrafild_of_medicine')
#     appointment=models.ForeignKey(appointments, on_delete=models.DO_NOTHING)
#     clinic=models.ForeignKey(Clinic,on_delete=models.DO_NOTHING,related_name='prescription_clinic')
#     doctor=models.ForeignKey(Doctor,on_delete=models.DO_NOTHING,related_name='prescription_doctor')
#     class Meta:
#         db_table="prescription"
    
    
# class extrafild_of_medicine(models.Model):
#     medicine=models.ForeignKey(medicine,on_delete=models.DO_NOTHING)
#     prescription=models.ForeignKey(prescription,on_delete=models.DO_NOTHING)
#     frequency=models.CharField(max_length=30)
#     Duration=models.CharField(max_length=50)
#     Note=models.CharField(max_length=50)
#     class Meta:
#         db_table="extrafild_of_medicine" 
