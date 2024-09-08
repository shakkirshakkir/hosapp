from django.urls import path
from .views import *

urlpatterns=[
    path('abo/',About,name="about"),
    path('hom/',Home,name="home"),
    path('con/',Contact,name="contact"),
    path('alog/',Login,name="login"),
    path('logo/',Logout,name="logout"),
    path('aind/',Index,name="index"),
    path('vdoc/',ViewDoctor,name="viewdoctor"),
    path('ddoc(?p<int:pid>)/',DeleteDoctor,name="deletedoctor"),
    path('adoc/',AddDoctor,name="adddoctor"),
    path('vpat/',ViewPatient,name="viewpatient"),
    path('dpat(?p<int:pid>)/',DeletePatient,name="deletepatient"),
    path('apat/',AddPatient,name="addpatient"),
    path('vapp/',ViewAppointment,name="viewappointment"),
    path('dapp(?p<int:pid>)/',DeleteAppointment,name="deleteappointment"),
    path('aapp/',AddAppointment,name="addappointment"),
    path('add-appointment-request/',add_appointment_request, name='add_appointment_request'),
    path('appointment-request-success/',appointment_request_success, name='appointment_request_success'),
    path('user/login/', user_login, name='user_login'),
    path('register/',register, name='register'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('appointment/request/<int:request_id>/create-payment/',create_payment, name='create_payment'),

    path('appointment/request/<int:request_id>/execute-payment/',execute_payment, name='execute_payment'),
    path('payment/cancelled/',payment_cancelled, name='payment_cancelled'),
    path('appointment/request/<int:request_id>/approve/',approve_appointment_request, name='approve_appointment_request'),
    path('appointment/request/<int:request_id>/',appointment_request_detail, name='appointment_request_detail'),
    # path('payment/',payment, name='payment'),
    path('charge/',charge, name='charge'),
    path('payment/',process_payment, name='process_payment'),
    path('payment/success/',payment_success, name='payment_success'),
    path('payment/error/',payment_error, name='payment_error'),








    # other URLs







]