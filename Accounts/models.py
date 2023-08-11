from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser)
from django.core.validators import MaxValueValidator
from django_fields import DefaultStaticImageField
# Create your models here.



class UserAccountManager(BaseUserManager):
	def create_user(self , email , password = None):
		if not email or len(email) <= 0 :
			raise ValueError("Email field is required !")
		if not password :
			raise ValueError("Password is must !")
		
		user = self.model(
			email = self.normalize_email(email) ,
		)
		user.set_password(password)
		user.save(using = self._db)
		return user
	
	def create_superuser(self , email , password):
		user = self.create_user(
			email = self.normalize_email(email) ,
			password = password
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using = self._db)
		return user
	
class UserAccount(AbstractBaseUser):
    class Types(models.TextChoices):
        CLINIC = "CLINIC" , "clinic"
        STAFF = "STAFF" , "staff"
                
        
        DOCTOR="DOCTOR","doctor"
        
    class gender(models.TextChoices):
        Male = "Male", "male"
        Female = "Female", "female"
    image_and_logo=DefaultStaticImageField(upload_to="images_and_logo",default_image_path='images/blank.png',blank=True)
    type = models.CharField(max_length = 8 , choices = Types.choices ,
                            # Default is user is teacher
                            default = Types.CLINIC)
    email = models.EmailField(max_length = 200 , unique = True)
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    clinic_Name=models.CharField(max_length=50,default="")
    is_doctor = models.BooleanField(default = False)   
    is_clinic = models.BooleanField(default = False)
    Owner_First_Name=models.CharField(max_length=25,default='')
    Owner_Last_Name=models.CharField(max_length=25,default='')
    first_Name=models.CharField(max_length=25,default='')
    last_Name=models.CharField(max_length=25,default='')
    designation=models.TextField(default='')
    experience=models.PositiveIntegerField(validators=[MaxValueValidator(99)],default=0)
    qualification=models.TextField(default='')
    specialist=models.TextField(default='')
    contact=models.CharField(max_length=10)
    Block=models.BooleanField(default=False)
    map=models.CharField(default="",max_length=100)
    Address=models.TextField(default="")
    DOB=models.DateField(blank=True,null=True)
    gender=models.CharField(max_length=8,choices=gender.choices,default=gender.Male)
    staff=models.ForeignKey('Staff',on_delete=models.DO_NOTHING,blank=True,null=True,related_name='User_accounts_staff')
    clinic=models.ForeignKey('Clinic',on_delete=models.DO_NOTHING,blank=True,null=True,related_name='User_accounts_clinic')
    
    USERNAME_FIELD = "email"
    
    # defining the manager for the UserAccount model
    objects = UserAccountManager()
    
    def __str__(self):
        return str(self.email)
    
    def has_perm(self , perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self , app_label):
        return True
    
    def save(self , *args , **kwargs):
        if not self.type or self.type == None :
            self.type = UserAccount.Types.TEACHER
        return super().save(*args , **kwargs)




class ClinicManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email  = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = UserAccount.Types.CLINIC)
        return queryset    



class Clinic(UserAccount):
    class Meta : 
        proxy = True
    objects = ClinicManager()
      
    def save(self , *args , **kwargs):
        self.type = UserAccount.Types.CLINIC
        self.is_clinic = True
        return super().save(*args , **kwargs)
    
    def __str__(self):
        return str(self.clinic_Name)
      
class StaffManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
        
    def get_queryset(self , *args , **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = UserAccount.Types.STAFF)
        return queryset
      
class Staff(UserAccount):
    class Meta :
        proxy = True
    objects = StaffManager()
      
    def save(self  , *args , **kwargs):
        self.type = UserAccount.Types.STAFF
        self.is_staff = True
        return super().save(*args , **kwargs)


class DoctotManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email  = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = UserAccount.Types.DOCTOR)
        return queryset    



class Doctor(UserAccount):
    class Meta : 
        proxy = True
    objects = DoctotManager()
      
    def save(self , *args , **kwargs):
        self.type = UserAccount.Types.DOCTOR
        self.is_doctor = True
        return super().save(*args , **kwargs)
    
    def __str__(self):
        return str(self.first_Name)


