from rest_framework import serializers
from .models import patient_information,doc_non_availability,appointments,medicine
from Accounts.models import UserAccount,Doctor,Staff,Clinic
from rest_framework import status
from django.conf import settings
from datetime import datetime
from .TimeFun import time_converet_AM_PM
from smtpUtile import Util
from twilio.rest import Client
    
class addpatient_infoSerializer(serializers.ModelSerializer):
    patient_First_Name=serializers.CharField(max_length=25)
    patient_Last_Name=serializers.CharField(max_length=25)
    contect=serializers.CharField(max_length=10)
    DOB=serializers.DateField()
    gender=serializers.CharField(default="Male")
    weight=serializers.CharField(max_length=5,default="")
    address=serializers.CharField(style={'base_template': 'textarea.html'},default="")
    medical_Conditions=serializers.CharField(style={'base_template': 'textarea.html'},default="")
    past_Surgeries_or_Hospitalizations=serializers.CharField(style={'base_template': 'textarea.html'},default="")
    known_allergies=serializers.CharField(style={'base_template': 'textarea.html'},default="")
    currently_medications_or_supplements=serializers.CharField(style={'base_template': 'textarea.html'},default="")
    current_Symptoms_or_issue=serializers.CharField(style={'base_template': 'textarea.html'},default="")
    current_symptoms_started=serializers.DateField(default=None)
    current_symptoms_detail=serializers.CharField(style={'base_template': 'textarea.html'},default="")
    smokeing_or_tobacco_or_alcohol=serializers.BooleanField(default=False)
    physically_Activety=serializers.CharField(style={'base_template': 'textarea.html'},default="")
    diet=serializers.CharField(style={'base_template': 'textarea.html'},default="")
    mental_Health=serializers.CharField(style={'base_template': 'textarea.html'},default="")
    Immunization_History=serializers.CharField(style={'base_template': 'textarea.html'},default="")
    women_Health=serializers.CharField(style={'base_template': 'textarea.html'},default="")
    other_Health_Concerns=serializers.CharField(style={'base_template': 'textarea.html'},default="")
    class Meta:
        model = patient_information
        fields = ['patient_First_Name','patient_Last_Name','contect','gender','address','medical_Conditions','past_Surgeries_or_Hospitalizations','known_allergies','currently_medications_or_supplements','current_Symptoms_or_issue','current_symptoms_detail','smokeing_or_tobacco_or_alcohol','physically_Activety','diet','mental_Health','Immunization_History','women_Health','other_Health_Concerns','DOB','current_symptoms_started','weight']

    def validate(self, attrs):
        user=self.context.get('user')
        if user.Block==True:
            raise serializers.ValidationError("You are block plez contect wiz 91")
        elif user.is_doctor==True:
            raise serializers.ValidationError("You are not clinic or staff profile") 
        return attrs
    
    def create(self, validated_data):
        user=self.context.get('user')
        if user.type=="STAFF":
            cli_id=Clinic.objects.get(id=user.clinic.id)
            return patient_information.objects.create(patient_First_Name=self.validated_data['patient_First_Name'],patient_Last_Name=self.validated_data['patient_Last_Name'],contect=self.validated_data['contect'],gender=self.validated_data['gender'],address=self.validated_data['address'],medical_Conditions=self.validated_data['medical_Conditions'],past_Surgeries_or_Hospitalizations=self.validated_data['past_Surgeries_or_Hospitalizations'],known_allergies=self.validated_data['known_allergies'],currently_medications_or_supplements=self.validated_data['currently_medications_or_supplements'],current_Symptoms_or_issue=self.validated_data['current_Symptoms_or_issue'],current_symptoms_detail=self.validated_data['current_symptoms_detail'],smokeing_or_tobacco_or_alcohol=self.validated_data['smokeing_or_tobacco_or_alcohol'],physically_Activety=self.validated_data['physically_Activety'],diet=self.validated_data['mental_Health'],mental_Health=self.validated_data['mental_Health'],Immunization_History=self.validated_data['Immunization_History'],women_Health=self.validated_data['women_Health'],other_Health_Concerns=self.validated_data['other_Health_Concerns'],DOB=self.validated_data['DOB'],current_symptoms_started=self.validated_data['current_symptoms_started'],weight=self.validated_data['weight'],clinc=cli_id,staff=user)
        return patient_information.objects.create(patient_First_Name=self.validated_data['patient_First_Name'],patient_Last_Name=self.validated_data['patient_Last_Name'],contect=self.validated_data['contect'],gender=self.validated_data['gender'],address=self.validated_data['address'],medical_Conditions=self.validated_data['medical_Conditions'],past_Surgeries_or_Hospitalizations=self.validated_data['past_Surgeries_or_Hospitalizations'],known_allergies=self.validated_data['known_allergies'],currently_medications_or_supplements=self.validated_data['currently_medications_or_supplements'],current_Symptoms_or_issue=self.validated_data['current_Symptoms_or_issue'],current_symptoms_detail=self.validated_data['current_symptoms_detail'],smokeing_or_tobacco_or_alcohol=self.validated_data['smokeing_or_tobacco_or_alcohol'],physically_Activety=self.validated_data['physically_Activety'],diet=self.validated_data['mental_Health'],mental_Health=self.validated_data['mental_Health'],Immunization_History=self.validated_data['Immunization_History'],women_Health=self.validated_data['women_Health'],other_Health_Concerns=self.validated_data['other_Health_Concerns'],DOB=self.validated_data['DOB'],current_symptoms_started=self.validated_data['current_symptoms_started'],weight=self.validated_data['weight'],clinc=user)
    
    
class add_doc_non_availabilitySerializer(serializers.ModelSerializer):
    slots=serializers.ListField(child=serializers.CharField())
    class Meta:
        model=doc_non_availability
        fields= ['doctor_non_availability_date','slots']
        
    def validate(self, attrs):
        user=self.context.get('user')
        doc_id=self.context.get('doc_id')
        doc_avi_date=attrs.get('doctor_non_availability_date')
        cli=user.id
        doc=doc_id
        blk_chk=user.Block
        if user.type=="STAFF":
            cli=user.clinic.id
            blk_chk=user.clinic.Block
        if user.type=="DOCTOR":
            cli=user.clinic.id
            doc=user.id
            blk_chk=user.clinic.Block
        chk_doc=doc_non_availability.objects.filter(clinic=cli,doctor_id=doc,doctor_non_availability_date=doc_avi_date).values()
        if chk_doc.exists():  
            raise serializers.ValidationError('that doctor with that date already added')   
        if blk_chk==True:
            raise serializers.ValidationError("You are block plez contect wiz 91")
        try:
            do_obj=Doctor.objects.get(id=doc)
            if do_obj.clinic.id != cli:
                raise serializers.ValidationError("that doctor is not belongs to you")   
        except:
            raise serializers.ValidationError("that doctor is not exists")
        return attrs
    
    def create(self, validated_data):
        user=self.context.get('user')
        doc_id=self.context.get('doc_id')
        doc_id_no=doc_id
        clinic_obj=user
        stf=None
        if user.type=="STAFF":
            clinic_obj=Clinic.objects.get(id=user.clinic.id)
            stf=user
        doc_obj=Doctor.objects.get(id=doc_id_no) 
        if user.type=="DOCTOR":
            clinic_obj=Clinic.objects.get(id=user.clinic.id)
            doc_obj=user
        return doc_non_availability.objects.create(doctor_non_availability_date=self.validated_data['doctor_non_availability_date'],doctor=doc_obj,clinic=clinic_obj,slots=self.validated_data['slots'],staff=stf)
        
        
class view_all_patientSerializer(serializers.ModelSerializer):
    class Meta:
        model=patient_information
        fields= ['id','patient_First_Name','patient_Last_Name','contect','gender','address','medical_Conditions','past_Surgeries_or_Hospitalizations','known_allergies','currently_medications_or_supplements','current_Symptoms_or_issue','current_symptoms_detail','smokeing_or_tobacco_or_alcohol','physically_Activety','diet','mental_Health','Immunization_History','women_Health','other_Health_Concerns','DOB','current_symptoms_started','weight','date_of_creation']     
        
        
class view_doc_non_availabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model=doc_non_availability
        fields= ['doctor_availability_date','in_time','out_time']
        
        

class add_appointmentSerializer(serializers.ModelSerializer):
    patient_id=serializers.IntegerField()
    slots=serializers.TimeField(format='%I:%M %p')
    class Meta:
        model=appointments
        fields=["patient_id","slots","date_of_appointment"]
        
    def validate(self, attrs):
        user=self.context.get('user')
        doc_id=self.context.get('doc_id')
        Slots=attrs.get('slots') 
        pat_id=attrs.get('patient_id')
        app_date=attrs.get('date_of_appointment')
        cli_id=user.id
        cli_blk=user.Block
        if user.type=="STAFF":
            cli_blk=user.clinic.Block
            cli_id=user.clinic.id
        chk_date=doc_non_availability.objects.filter(doctor_non_availability_date=app_date,doctor_id=doc_id,clinic=cli_id).values("doctor_non_availability_date","slots")
        if chk_date.exists():
            un_avi_list=eval(chk_date[0]["slots"])
            if time_converet_AM_PM(str(Slots)) in un_avi_list:
                raise serializers.ValidationError("the date or slots not available")
        chk_patient=patient_information.objects.filter(id=pat_id).values("clinc_id")
        if cli_blk==True:
            raise serializers.ValidationError("You are block plez contect wiz 91")
        if chk_patient.exists():
            if chk_patient[0]["clinc_id"]!=cli_id:
                raise serializers.ValidationError("this patient not belong's to you")
        else:
            raise serializers.ValidationError("plz add patient first")
        chk_doc=Doctor.objects.filter(id=doc_id).values("clinic_id")
        if chk_doc.exists():
            if chk_doc[0]["clinic_id"]!=cli_id:
                raise serializers.ValidationError("this Doctor not belong's to you")
        else:
            raise serializers.ValidationError("plz reg doctor first")
        chk_pat_with_same_doc=appointments.objects.filter(patient_id=pat_id,doctor_id=doc_id,date_of_appointment=app_date)
        if chk_pat_with_same_doc.exists():
            raise serializers.ValidationError("this patient has an appoiment on with same doctor")
        chk_pat_with_same_date_and_slots=appointments.objects.filter(patient_id=pat_id,date_of_appointment=app_date,slots=Slots)
        if chk_pat_with_same_date_and_slots.exists():
            raise serializers.ValidationError("this patient has an appoiment with other doctor on same date & slots")
        chk_patient_appointment=appointments.objects.filter(clinc_id=cli_id,doctor_id=doc_id,date_of_appointment=app_date,slots=Slots)
        if chk_patient_appointment.exists():
            raise serializers.ValidationError("this patient has an appoiment on"+" "+str(app_date))
        return attrs
    
    
    def create(self, validated_data):
        user=self.context.get('user')
        doc_id=self.context.get('doc_id')
        cli=user
        if user.type == "STAFF":
            cli=Clinic.objects.get(id=user.clinic_id)
        doc=Doctor.objects.get(id=doc_id)
        patient_obj=patient_information.objects.get(id=self.validated_data['patient_id'])
        app_obj=appointments.objects.create(add_by=user,slots=self.validated_data['slots'],patient_id=patient_obj,clinc=cli,doctor=doc,date_of_appointment=self.validated_data['date_of_appointment'])
        app_obj.save()
        
        # msg="We are pleased to inform you that your appointment with Dr."+ doc.first_Name + " "+ doc.last_Name +" has been successfully booked. \n Appointment Details: \n Date:"+str(self.validated_data['date_of_appointment']) +"\n Time:"+ time_converet_AM_PM(str(self.validated_data['slots'])) +"\n Location:"+cli.Address
        
        # doc_msg="we are pleased to inform you that you have an appointment with the patient "+patient_obj.patient_First_Name+" "+patient_obj.patient_Last_Name +"\n Appointmet Details \n Date:"+ str(self.validated_data['date_of_appointment']) + "\n Time:"+time_converet_AM_PM(str(self.validated_data['slots']))
        
        # account_sid = "AC5eee2943fe98822ac5efffc9cdc3d63d"
        # auth_token  = "c2175382593e3ae86de28cd4b8326694"

        # client = Client(account_sid, auth_token)
        # message = client.messages.create(
        #     to="+91"+patient_obj.contect,
        #     from_="+14846235992",
        #     body=msg)  
        
        # client2 = Client(account_sid, auth_token)
        # doctor_message = client2.messages.create(
        #     to="+91"+doc.contact,
        #     from_="+14846235992",
        #     body=doc_msg)  
        # to="+919165165814",
        return validated_data
    


class view_appointmentSerializer(serializers.ModelSerializer):
    patient=serializers.ListField(child=serializers.CharField())
    slot=serializers.DictField(child=serializers.CharField())
    add_by=serializers.ListField(child=serializers.CharField())
    doctor=serializers.ListField(child=serializers.CharField())
    class Meta:
        model=appointments        
        fields= ['id','add_by','date_of_creation','patient','slot','doctor']
        
        
# class view_appointmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=appointments        
#         fields= ['id','add_by','date_of_creation','patient_id','slots']
                
        
class patientupSerializer(serializers.ModelSerializer):
    class Meta:
        model=patient_information
        fields=['patient_First_Name','patient_Last_Name','contect','gender','address','medical_Conditions','past_Surgeries_or_Hospitalizations','known_allergies','currently_medications_or_supplements','current_Symptoms_or_issue','current_symptoms_detail','smokeing_or_tobacco_or_alcohol','physically_Activety','diet','mental_Health','Immunization_History','women_Health','other_Health_Concerns','DOB','current_symptoms_started','weight']

    def validate(self, attrs):
        patient_obj=self.context.get('patient_obj')
        user=self.context.get('user')
        user_id=user.id
        if user.type=="STAFF":
            user_id=user.clinic.id
        if user_id!=patient_obj.clinc.id:
            raise serializers.ValidationError("Patient not belong to you")     
        if patient_obj.clinc.Block==True:
            raise serializers.ValidationError("Clinic is block please contect Wiz 91")
        return attrs
    
    
    
class view_all_non_availability_datesSerializers(serializers.ModelSerializer):
    doctor=serializers.ListField(child=serializers.CharField())
    clinic=serializers.ListField(child=serializers.CharField())
    slots=serializers.ListField(child=serializers.CharField())
    class Meta:
        model=doc_non_availability
        fields= ['id','doctor','clinic','slots','doctor_non_availability_date','date_of_creation']   
        
        
        
class add_medicineSerializer(serializers.ModelSerializer):
    class Meta:
        model=medicine
        fields=["name_of_medicine","manufacturer","strength","formulation","drug_Class"]
        
    def validate(self, attrs):
        user=self.context.get('user')
        chk_blk=user.Block
        if user.type=="STAFF" or user.type=="DOCTOR":
            chk_blk=user.clinic.Block
        if chk_blk==True:
            raise serializers.ValidationError("Clinic is block please contect Wiz 91")
        return attrs
       
    def create(self, validated_data):
        user=self.context.get('user')
        cli_obj=user
        if user.type=="STAFF" or user.type=="DOCTOR":
            cli_obj=Clinic.objects.get(id=user.clinic.id)
        app_obj=medicine.objects.create(name_of_medicine=self.validated_data['name_of_medicine'],manufacturer=self.validated_data['manufacturer'],strength=self.validated_data['strength'],formulation=self.validated_data['formulation'],drug_Class=self.validated_data['drug_Class'],clinic=cli_obj,add_by=user)
        app_obj.save()
        return validated_data

class view_all_medicineSerializers(serializers.ModelSerializer):
    clinic=serializers.ListField(child=serializers.CharField())
    add_by=serializers.DictField(child=serializers.CharField())
    class Meta:
        model=medicine
        fields= ['id','name_of_medicine','manufacturer','formulation','strength','drug_Class','date_of_creation','clinic',"add_by"]   
   
    
# class add_prescriptionSerializer(serializers.ModelSerializer):
#     medicines_arrey=serializers.ListField(child=serializers.IntegerField())
#     appointment_id=serializers.IntegerField()
#     class Meta:
#         model=prescription
#         fields=["medicines_arrey","appointment_id"]
        
#     def validate(self, attrs):
#         return attrs
       
#     def create(self, validated_data):
#         user=self.context.get('user')
#         medicines=self.validated_data['medicines_arrey']
#         appointment_id=self.validated_data['appointment_id']
#         return validated_data