from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets,status,mixins,generics
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from .serializers import addpatient_infoSerializer,view_all_patientSerializer,add_appointmentSerializer,view_appointmentSerializer,patientupSerializer,add_doc_non_availabilitySerializer,view_all_non_availability_datesSerializers,add_medicineSerializer,view_all_medicineSerializers
from rest_framework.response import Response
from Accounts.models import Clinic,UserAccount,Doctor,Staff
from .models import doc_non_availability,appointments,patient_information,medicine
from .TimeFun import time_converet_AM_PM
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination


class add_patient(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=addpatient_infoSerializer
    def post(self, request,format=None):
        serializer = addpatient_infoSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'status': status.HTTP_200_OK,'message':'added','data':serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST,'message':serializer.errors,'data':{}}, status=status.HTTP_400_BAD_REQUEST)
    
    
class add_doc_non_availability(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=add_doc_non_availabilitySerializer
    def post(self,request,*args,**kwargs):
        # print(kwargs['pk'])
        serializer=add_doc_non_availabilitySerializer(data=request.data, context={'user':request.user,'doc_id':kwargs['pk']})
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({'status': status.HTTP_200_OK,'message':'added','data':serializer.data}, status=status.HTTP_200_OK)
        

    
class view_all_patient(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=view_all_patientSerializer
    pagination_class = LimitOffsetPagination
    def get(self,request,*args,**kwargs):
        cli_id=request.user.id
        cli_blk=request.user.Block
        if request.user.type=="STAFF":
            cli_id=request.user.clinic.id
            cli_blk=request.user.clinic.Block
        if request.user.is_doctor == True or cli_blk==True:  
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block or not a clnic profile','data':{}}, status=status.HTTP_403_FORBIDDEN)
        doc_obj=patient_information.objects.filter(clinc=cli_id).values()
        paginator = self.pagination_class()
        paginated_obj_list = paginator.paginate_queryset(doc_obj, self.request)
        serializer = self.serializer_class(paginated_obj_list, many=True)
        paginated_response=paginator.get_paginated_response(serializer.data)
        response_dict = {
            'status': status.HTTP_200_OK,
            'message':"ok",
            'data': paginated_response.data,
            # 'count': paginated_response.data['count'],
            # 'next': paginated_response.data['next'],
            # 'previous': paginated_response.data['previous'],
        }
        return Response(response_dict, status=status.HTTP_200_OK)
        # return Response({'status': status.HTTP_200_OK,'message':'ok','data':doc_obj}, status=status.HTTP_200_OK)
    
    
class add_appoitment(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=add_appointmentSerializer
    def post(self,request,*args,**kwargs):
        serializer=add_appointmentSerializer(data=request.data, context={'user':request.user,'doc_id':kwargs['pk']})
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({'status': status.HTTP_200_OK,'message':'added','data':serializer.data}, status=status.HTTP_200_OK)
        

# class viewall_appointments(generics.ListAPIView):
#     permission_classes=[IsAuthenticated]
#     serializer_class=view_appointmentSerializer
#     def get(self,request,*args,**kwargs):
#         userblk=request.user.Block
#         user=request.user.id
#         if request.user.type=="DOCTOR":
#             return Response ({'status': status.HTTP_403_FORBIDDEN,'message':"You the doctor profile you can't see all appointment of other doctor",'data':{}}, status=status.HTTP_403_FORBIDDEN)
#         if request.user.type=="STAFF":
#             userblk=request.user.clinic.Block
#             user=request.user.clinic.id
#         if userblk==True: 
#             return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block.','data':{}}, status=status.HTTP_403_FORBIDDEN)
#         doc_obj=appointments.objects.filter(clinc=user).values("id")
#         if doc_obj.exists():
#             obj_list=[]
#             for i in doc_obj:
#                 appObj=appointments.objects.select_related().get(id=i['id'])
#                 addby=UserAccount.objects.get(id=appObj.add_by.id)
#                 abby_list=[appObj.add_by.id,addby.Owner_First_Name+" "+addby.Owner_Last_Name]
#                 if addby.type=="STAFF":
#                     abby_list=[appObj.add_by.id,addby.first_Name+" "+addby.last_Name]
#                 obj_list.append({"add_by":abby_list,"date_of_creation":appObj.date_of_creation,"doctor":[appObj.doctor.id,appObj.doctor.first_Name+" "+appObj.doctor.last_Name],"patient":[appObj.patient_id.id,appObj.patient_id.patient_First_Name+" "+appObj.patient_id.patient_Last_Name],"slot":{"date":appObj.date_of_appointment,"slote_no":appObj.slots}})
#                 print(appObj.patient_id.id)
#             return Response({'status': status.HTTP_200_OK,'message':'ok','data':obj_list}, status=status.HTTP_200_OK)
#         return Response ({'status': status.HTTP_404_NOT_FOUND,'message':'No appointments available','data':{}}, status=status.HTTP_404_NOT_FOUND)



# class CustomPagination(PageNumberPagination):
#     def get_paginated_response(self, data):
#         return Response({
#             'count': self.page.paginator.count,
#             'next': self.get_next_link(),
#             'previous': self.get_previous_link(),
#             'results': data,
#             'custom_field': 'Custom Value'  # Add any additional custom fields you want
#         })

# class viewall_appointments(generics.ListAPIView):
#     queryset = appointments.objects.all()
#     serializer_class = view_appointmentSerializer
#     pagination_class = LimitOffsetPagination
    

class viewall_appointments(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = view_appointmentSerializer
    pagination_class = LimitOffsetPagination
    # page_size = 10  # Number of items per page
    # max_page_size = 100  # Maximum number of items per page
 
    def get(self,request,*args,**kwargs):   
        userblk=request.user.Block
        user=request.user.id
        if request.user.type=="DOCTOR":
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':"You the doctor profile you can't see all appointment of other doctor",'data':{}}, status=status.HTTP_403_FORBIDDEN)
        if request.user.type=="STAFF":
            userblk=request.user.clinic.Block
            user=request.user.clinic.id
        if userblk==True: 
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block.','data':{}}, status=status.HTTP_403_FORBIDDEN)
        doc_obj=appointments.objects.filter(clinc=user).values("id")
        if doc_obj.exists():
            obj_list=[]
            for i in doc_obj:
                appObj=appointments.objects.select_related().get(id=i['id'])
                addby=UserAccount.objects.get(id=appObj.add_by.id)
                abby_list=[appObj.add_by.id,addby.Owner_First_Name+" "+addby.Owner_Last_Name]
                if addby.type=="STAFF":
                    abby_list=[appObj.add_by.id,addby.first_Name+" "+addby.last_Name]
                obj_list.append({"id":appObj.id,"add_by":abby_list,"date_of_creation":appObj.date_of_creation,"doctor":[appObj.doctor.id,appObj.doctor.first_Name+" "+appObj.doctor.last_Name],"patient":[appObj.patient_id.id,appObj.patient_id.patient_First_Name+" "+appObj.patient_id.patient_Last_Name],"slot":{"date":appObj.date_of_appointment,"slote_no":appObj.slots}})
            print(obj_list)
            paginator = self.pagination_class()
            paginated_obj_list = paginator.paginate_queryset(obj_list, self.request)
            serializer = self.serializer_class(paginated_obj_list, many=True)
            paginated_response=paginator.get_paginated_response(serializer.data)
            response_dict = {
                'status': status.HTTP_200_OK,
                'message':"ok",
                'data': paginated_response.data,
                # 'count': paginated_response.data['count'],
                # 'next': paginated_response.data['next'],
                # 'previous': paginated_response.data['previous'],
            }
            return Response(response_dict,status=status.HTTP_200_OK)
        return Response ({'status': status.HTTP_200_OK,'message':'No appointments available','data':{"count": "0", "next": "null", "previous": "null", "results": []}}, status=status.HTTP_200_OK)
       
       
class doctor_patient_appoiment_list(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        if request.user.type!="DOCTOR":
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':"You not doctor profile you can't doctor self appointment of other doctor",'data':{}}, status=status.HTTP_403_FORBIDDEN)
        patient_list=[]
        a=appointments.objects.filter(doctor_id=request.user.id).values("id")
        for i in a:
            appoi_obj=appointments.objects.select_related().get(id=i['id'])
            adb=[appoi_obj.add_by.first_Name+" "+appoi_obj.add_by.last_Name,appoi_obj.add_by.id]
            if appoi_obj.add_by.type=="CLINIC":
                adb=[appoi_obj.add_by.Owner_First_Name+" "+appoi_obj.add_by.Owner_Last_Name,appoi_obj.add_by.id]
            patient_list.append({"date_of_creation":appoi_obj.date_of_creation,"date_of_appointment":appoi_obj.date_of_appointment,"clinic":[appoi_obj.clinc.Owner_First_Name+" "+appoi_obj.clinc.Owner_Last_Name,appoi_obj.clinc.id],"addby":adb,"Patient":{"patient_First_Name":appoi_obj.patient_id.patient_First_Name+" "+appoi_obj.patient_id.patient_Last_Name,"contect":appoi_obj.patient_id.contect,"gender":appoi_obj.patient_id.gender,"address":appoi_obj.patient_id.address,"id":appoi_obj.patient_id.id,"patient_DOB":appoi_obj.patient_id.DOB,"weight":appoi_obj.patient_id.weight},"slots":appoi_obj.slots,"close":appoi_obj.close})
        return Response({'status': status.HTTP_200_OK,'message':"ok",'data':patient_list}, status=status.HTTP_200_OK)
    
    
class patient_update(GenericAPIView,mixins.UpdateModelMixin):
   permission_classes=[IsAuthenticated]
   serializer_class =patientupSerializer
   def put(self,request,*args,**kwargs):
      try:
        patient_obj = patient_information.objects.get(id=kwargs['pk'])
      except:
        return Response ({'status': status.HTTP_404_NOT_FOUND,'message':'patient not found','data':{}}, status=status.HTTP_404_NOT_FOUND)  
      serializer = self.serializer_class(instance=patient_obj, data=request.data,context={'patient_obj':patient_obj,'user':request.user})
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({'status': status.HTTP_200_OK,'message':'staff_updated','data':serializer.data}, status=status.HTTP_200_OK)
    
    
class view_all_non_availability_dates(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=view_all_non_availability_datesSerializers
    pagination_class = LimitOffsetPagination
    def get(self,request,*args,**kwargs):
        cli=request.user.id
        chk_blk=request.user.Block
        if request.user.type=="STAFF":
            chk_blk=request.user.clinic.Block
            cli=request.user.clinic.id
        if request.user.type=="DOCTOR":
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':"the doctor profile can't see all non availability's of all doctor",'data':{}}, status=status.HTTP_403_FORBIDDEN)
        if chk_blk==True:  
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block','data':{}}, status=status.HTTP_403_FORBIDDEN)
        doc_non_obj=doc_non_availability.objects.filter(clinic=cli).values("id")
        don_non_list=[]
        for i in doc_non_obj:
            obj=doc_non_availability.objects.select_related().get(id=i['id'])
            don_non_list.append({"id":obj.id,"date_of_creation":obj.date_of_creation,"doctor_non_availability_date":obj.doctor_non_availability_date,"doctor":[obj.doctor.id,obj.doctor.first_Name+" "+obj.doctor.last_Name],"clinic":[obj.clinic.id,obj.clinic.clinic_Name],"slots":eval(obj.slots)})
        paginator = self.pagination_class()
        print(don_non_list)
        paginated_obj_list = paginator.paginate_queryset(don_non_list, self.request)
        serializer = self.serializer_class(paginated_obj_list, many=True)
        paginated_response=paginator.get_paginated_response(serializer.data)
        response_dict = {
            'status': status.HTTP_200_OK,
            'message':"ok",
            'data': paginated_response.data,
            # 'count': paginated_response.data['count'],
            # 'next': paginated_response.data['next'],
            # 'previous': paginated_response.data['previous'],
        }
        return Response(response_dict, status=status.HTTP_200_OK)  
        # return Response({'status': status.HTTP_200_OK,'message':'ok','data':don_non_list}, status=status.HTTP_200_OK)
    
    
    
class doc_non_availability_delete(GenericAPIView,mixins.DestroyModelMixin):
    permission_classes=[IsAuthenticated]
    queryset=doc_non_availability.objects.all()
    def delete(self,request,*args,**kwargs):
        cli_id=request.user.id
        if request.user.type=="STAFF" or request.user.type=="DOCTOR":
            cli_id=request.user.clinic.id           
        chk_avilable=doc_non_availability.objects.filter(id=kwargs['pk'])
        if chk_avilable.exists():
            doc_non_obj=doc_non_availability.objects.select_related().get(id=kwargs['pk'])
            if request.user.type == "DOCTOR":
                if doc_non_obj.doctor.id!=request.user.id:
                    return Response ({'status': status.HTTP_401_UNAUTHORIZED,'message':"the non availability not belong's to you",'data':{}}, status=status.HTTP_401_UNAUTHORIZED) 
            if cli_id!=doc_non_obj.clinic.id:
                 return Response({'status': status.HTTP_401_UNAUTHORIZED,'message':'doctor not belong you','data':{}}, status=status.HTTP_401_UNAUTHORIZED) 
            del_item=self.destroy(self,request,*args,**kwargs)
            return Response ({'status': status.HTTP_204_NO_CONTENT,'message':'sucessfully_deleted','data':{str(del_item)}}, status=status.HTTP_204_NO_CONTENT)                       
        return Response({'status': status.HTTP_404_NOT_FOUND,'message':'Not Found','data':{}}, status=status.HTTP_404_NOT_FOUND)
    
    
class Doctor_non_availability_views(GenericAPIView,mixins.RetrieveModelMixin):
    queryset=doc_non_availability.objects.all()
    serializer_class=view_all_non_availability_datesSerializers
    permission_classes=[IsAuthenticated]  
    def get(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data,context={'user':request.user})                                  
        chk_avilable=doc_non_availability.objects.filter(id=kwargs['pk'])
        a=self.retrieve(self,request,*args,**kwargs)
        user_blk=request.user.Block
        cli_id=request.user.id
        if request.user.type=="STAFF" or request.user.type=="DOCTOR":
            user_blk=request.user.clinic.Block
            cli_id=request.user.clinic.id
        if user_blk==True:
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block','data':{}}, status=status.HTTP_403_FORBIDDEN)
        if chk_avilable.exists():
            non_avi_obj=doc_non_availability.objects.select_related().get(id=kwargs['pk'])
            if non_avi_obj.clinic.id!=cli_id:
                return Response({'status': status.HTTP_401_UNAUTHORIZED,'message':'doctor not belong you','data':{}}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'status': status.HTTP_200_OK,'message':'ok','data':a.data}, status=status.HTTP_200_OK)
      

class add_medicine(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=add_medicineSerializer
    def post(self,request,*args,**kwargs):
        serializer=add_medicineSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({'status': status.HTTP_200_OK,'message':'added','data':serializer.data}, status=status.HTTP_200_OK)
        

class doctor_self_patient(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        if request.user.type!="DOCTOR":
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':"You not doctor profile you can't see his patients",'data':{}}, status=status.HTTP_403_FORBIDDEN)
        patient_list=[]
        single_patient=[]
        a=appointments.objects.filter(doctor_id=request.user.id).values("id","patient_id")
        for i in a:
            if i['patient_id'] not in single_patient:
                single_patient.append(i['patient_id'])
        for j in single_patient:
            appoi_obj=patient_information.objects.select_related().get(id=j)
            patient_list.append({"id":appoi_obj.id,"patient_First_Name":appoi_obj.patient_First_Name,"patient_Last_Name":appoi_obj.patient_Last_Name,"contect":appoi_obj.contect,"gender":appoi_obj.gender,"address":appoi_obj.address,"DOB":appoi_obj.DOB,"medical_Conditions":appoi_obj.medical_Conditions,"past_Surgeries_or_Hospitalizations":appoi_obj.past_Surgeries_or_Hospitalizations,"known_allergies":appoi_obj.known_allergies,"currently_medications_or_supplements":appoi_obj.currently_medications_or_supplements,"current_Symptoms_or_issue":appoi_obj.current_Symptoms_or_issue,"current_symptoms_started":appoi_obj.current_symptoms_started,"current_symptoms_detail":appoi_obj.current_symptoms_detail,"smokeing_or_tobacco_or_alcohol":appoi_obj.smokeing_or_tobacco_or_alcohol,"physically_Activety":appoi_obj.physically_Activety,"diet":appoi_obj.diet,"mental_Health":appoi_obj.mental_Health,"Immunization_History":appoi_obj.Immunization_History,"women_Health":appoi_obj.women_Health,"other_Health_Concerns":appoi_obj.other_Health_Concerns,"date_of_creation":appoi_obj.date_of_creation,"weight":appoi_obj.weight,"Clinic":[appoi_obj.clinc.id,appoi_obj.clinc.Owner_First_Name+" "+appoi_obj.clinc.Owner_Last_Name]})
        return Response({'status': status.HTTP_200_OK,'message':"ok",'data':patient_list}, status=status.HTTP_200_OK)       
        
        

class viewall_medicine(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=view_all_medicineSerializers
    pagination_class = LimitOffsetPagination
    def get(self,request,*args,**kwargs):
        cli=request.user.id
        chk_blk=request.user.Block
        if request.user.type=="STAFF" or request.user.type=="DOCTOR":
            chk_blk=request.user.clinic.Block
            cli=request.user.clinic.id
        if chk_blk==True:  
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'the profile is block','data':{}}, status=status.HTTP_403_FORBIDDEN)
        med_fil=medicine.objects.filter(clinic_id=cli).values("id")
        if med_fil.exists():
            medi_list=[]
            for i in med_fil:
                med_obj=medicine.objects.select_related().get(id=i['id'])
                medi_list.append({'id':med_obj.id,"name_of_medicine":med_obj.name_of_medicine,"manufacturer":med_obj.manufacturer,"strength":med_obj.strength,"formulation":med_obj.formulation,"drug_Class":med_obj.drug_Class,"date_of_creation":med_obj.date_of_creation,"clinic":[med_obj.clinic.id,med_obj.clinic.Owner_First_Name+" "+med_obj.clinic.Owner_Last_Name],"add_by":{"id":med_obj.add_by.id,"type":med_obj.add_by.type}})
                
                paginator = self.pagination_class()
                paginated_obj_list = paginator.paginate_queryset(medi_list, self.request)
                serializer = self.serializer_class(paginated_obj_list, many=True)
                paginated_response=paginator.get_paginated_response(serializer.data)
                response_dict = {
                'status': status.HTTP_200_OK,
                'message':"ok",
                'data': paginated_response.data,
                # 'count': paginated_response.data['count'],
                # 'next': paginated_response.data['next'],
                # 'previous': paginated_response.data['previous'],
                }
            return Response(response_dict, status=status.HTTP_200_OK)
        return Response ({'status': status.HTTP_200_OK,'message':'No appointments available','data':{"count": "0", "next": "null", "previous": "null", "results": []}}, status=status.HTTP_200_OK)
        

class Doctor_DashboardData(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        if request.user.type!="DOCTOR":
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':"You are not doctor profile you can't see his Dashboard Data",'data':{}}, status=status.HTTP_403_FORBIDDEN)
        Doctor_total_appointments=appointments.objects.filter(doctor_id=request.user.id).count()
        no_off_patient=[]
        a=appointments.objects.filter(doctor_id=request.user.id).values("id",'patient_id')
        for i in a:
            if i['patient_id'] not in no_off_patient:
                no_off_patient.append(i['patient_id'])
        print(len(no_off_patient))
        return Response({'status': status.HTTP_200_OK,'message':'ok','data':[{"Doctor_total_appointments":Doctor_total_appointments,"total_No_of_patient_of_doctor":len(no_off_patient)}]}, status=status.HTTP_200_OK)
    
    
