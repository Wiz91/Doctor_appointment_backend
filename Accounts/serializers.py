from rest_framework import serializers,status
from rest_framework.validators import UniqueValidator
from .models import UserAccount,Clinic,Staff,Doctor
from django.contrib.auth.hashers import make_password
from appointment.models import patient_information,appointments


# Doc serializers registration



class DocRegisterSerializer(serializers.ModelSerializer):
    first_Name=serializers.CharField(max_length=25)
    last_Name=serializers.CharField(max_length=25)
    Address=serializers.CharField(max_length=100)
    DOB=serializers.DateField()
    gender=serializers.ChoiceField(choices=["Male","Female"])
    designation=serializers.CharField(max_length=100)
    experience=serializers.CharField(max_length=100)
    qualification=serializers.CharField(max_length=100)
    specialist=serializers.CharField(max_length=100)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    image_and_logo=serializers.ImageField(max_length=None, use_url=True,default="")
    class Meta:
        model = Doctor
        fields = ['email','contact','first_Name','last_Name','Address','DOB','image_and_logo','gender','designation','experience','qualification','specialist','password','password2']
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user=self.context.get('user')
        if user.type =="STAFF":
            if user.clinic.Block==True:
                raise serializers.ValidationError("You'r clinic is blocked")
        if user.is_doctor == True or user.Block == True:
            raise serializers.ValidationError("You are not clinic profile or you blocked")
        if password != password2:
            raise serializers.ValidationError("password and confirm password dosen't match")
        return attrs
    
    def create(self, validated_data):
        user=self.context.get('user')
        print(validated_data.get('image_and_logo'))
        if user.type == "STAFF":
            get_clinic_obj=Clinic.objects.get(id=user.clinic_id)
            return Doctor.objects.create(email=self.validated_data['email'],contact=self.validated_data['contact'],first_Name=self.validated_data['first_Name'],last_Name=self.validated_data['last_Name'],designation=self.validated_data['designation'],experience=self.validated_data['experience'],qualification=self.validated_data['qualification'],specialist=self.validated_data['specialist'],password=make_password(self.validated_data['password']),staff=user,clinic=get_clinic_obj,DOB=self.validated_data['DOB'],Address=self.validated_data['Address'],gender=self.validated_data['gender'],image_and_logo=validated_data.get('image_and_logo'))
        return Doctor.objects.create(email=self.validated_data['email'],contact=self.validated_data['contact'],first_Name=self.validated_data['first_Name'],last_Name=self.validated_data['last_Name'],designation=self.validated_data['designation'],experience=self.validated_data['experience'],qualification=self.validated_data['qualification'],specialist=self.validated_data['specialist'],password=make_password(self.validated_data['password']),clinic=user,DOB=self.validated_data['DOB'],Address=self.validated_data['Address'],gender=self.validated_data['gender'],image_and_logo=validated_data.get('image_and_logo'))
      


# staff serializers registration

class Staff_registrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    image_and_logo=serializers.ImageField(max_length=None, use_url=True,default="")
    class Meta:
        model = Staff
        fields = ['email','contact','first_Name','last_Name','password','password2','image_and_logo']
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user=self.context.get('user')
        if user.is_clinic != True:
            raise serializers.ValidationError("You are not clinic profile")
        if password != password2:
            raise serializers.ValidationError("password and confirm password dosen't match")
        return attrs
    
    def create(self, validated_data):
        user=self.context.get('user')
        if user.Block != True:
            return Staff.objects.create(email=self.validated_data['email'],contact=self.validated_data['contact'],first_Name=self.validated_data['first_Name'],last_Name=self.validated_data['last_Name'],image_and_logo=validated_data.get('image_and_logo'),password=make_password(self.validated_data['password']),clinic=user)
        raise serializers.ValidationError("Please contect to Wiz 91")

# logins

class ClnicloginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=UserAccount
        fields=['email','password']
        
 

#  Account update serializer


class ClniupSerializer(serializers.ModelSerializer):
    # image_and_logo=serializers.ImageField(max_length=None, use_url=True,required=False,default="")
    class Meta:
        model=Clinic
        fields=['email','contact','clinic_Name','Owner_First_Name','Owner_Last_Name','Address','map','image_and_logo']

    def validate(self, attrs):
        user=self.context.get('user')
        if user.is_clinic != True:
            raise serializers.ValidationError("You are not clinic profile")
        if user.Block != False:
            raise serializers.ValidationError("Please contect to Wiz 91")
        return attrs


class DocterupSerializer(serializers.ModelSerializer):
    id=serializers.ReadOnlyField()
    class Meta:
        model=Doctor
        fields=['id','email','contact','first_Name','last_Name','Address','DOB','gender','designation','experience','qualification','specialist','contact','image_and_logo']

    def validate(self, attrs):
        user_obj=self.context.get('user_obj')
        user=self.context.get('user')
        if user_obj.clinic.Block==True:
            raise serializers.ValidationError("Clinic is block please contect Wiz 91")
        if user.type=="CLINIC":
            if user.id!=user_obj.clinic_id:
                raise serializers.ValidationError("staff not belongs to you")
        return attrs
    

class StaffupSerializer(serializers.ModelSerializer):
    id=serializers.ReadOnlyField()
    class Meta:
        model=Staff
        fields=['id','email','contact','first_Name','last_Name','image_and_logo']

    def validate(self, attrs):
        user_obj=self.context.get('user_obj')
        user=self.context.get('user')
        if user_obj.clinic.Block==True:
            raise serializers.ValidationError("Clinic is block please contect Wiz 91")
        if user.type=="CLINIC":
            if user.id!=user_obj.clinic_id:
                raise serializers.ValidationError("staff not belongs to you")
        return attrs
    
#views
 

 
class ClniViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Clinic
        fields=['id','email','contact','clinic_Name','Owner_First_Name','Owner_Last_Name','Address','map']

    def validate(self, attrs):
        return attrs
 
class doctorviewSerializer(serializers.ModelSerializer):
    image_and_logo=serializers.URLField()
    class Meta:
        model=Doctor
        fields=['id','email','contact','first_Name','last_Name','Address','DOB','gender','designation','experience','qualification','specialist','contact','image_and_logo']
        
    def validate(self, attrs):
        return attrs 
    
    
 
class StaffviewupSerializer(serializers.ModelSerializer):
    image_and_logo=serializers.URLField()
    class Meta:
        model=Staff
        fields=['id','password','email','contact','first_Name','last_Name','image_and_logo']

    def validate(self, attrs):
        print("xyz")
        return attrs
 
 #delete   
class doctordelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctor
        fields=['email','contact','first_Name','last_Name','designation','experience','qualification','specialist','contact']

    def validate(self, attrs):
        return attrs
    
    
    def delete(self, validated_data):
        raise serializers.ValidationError("password and confirm password dosen't match")



class ClinicSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model=Clinic
        fields=["id","email","Owner_First_Name","Owner_Last_Name","Address","contact","map","type",'image_and_logo']

    def validate(self, attrs):
        return attrs
    
class doctorSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctor
        fields=["id","email","first_Name","last_Name","Address","contact","specialist","qualification","experience","designation","clinic_id","image_and_logo","type"]

    def validate(self, attrs):
        return attrs
    
class StaffSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model=Staff
        fields=["id","email","first_Name","last_Name","Address","contact","type","image_and_logo"]

    def validate(self, attrs):
        return attrs
    

class DashboardSerializer(serializers.ModelSerializer):
    total_appointments=serializers.IntegerField()
    total_patients=serializers.IntegerField()
    total_doctors=serializers.IntegerField()
    total_staff=serializers.IntegerField()
    class Meta:
        model=appointments
        fields= ["total_appointments","total_patients","total_doctors","total_staff"]     