"""
URL configuration for Bus_Reservation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Bus_app.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Bus_Resarvation/Email_Registration/',Email_RegisterView.as_view(),name='Email_Signup'),
    path('Bus_Resarvation/Email_Login/',Email_LoginView.as_view(),name='Email_Login'),
    path('bus_resarvation/Email_Otp_Verify/',Email_OtpVerifyView.as_view(),name='Email_otp_verify'),
    path('',HomeView.as_view(),name='Home'), 
    path('bus_resarvation/Logout/',LogoutView.as_view(),name='logout'),

    path('Bus_Resarvation/Phone_Registration/',Phone_RegisterView.as_view(),name='Phone_Signup'), 
    path('Bus_Resarvation/Otp_Verify/',Phone_Otp_Verify_View.as_view(),name='phone_otp_verify'),
    path('Bus_Resarvation/Phone_Login/',Phone_LoginView.as_view(),name='Phone_Login'),
   
    path('Bus_Resarvation/Email_Password_Forgot/',Email_Forgot_PasswordView.as_view(),name='Email_Forgot_password'),
    path('Bus_Resarvation/Email_Password_Forgot_OTP_Verfiy/',Email_Forgot_Password_verifyView.as_view(),name='Email_Password_OTP_verfy'),
    path('bus_resarvation/Email_Password_Reset/',Email_Password_ResetView.as_view(),name='Email_Reset_Password'),

    path('Bus_Resarvation/Phone_password_Forgot/',Phone_Forget_PasswordView.as_view(),name="Phone_Reset_Password"),
    path('bus_reservation/phone_password_otp_verify/',Phone_Password_OTP_VerifyView.as_view(),name='Phone_Password_Verify'),
    path('Bus_Reservation/Phone_Password_Reset/',Phone_Password_ResetView.as_view(),name='Phone_Password_Reset'),

    path('Bus_Reservation/Profile/',ProfileView.as_view(),name='profile'), 

    path('Bus_Reservation/Bus_Route/',Bus_RouteView.as_view(),name="Bus_Route"), 
    path('Bus_Reservation/bus_route_list/',Bus_Route_ListView.as_view(),name="Bus_Route_List"),############# !!!!!!!!!!!
    path('bus_reservation/Bus_Route_Details/<int:pk>/',Bus_Route_DetailsView.as_view(),name="Bus_Route_Details"),
    path('bus_reservation/Bus_Route_Update/<int:pk>/',Bus_Route_UpdateView.as_view(),name="Bus_Route_Update"),########## !!!!!!!!!!!!1
    path('bus_reservation/bus_route_delete/<int:pk>/',Route_DeleteView.as_view(),name='route_delete'),#!!!!!!!!!!!!!!!!!!!!
    
    path('bus_reservation/bus/',Bus_Register_view.as_view(),name='bus'),#########....................
    path('bus_reservation/bus_update/<int:pk>/',Bus_Update_View.as_view(),name='bus_update'),##########................
    path('bus_reservation/bus_list/',Bus_List_View.as_view(),name='Bus_list'), ############..................
    path('bus_reservation/bus_details/<int:pk>/',Bus_Detail_View.as_view(),name='bus_details'), ################................
    path('bus_reservation/bus_delete/<int:pk>/',Bus_DeleteView.as_view(),name='delete_bus'), ################...................

    # path('bus_reservation/bus_booking/',Bus_BookingView.as_view(),name='booking'), ################
    
    path('bus_reservation/seats/<int:pk>/',Bus_SeatsView.as_view(),name='seats') ,############# ...........
    path('bus_reservation/booking_details/',Booking_DetailsView.as_view(),name='booked'),###########.............

    path('bus_reservation/booking_cancelition/<int:pk>/',Booking_CancelitionView.as_view(),name='booking_cancelition'),#..................

    path('bus_reservation/review/<int:pk>/',Review_View.as_view(),name='review'),############### bus_list@@@@@@@@
    path('bus_reservation/review_details/<int:pk>/',Review_DetailsView.as_view(),name='review_details'),########### @@@@@@@@@
    path('bus_reservation/review_delete/<int:pk>/',Review_DeleteView.as_view(),name='review_delete'),############## @@@@@@@@@
    path('bus_reservatio/razorpay_payment/',Razorpay_PaymentView.as_view(),name='razorpay_payment'),############
    path('bus_reservation/payment_sucess/',Payment_successView.as_view(),name='payment_success'), ############
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)