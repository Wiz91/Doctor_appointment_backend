from django.shortcuts import render
from rest_framework import viewsets,status,mixins,generics
from .serializers import DocRegisterSerializer,Staff_registrationSerializer,ClnicloginSerializer,ClniupSerializer,DocterupSerializer,StaffupSerializer,doctordelSerializer,ClniViewsSerializer,doctorviewSerializer,StaffviewupSerializer,ClinicSelfSerializer,doctorSelfSerializer,StaffSelfSerializer,DashboardSerializer
from .models import UserAccount,Clinic,Doctor,Staff
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from appointment.models import appointments,patient_information,doc_non_availability,medicine
from smtpUtile import Util
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination


from rest_framework.authentication import TokenAuthentication

class IgnoreBearerTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Check if the "Authorization" header is present in the request
        if 'Authorization' in request.headers:
            # Get the value of the "Authorization" header
            auth_header = request.headers['Authorization']

            # If the header starts with "Bearer", ignore it and return None for authentication
            if auth_header.startswith('Bearer'):
                return None

        # Return the result of the super method, even if it's None
        return super().authenticate(request)


       
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }




# Create your views here.
class Doc_Registartion_API(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes=[IsAuthenticated]
    serializer_class=DocRegisterSerializer
    @swagger_auto_schema()
    def post(self, request,format=None):
        serializer = DocRegisterSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token=get_tokens_for_user(user)
            cli_name=request.user.clinic_Name
            if request.user.type=="STAFF":
                cli_name=request.user.clinic.clinic_Name
            data={
                 'email_subject':"Doctor registered",
                 'body': "Dr "+ request.data['first_Name']+" "+request.data['last_Name']+ " " +"You'r registering with"+" "+ cli_name +". We are excited to have you join our team of esteemed doctors.",
                 'to_email': request.data['email']
            }
            Util.send_email(data)
            return Response({'status': status.HTTP_200_OK,'message':'Registration Successful','data':{"Token":token}},status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST,'message':serializer.errors,'data':{}}, status=status.HTTP_400_BAD_REQUEST)
    

class Staff_Registartion_API(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes=[IsAuthenticated]
    serializer_class=Staff_registrationSerializer
    def post(self, request,format=None):
        serializer = Staff_registrationSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token=get_tokens_for_user(user)
            return Response({'status': status.HTTP_201_CREATED,'message':'Registration Successful','data':{"Token":token}},status=status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_400_BAD_REQUEST,'message':serializer.errors,'data':{}}, status=status.HTTP_400_BAD_REQUEST)



# login views


class ClinicLoginView(GenericAPIView):
   serializer_class=ClnicloginSerializer
   authentication_classes = [IgnoreBearerTokenAuthentication]
   def post(self,request,format=None):
      serializer=ClnicloginSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
         email=serializer.data.get('email')
         password=serializer.data.get('password')
         try:
            user_obj=UserAccount.objects.get(email=email)
         except:
            return Response({'status': status.HTTP_404_NOT_FOUND,'message':'Please Registerd user first','data':{}}, status=status.HTTP_404_NOT_FOUND)
         if user_obj.Block==True:
            return Response({'status': status.HTTP_401_UNAUTHORIZED,'message':'Clinic is blocked','data':{}}, status=status.HTTP_401_UNAUTHORIZED)             
         user=authenticate(email=email,password=password)
         if user is not None:
            # print(user.image_and_logo)
            token=get_tokens_for_user(user)
            if user.type=="CLINIC":
                detial_dict={"Owner_First_Name":user.Owner_First_Name,"Owner_Last_Name":user.Owner_Last_Name,"Address":user.Address,"contact":user.contact,"email":user.email,"clinic_Name":user.clinic_Name,"image_and_logo":'/media/'+str(user.image_and_logo),"map":user.map}
            elif user.type=="STAFF":
                detial_dict={"first_Name":user.first_Name,"last_Name":user.last_Name,"Address":user.Address,"contact":user.contact,"email":user.email,"clinic_Name":user.clinic.clinic_Name,"image_and_logo":'/media/'+str(user.image_and_logo),"map":user.clinic.map}
            else:
                detial_dict={"first_Name":user.first_Name,"last_Name":user.last_Name,"Address":user.Address,"contact":user.contact,"email":user.email,"clinic_info":{"clinic_Name":user.clinic.clinic_Name,"contact":user.clinic.contact,"Address":user.clinic.Address,"logo":'/media/'+str(user.clinic.image_and_logo)},"designation":user.designation,"experience":user.experience,"qualification":user.qualification,"specialist":user.specialist,"image_and_logo":'/media/'+str(user.image_and_logo)}
            return Response({'status': status.HTTP_200_OK,'message':'Login Success','data':{"type":user.type,"Token":token,"user_details":detial_dict}},status=status.HTTP_200_OK)
         else:
             return Response({'status': status.HTTP_404_NOT_FOUND,'message':'Email or password is not Valid','data':{}}, status=status.HTTP_404_NOT_FOUND)
            
         

# #Accounts update


class clinic_update(GenericAPIView,mixins.UpdateModelMixin):
   permission_classes=[IsAuthenticated]
   serializer_class =ClniupSerializer
   def put(self,request,*args,**kwargs):
      chk=request.user.Block
      if chk == True:
            return Response({'status': status.HTTP_403_FORBIDDEN,'message':'Plez contect Wiz 91','data':{}}, status=status.HTTP_403_FORBIDDEN)
      user = Clinic.objects.get(id=self.request.user.id)
      serializer = self.serializer_class(instance=user, data=request.data,context={'user':request.user})
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({'status': status.HTTP_200_OK,'message':'updated','data':serializer.data}, status=status.HTTP_200_OK)
     
  

class Doctor_update(GenericAPIView,mixins.UpdateModelMixin):
   parser_classes = [MultiPartParser, FormParser]
   permission_classes=[IsAuthenticated]
   serializer_class =DocterupSerializer
   def put(self,request,*args,**kwargs):
      user_id=self.request.user.id
      if request.user.type =="CLINIC" or request.user.type=="STAFF":
        if request.data.get('id') == None:
            return Response({'status': status.HTTP_404_NOT_FOUND,'message':'You are the clinic profile "id" parameter is missing','data':{}}, status=status.HTTP_404_NOT_FOUND)  
        user_id=request.data['id']   
      try:
        user = Doctor.objects.get(id=user_id)
      except:
        return Response({'status': status.HTTP_404_NOT_FOUND,'message':'please add the staff first','data':{}}, status=status.HTTP_404_NOT_FOUND) 
      serializer = self.serializer_class(instance=user, data=request.data,context={'user':request.user,'user_obj':user})
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({'status': status.HTTP_200_OK,'message':'updated','data':serializer.data}, status=status.HTTP_200_OK)
  

class Staff_update(GenericAPIView,mixins.UpdateModelMixin):
   parser_classes = [MultiPartParser, FormParser]
   permission_classes=[IsAuthenticated]
   serializer_class =StaffupSerializer
   def put(self,request,*args,**kwargs):
      user_id=self.request.user.id
      if request.user.type =="CLINIC":
        if request.data.get('id') == None:
            return Response({'status': status.HTTP_404_NOT_FOUND,'message':'You are the clinic profile "id" parameter is missing','data':{}}, status=status.HTTP_404_NOT_FOUND)  
        user_id=request.data['id']   
      try:
        user = Staff.objects.get(id=user_id)
      except:
        return Response({'status': status.HTTP_404_NOT_FOUND,'message':'please add the staff first','data':{}}, status=status.HTTP_404_NOT_FOUND) 
      serializer = self.serializer_class(instance=user, data=request.data,context={'user_obj':user,'user':request.user})
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({'status': status.HTTP_200_OK,'message':'staff_updated','data':serializer.data}, status=status.HTTP_200_OK)


#view
class Doctor_account_views(GenericAPIView,mixins.RetrieveModelMixin):
    queryset=Doctor.objects.all()
    serializer_class=doctorviewSerializer
    permission_classes=[IsAuthenticated]  
    def get(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data,context={'user':request.user})                                  
        chk_avilable=Doctor.objects.filter(id=kwargs['pk'])
        a=self.retrieve(self,request,*args,**kwargs)
        if chk_avilable.exists():
            doc_obj=Doctor.objects.select_related().get(id=kwargs['pk'])
            if request.user.type=="CLINIC":
                if doc_obj.clinic.id==request.user.id or request.user.Block != True:
                    return Response({'status': status.HTTP_200_OK,'message':'ok','data':a.data}, status=status.HTTP_200_OK)
                return Response({'status': status.HTTP_401_UNAUTHORIZED,'message':'doctor not belong you','data':{}}, status=status.HTTP_401_UNAUTHORIZED)
            if request.user.type=="DOCTOR" or request.user.type=="STAFF":
                if doc_obj.clinic.id==request.user.clinic.id or request.user.clinic.Block!=True:
                    return Response({'status': status.HTTP_200_OK,'message':'ok','data':a.data}, status=status.HTTP_200_OK)
                return Response({'status': status.HTTP_401_UNAUTHORIZED,'message':'doctor not belong you','data':{}}, status=status.HTTP_401_UNAUTHORIZED)
            
            
class Doctor_all_account_views(generics.ListAPIView):
    serializer_class=doctorviewSerializer
    permission_classes=[IsAuthenticated]
    pagination_class = LimitOffsetPagination
    def get(self,request,*args,**kwargs):
        cli_id=request.user.id
        chk_blk=request.user.Block
        if request.user.type=="STAFF":
            cli_id=request.user.clinic.id
            chk_blk=request.user.clinic.Block
        if request.user.is_doctor == True or chk_blk==True: 
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block or not a clnic or staff profile','data':{}}, status=status.HTTP_403_FORBIDDEN)
        doc_obj=Doctor.objects.filter(clinic=cli_id).values("id","email", "first_Name","last_Name","contact","DOB","gender","Address","designation","experience","qualification","specialist","image_and_logo")
        print(doc_obj)
        paginator = self.pagination_class()
        paginated_obj_list = paginator.paginate_queryset(doc_obj, self.request)
        serializer = self.serializer_class(paginated_obj_list, many=True)
        paginated_response=paginator.get_paginated_response(serializer.data)
        print(paginated_response.data)
        response_dict = {
                'status': status.HTTP_200_OK,
                'message':"ok",
                'data': paginated_response.data,
            }
        return Response(response_dict, status=status.HTTP_200_OK)
        


class Staff_account_views(GenericAPIView,mixins.RetrieveModelMixin):
    queryset=Staff.objects.all()
    serializer_class=StaffviewupSerializer
    permission_classes=[IsAuthenticated]  
    def get(self,request,*args,**kwargs):
        chk_avilable=Staff.objects.filter(id=kwargs['pk'])
        if chk_avilable.exists():
            staff_obj=Staff.objects.select_related().get(id=kwargs['pk'])
            if staff_obj.clinic.id==request.user.id:
                if request.user.is_doctor == True or request.user.Block==True: 
                    return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block or not a clnic profile','data':''}, status=status.HTTP_403_FORBIDDEN)
                return Response({'status': status.HTTP_200_OK,'message':'retrived','data':self.retrieve(self,request,*args,**kwargs)}, status=status.HTTP_200_OK)
                # return self.retrieve(self,request,*args,**kwargs)
            return Response({'status': status.HTTP_403_FORBIDDEN,'message':'staff not belong you','data':{}}, status=status.HTTP_403_FORBIDDEN)
    
class Staff_all_account_views(generics.ListAPIView):    
    serializer_class=StaffviewupSerializer
    permission_classes=[IsAuthenticated]
    pagination_class = LimitOffsetPagination
    def get(self,request,*args,**kwargs):
        if request.user.is_doctor == True or request.user.Block==True: 
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block or not a clnic profile','data':{}}, status=status.HTTP_403_FORBIDDEN)
        doc_obj=Staff.objects.filter(clinic=request.user.id).values()
        paginator = self.pagination_class()
        paginated_obj_list = paginator.paginate_queryset(doc_obj, self.request)
        serializer = self.serializer_class(paginated_obj_list, many=True)
        paginated_response=paginator.get_paginated_response(serializer.data)
        response_dict = {
                'status': status.HTTP_200_OK,
                'message':"ok",
                'data': paginated_response.data,
            }
        return Response(response_dict, status=status.HTTP_200_OK)
        # return Response({'status': status.HTTP_200_OK,'message':'ok','data':doc_obj}, status=status.HTTP_200_OK)
    
    
#Delete

class doctor_delete(GenericAPIView,mixins.DestroyModelMixin):
    permission_classes=[IsAuthenticated]
    queryset=Doctor.objects.all()
    def delete(self,request,*args,**kwargs):
        chk_avilable=Doctor.objects.filter(id=kwargs['pk'])
        cli_id=request.user.id
        cli_blk=request.user.Block
        if request.user.type=="STAFF":
            cli_id=request.user.clinic.id
            cli_blk=request.user.Block
        if chk_avilable.exists():
            doc_obj=Doctor.objects.select_related().get(id=kwargs['pk'])
            if doc_obj.clinic.id==cli_id:
                if request.user.is_doctor == True or cli_blk==True:  
                    return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block or not a clnic profile','data':{}}, status=status.HTTP_403_FORBIDDEN)
                appondelete=appointments.objects.filter(doctor=kwargs['pk'])
                appondelete.delete()
                nonavidel=doc_non_availability.objects.filter(doctor=kwargs['pk'])
                nonavidel.delete()
                del_item=self.destroy(self,request,*args,**kwargs)
                return Response({'status': status.HTTP_204_NO_CONTENT,'message':'sucessfully_deleted','data':{str(del_item)}}, status=status.HTTP_204_NO_CONTENT)
            return Response({'status': status.HTTP_401_UNAUTHORIZED,'message':'doctor not belong you','data':{}}, status=status.HTTP_401_UNAUTHORIZED)   
        return Response({'status': status.HTTP_404_NOT_FOUND,'message':'Not Found','data':{}}, status=status.HTTP_404_NOT_FOUND)                       
       

class staff_delete(GenericAPIView,mixins.DestroyModelMixin):
    permission_classes=[IsAuthenticated]
    queryset=Staff.objects.all()
    def delete(self,request,*args,**kwargs):
        chk_avilable=Staff.objects.filter(id=kwargs['pk'])
        if chk_avilable.exists():
            staf_obj=Staff.objects.select_related().get(id=kwargs['pk'])
            if staf_obj.clinic.id==request.user.id:
                if request.user.is_doctor == True or request.user.Block==True:  
                    return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block or not a clnic profile','data':{}}, status=status.HTTP_403_FORBIDDEN)
                del_item=self.destroy(self,request,*args,**kwargs)
                return Response ({'status': status.HTTP_204_NO_CONTENT,'message':'sucessfully_deleted','data':{str(del_item)}}, status=status.HTTP_204_NO_CONTENT)
            return Response({'status': status.HTTP_401_UNAUTHORIZED,'message':'staff not belong you','data':{}}, status=status.HTTP_401_UNAUTHORIZED)                        
        return Response({'status': status.HTTP_404_NOT_FOUND,'message':'Not Found','data':{}}, status=status.HTTP_404_NOT_FOUND)
    
    
class doctor_self_view(GenericAPIView,mixins.RetrieveModelMixin):
    permission_classes=[IsAuthenticated]
    serializer_class=doctorSelfSerializer
    def get(self,request,*args,**kwargs):
        if request.user.type!="DOCTOR" or request.user.clinic.Block==True:
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block or not a doctor profile','data':{}}, status=status.HTTP_403_FORBIDDEN)
        user = Doctor.objects.filter(id=self.request.user.id).values("id","email","first_Name","last_Name","Address","contact","specialist","qualification","experience","designation","clinic_id","type","image_and_logo")
        return Response({'status': status.HTTP_200_OK,'message':'ok','data':user[0]}, status=status.HTTP_200_OK)
    
class clinic_self_view(GenericAPIView,mixins.RetrieveModelMixin):
    permission_classes=[IsAuthenticated]
    serializer_class=ClinicSelfSerializer
    def get(self,request,*args,**kwargs):
        if request.user.type!="CLINIC" or request.user.Block==True:
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block or not a clinic profile','data':{}}, status=status.HTTP_403_FORBIDDEN)
        user = Clinic.objects.filter(id=self.request.user.id).values("id","email","Owner_First_Name","Owner_Last_Name","Address","contact","map","type","clinic_Name","image_and_logo")
        return Response({'status': status.HTTP_200_OK,'message':'ok','data':user[0]}, status=status.HTTP_200_OK)
    
class staff_self_view(GenericAPIView,mixins.RetrieveModelMixin):
    permission_classes=[IsAuthenticated]
    serializer_class=StaffSelfSerializer
    def get(self,request,*args,**kwargs):
        if request.user.type!="STAFF" or request.user.Block==True:
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block or not a Staff profile','data':{}}, status=status.HTTP_403_FORBIDDEN)
        user = Staff.objects.filter(id=self.request.user.id).values("id","email","first_Name","last_Name","Address","contact","type","image_and_logo")
        return Response({'status': status.HTTP_200_OK,'message':'ok','data':user[0]}, status=status.HTTP_200_OK)
    

class DashboardData(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=DashboardSerializer
    def get(self,request,*args,**kwargs):
        cli_id=request.user.id
        cli_blk=request.user.Block
        if request.user.type=="STAFF":
            cli_id=request.user.clinic.id
            cli_blk=request.user.clinic.Block
        if request.user.is_doctor == True or cli_blk==True:  
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block or not a clnic profile','data':{}}, status=status.HTTP_403_FORBIDDEN)
        total_patients=patient_information.objects.filter(clinc=cli_id).count()
        total_appointments=appointments.objects.filter(clinc=cli_id).count()
        total_doctors=Doctor.objects.filter(clinic=cli_id).count()
        total_staff=Staff.objects.filter(clinic=cli_id).count()
        Dashboard_data=[{"total_patients":total_patients,"total_appointments":total_appointments,"total_doctors":total_doctors,"total_staff":total_staff}]
        return Response({'status': status.HTTP_200_OK,'message':'ok','data':Dashboard_data}, status=status.HTTP_200_OK)
    


