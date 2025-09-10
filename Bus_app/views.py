
from django.shortcuts import render,redirect

from django.views.generic import View

from Bus_app.forms import *

from Bus_app.models import *

from django.core.mail import send_mail

from django.contrib.auth import authenticate,login,logout

from Bus_app.utils.sms import send_sms  

from django.http import JsonResponse #phone otp

from datetime import datetime,timedelta #time 

from django.http import HttpResponse

from django.db.models import Q

from django.contrib import messages

import random

from  django.conf import settings

    ###################### home ###########################

class HomeView(View):

    def get(self, request):
        source = request.GET.get('source')
        destination = request.GET.get('destination')
        available_date = request.GET.get('Available_date')
        selected_types = request.GET.getlist('bus_type')

        bus_types = ['AC', 'NONAC', 'SLEEPER', 'SEATER']
        buses = []

        if source and destination and available_date:
            routes = Route.objects.filter(
                source__iexact=source.strip(),
                destination__iexact=destination.strip(),
                Available_date=available_date
            )
            buses = Bus_Model.objects.filter(Route_Fk__in=routes)

            if selected_types:
                buses = buses.filter(Bus_Types__in=selected_types)

        return render(request, 'home.html', {
            'buses': buses,
            'source': source,
            'destination': destination,
            'available_date': available_date,
            'bus_types': bus_types,
            'selected_types': selected_types,
        })



# signup


class Email_RegisterView(View):

    def get(self,request):

        form=User_Email_RegisterForm

        return render(request,'Email_Signup.html',{'form':form})

    def post(self,request):

        form = User_Email_RegisterForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
           
            otp = random.randint(1000,9999)

            request.session['otp'] = otp
            request.session['username'] = username
            request.session['email'] = email 
            request.session['password'] = password

            mail = send_mail(subject="otp for registration",message= str(otp),from_email= settings.EMAIL_HOST_USER,recipient_list=[email])

            if mail:

                print("hello")
                print(otp)
            return redirect('Email_otp_verify')
        
        else:
            print(form.errors)

            return redirect("Email_Signup")

class Email_OtpVerifyView(View):

    def get(self,request):

        form =  Email_OtpVerifyForm

        return render(request,"Email_otp.html",{"form":form})

    def post(self,request):

        form = Email_OtpVerifyForm(request.POST)

        if form.is_valid():

            enterd_otp = form.cleaned_data.get('otp')

            if str(enterd_otp) == str(request.session.get('otp')):
   
                CustomUser.objects.create_user(username=request.session.get('username'),email=request.session.get('email'),
                password=request.session.get('password'))

                print(enterd_otp)
               

                return redirect("Email_Login")
                
        return redirect('Email_Signup')

class Email_LoginView(View):

    def get(self,request):

        form = LoginEmailForm

        return render(request,"Email_login.html",{"form":form})
    
    def post(self,request):

        form = LoginEmailForm(request.POST)

        if form.is_valid():

            user_email =form.cleaned_data.get('email')
           
            user = CustomUser.objects.get(email = user_email) 

            username = user.username

            password = form.cleaned_data.get('password')

            user_obj = authenticate(request,username=username,password = password)

            if user_obj:

                login(request,user_obj)

                return redirect("Home")
            
            form=LoginEmailForm

        return render(request,"Email_login.html",{"form":form})
    
class LogoutView(View):

    def get(self,request):

        logout(request)

        return redirect("Email_Login")

############  Phone_Registion ###############

class Phone_RegisterView(View):

    def get(self,request):

        form=User_Phone_Number_RegisterForm

        return render(request,'Phone_Signup.html',{'form':form})
    
    def post(self,request):

        form=User_Phone_Number_RegisterForm(request.POST)

        if form.is_valid():

            username=form.cleaned_data.get("username")

            phone_number=form.cleaned_data.get("phone_number")

            password=form.cleaned_data.get("password")

            otp=random.randint(10000,999999)

            request.session['otp']=otp

            request.session['username']=username

            request.session['phone_number']=phone_number

            request.session['password']=password

            # print(phone_number)

            sms=send_sms(message=f"otp verification {otp}",to_number=phone_number)

            if sms:

                print("SMS sent successfully")

                return redirect("phone_otp_verify")
        
            else:
    
                print('SMS failed to send')
    
                return redirect("Phone_Signup")

class Phone_Otp_Verify_View(View):

    def get(self,request):

        form=Phone_OtpVerifyForm

        return render(request, 'phone_otp.html', {'form': form})  

    def post(self,request):

        form=Phone_OtpVerifyForm(request.POST)

        if form.is_valid():

            enterd_otp = form.cleaned_data.get('otp')
    
            if str(enterd_otp) == str(request.session.get('otp')):

                CustomUser.objects.create_user(username=request.session.get('username'),phone_number= request.session.get('phone_number'),
                password=request.session.get('password'))

                print("sucessfully created")

                return redirect("Phone_Login")
        
        return redirect("Phone_Signup")


class Phone_LoginView(View):

    def get(self,request):

        form=Phone_LoginForm

        return render(request,'Phone_login.html',{'form':form})
    
    def post(self,request):

        form=Phone_LoginForm(request.POST)

        if form.is_valid():

            user_number=form.cleaned_data.get('phone_number')

            user=CustomUser.objects.get(phone_number=user_number)

            username=user.username

            password=form.cleaned_data.get('password')

            user_data=authenticate(request,username=username,password=password)

            if user_data:

                login(request,user_data)

                return redirect('Home')
            
        form=Phone_LoginForm
            
        return render(request,'Phone_login.html',{'form':form})
        

#############  Email_Password_Reset   ###################

class Email_Forgot_PasswordView(View):

    def get(self,request):

        form=Email_Forgot_PasswordForm

        return render(request,'Email_Forgot.html',{'form':form})
    
    def post(self,request):

        form=Email_Forgot_PasswordForm(request.POST)

        if form.is_valid():

            Email_id=form.cleaned_data.get('email')

            if Email_id:

                user_Email=CustomUser.objects.get(email=Email_id)

                otp=random.randint(1000,9999)

                request.session['otp']=otp

                request.session['email']=Email_id

                request.session['username']=user_Email.username

                print(otp)

                send_mail(subject='Password Reset OTP',message=str(otp),from_email=settings.EMAIL_HOST_USER,recipient_list=[Email_id])

                print("sucess")  

                return redirect('Email_Password_OTP_verfy')
        
        return redirect("Email_Signup")
        
class Email_Forgot_Password_verifyView(View):

    def get(self,request):

        form=Email_Forgot_Password_OTP_verifyForm

        return render(request,'Email_Forgot_OTP.html',{'form':form})
    
    def post(self,request):

        form=Email_Forgot_Password_OTP_verifyForm(request.POST)

        if form.is_valid():

            Enter_otp=form.cleaned_data.get('otp')

            generate_otp =request.session.get('otp')

            if int(Enter_otp) == int(generate_otp):
                print("correct")

                return redirect('Email_Reset_Password')
            
        return render(request,'Email_Forgot_OTP.html',{'form':form})
    
class Email_Password_ResetView(View):

    def get(self,request):

        form=Email_Password_ResetForm

        return render(request,'Email_Reset.html',{'form':form})
    
    def post(self,request):

        form=Email_Password_ResetForm(request.POST)

        if form.is_valid():

            user=CustomUser.objects.get(username=request.session.get('username'))

            New_password=form.cleaned_data.get('new_password')

            Confirm_password=form.cleaned_data.get('confirm_password')

            if New_password == Confirm_password:

                user.set_password(Confirm_password)

                user.save()

                return redirect("Email_Login")
            
            form=Email_Password_ResetForm

            return render(request,'Email_Reset.html',{'form':form})
        
######## phone password Reset View's ###########

class Phone_Forget_PasswordView(View):

    def get(self,request):

        form=Phone_Forgot_PasswordForm

        return render(request,'Phone_Forgot.html',{'form':form})
    
    def post(self,request):

        form=Phone_Forgot_PasswordForm(request.POST)

        if form.is_valid():

            phone_number=form.cleaned_data.get('phone_number')

            user=CustomUser.objects.get(phone_number=phone_number)

            otp=random.randint(1000,9999)

            request.session['otp']=otp

            request.session['phone_number']=phone_number

            request.session['username']=user.username

            send=send_sms(message=f'OTP Verify for Forgot Password{str(otp)}',to_number=phone_number)

            return redirect("Phone_Password_Verify")
        
        form=Phone_Forgot_PasswordForm

        print("not sucesses")
        
        return render(request,'Phone_Forgot.html',{'form':form})
    

class Phone_Password_OTP_VerifyView(View):

    def get(self,request):

        form=Phone_Forgot_Password_OTP_verifyForm

        return render(request,'Phone_Forgot_Otp.html',{'form':form})
    
    def post(self,request):

        form=Phone_Forgot_Password_OTP_verifyForm(request.POST)

        if form.is_valid():

            otp=form.cleaned_data.get('otp')

            generate_otp=request.session.get('otp')

            if int(otp) == int(generate_otp):

                return redirect("Phone_Password_Reset")
            
            return redirect("Phone_Reset_Password")
        
class Phone_Password_ResetView(View):

    def get(self,request):

        form=Phone_Password_ResetForm

        return render(request,'Phone_Password_Reset.html',{'form':form})
    
    def post(self,request):

        form=Phone_Password_ResetForm(request.POST)

        if form.is_valid():

            user=CustomUser.objects.get(username=request.session.get('username'))

            New_password=form.cleaned_data.get('new_password')

            Confirm_password=form.cleaned_data.get('confirm_password')

            if New_password == Confirm_password:

                user.set_password(Confirm_password)

                user.save()

                return redirect('Phone_Login')
            
        form=Phone_Password_ResetForm

        return render(request,'Phone_Password_Reset.html',{'form':form})
    
######### profile view #############

class ProfileView(View):

    def get(self,request):
        
        data=CustomUser.objects.get(id=request.user.id)

        return render(request,'Profile.html',{'data':data})

    def post(self, request):
        
        user = CustomUser.objects.get(id=request.user.id)

        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.gender = request.POST.get('gender')
        user.age =request.POST.get('age')
        user.dob = request.POST.get('dob')

        if request.FILES.get('image'):

            user.image = request.FILES.get('image')

        user.save()

        return redirect('profile')                
    #request.FILES >> If you don’t include request.FILES in forms with file uploads, the file fields will be ignored, and the uploaded files won’t be saved.
    #html must we gives <form action="#" method="post" enctype="multipart/form-data"> >> enctype >> it helps to form image file data to valide sending 
    #request.FILES – contains uploaded file data (like profile images).

# setting image

class Bus_RouteView(View):

    def get(self,request):

        form =Bus_RouteForm

        return render(request,'Bus_route.html',{'form':form})
    
    def post(self,request):

        form=Bus_RouteForm(request.POST)

        if form.is_valid():

            Route.objects.create(**form.cleaned_data)

            return redirect('bus')
        
        return render(request,'Bus_route.html',{'form':form})
        
####  bus details #########

class  Bus_Route_ListView(View):

    def get(self,request):

        Details=Route.objects.all()

        return render(request,'Bus_route_list.html',{'details':Details})
    
class Bus_Route_DetailsView(View):

    def get(self,request,**kwargs):

        route_id=kwargs.get('pk')

        route=Route.objects.get(id=route_id)

        return render(request,'Bus_route_Detail.html',{'route':route})
    
class Bus_Route_UpdateView(View):

    def get(self,request,**kwargs):

        id =kwargs.get('pk')

        data=Route.objects.get(id=id)

        form=Bus_RouteForm(instance=data)

        return render(request,'Bus_route_update.html',{'form':form})
    
    def post(self,request,**kwargs):

        id =kwargs.get('pk')

        data=Route.objects.get(id=id)

        form=Bus_RouteForm(request.POST,instance=data)

        if form.is_valid():

            form.save()

            messages.success(request,message='successfully updated ')
        
        return render(request,'Bus_route_update.html',{'form':form})
    
class Route_DeleteView(View):

    def get(self,request,**kwargs):

        id =kwargs.get('pk')

        route=Route.objects.get(id=id)

        if route:

            route.delete()

        return redirect('Bus_Route_List')
    
################ bus view ###################

class Bus_Register_view(View):

    def get(self,request):

        form=Bus_CreationForm

        return render(request,'Bus_create.html',{'form':form})
    
    def post(self,request):

        form=Bus_CreationForm(request.POST,request.FILES)

        if form.is_valid():

            Bus_Model.objects.create(**form.cleaned_data)

            print('sucess')

            messages.success(request, "bus created successfully!")
            
            form=Bus_CreationForm

            return render(request,'Bus_create.html',{'form':form})
        
        return redirect("Bus_list")

class Bus_Update_View(View):

    def get(self,request,**kwargs):

        id=kwargs.get('pk')

        data=Bus_Model.objects.get(id=id)

        form=Bus_CreationForm(instance=data)

        return render(request,'Bus_update.html',{'form':form})
    
    def post(self,request,**kwargs):

        id =kwargs.get('pk')

        data=Bus_Model.objects.get(id=id)

        form=Bus_CreationForm(request.POST,request.FILES,instance=data)

        if form.is_valid():

            form.save()

            messages.success(request,message='Bus updated successfully !')
        
        return render(request,'Bus_update.html',{'form':form})
      
class Bus_List_View(View):

    def get(self,request):

        data=Bus_Model.objects.all()
        
        return render(request,'Bus_list.html',{'data':data})
    
class Bus_Detail_View(View):

    def get(self,request,**kwargs):

        id =kwargs.get('pk')

        bus=Bus_Model.objects.get(id=id)

        return render(request,'Bus_Details.html',{'bus':bus})

class  Bus_DeleteView(View):

    def get(self,request,**kwargs):

        id =kwargs.get('pk')

        bus=Bus_Model.objects.get(id=id)

        if bus:

            bus.delete()

        return redirect('Bus_list')



# class Bus_BookingView(View):

#     def get(self,request):

#         form=Bus_BookingForm

#         return render(request,'booking.html',{'form':form})
    
#     def post(self,request):

#         form=Bus_BookingForm(request.POST)

#         if  form.is_valid():

#             Bus_BookingModel.objects.create(**form.cleaned_data)

#             return redirect('Home')
        
#         return render(request,'booking.html',{'form':form})
    


# ############ seats booking ############## and study this view carefully


class Bus_SeatsView(View):

    def get(self, request, **kwargs):
        bus_id = kwargs.get('pk')
        bus = Bus_Model.objects.get( id=bus_id)

        ##########this for review disply for last added one ######## Qury
        
        review=Review_Model.objects.filter(bus=bus_id).order_by('created_at').first()
        bookings = Bus_BookingModel.objects.filter(bus_Fk=bus)
        booked_seats = []
        for booking in bookings:
            booked_seats.extend(booking.seat_no.split(','))

        total_seats = bus.Total_seat
        available_seats = total_seats - len(booked_seats)

    
        return render(request, 'seats.html', {
            'bus': bus,
            'booked_seats': booked_seats,
            'total_seats': total_seats,
            'available_seats': available_seats,
            'price': int(bus.Price),
            'review':review,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID
        })


import razorpay

import json


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET ))

class Razorpay_PaymentView(View):

    def post(self,request):

        data=json.loads(request.body)

        amount = int(data.get('amount')) 

        seats = data.get('seats')

        bus_id = data.get('bus_id')

        razorpay_order = client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1
        })

        print(data)

        return JsonResponse({
            'order_id': razorpay_order['id'],
            'amount': razorpay_order['amount']
        })

class Payment_successView(View):

    def post(self, request):

        seats = request.POST.get('seats')
        bus_id = request.POST.get('bus_id')
        passengers = request.POST.get('passengers')

        order_id = request.POST.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')



        print(order_id)
        print(payment_id)

     
        bus = Bus_Model.objects.get(id=bus_id)
        selected_seats = seats.split(',')

        total_price = len(selected_seats) * int(bus.Price)

    
        booking = Bus_BookingModel.objects.create(
            user_Fk=request.user,
            bus_Fk=bus,
            seat_no=seats,
            passengers=passengers,
            total_price=total_price
        )

        # print(booking)

        payment=Payment_Model.objects.create(
            user=request.user,
            booking=booking,
            order_id=order_id,
            payment_id=payment_id,
            payment_status="PAID",
            amount=total_price
        )

        
        email_send=send_mail(subject='conformation your booking',message=f'Dear {request.user.username}, Your booking is confirmed form {bus.Operator_name} : travel agency. Thank you for booking with us',from_email=settings.EMAIL_HOST_USER,recipient_list=[request.user.email])
        # print(payment)

        return render(request,'payment_success.html',{'payment':payment})

######Booking Details ###########

# class Booking_DetailsView(View):

#     def get(self,request):
        
#         bookings =Bus_BookingModel.objects.filter(user_Fk=request.user)\
#             .select_related('bus_Fk','user_Fk')\
#             .order_by('-booking_date')
        
#         for booking in bookings:
            
#           route_date = booking.bus_Fk.Route_Fk.Available_date

#           booking.can_cancel = route_date > (datetime.today().date() + timedelta(days=1))

#           print(booking)
              
          
#         return render(request,'booking_details.html',{'bookings':bookings})

class Booking_DetailsView(View):
    def get(self, request):

        # Auto-delete expired bookings (more than 1 day past available date)
        today = datetime.today().date()

        expired_bookings = Bus_BookingModel.objects.filter(
            user_Fk=request.user,
            bus_Fk__Route_Fk__Available_date__lt=today - timedelta(days=1)
        )
        deleted_count = expired_bookings.count()

        print(deleted_count)

        expired_bookings.delete()

        bookings = Bus_BookingModel.objects.filter(user_Fk=request.user) \
            .select_related('bus_Fk', 'bus_Fk__Route_Fk') \
            .order_by('-booking_date')

        for booking in bookings:
            route_date = booking.bus_Fk.Route_Fk.Available_date

            # Only allow cancellation if route date is more than 1 day away
            booking.can_cancel = route_date > (datetime.today().date() + timedelta(days=1))

            print(f"Route Date: {route_date}, Today+1: {(datetime.today().date() + timedelta(days=1))}, Can Cancel: {booking.can_cancel}")

        return render(request, 'booking_details.html', {'bookings': bookings})
          
########### cancelition #############
    
class Booking_CancelitionView(View):

    def get(self,request,**kwargs):

        booking_id=kwargs.get('pk')

        booking=Bus_BookingModel.objects.get(id=booking_id)

        if booking:

            booking.delete()

        return redirect('booked')
    
########## Review adding ##########

class Review_View(View):

    def get(self,request,**kwargs):

        bus_id=kwargs.get('pk')

        bus=Bus_Model.objects.get(id=bus_id)

        form=ReviewForm 

        return render(request,'review.html',{'form':form,'bus':bus})

    def post(self,request,**kwargs):

        bus_id=kwargs.get('pk')

        bus=Bus_Model.objects.get(id=bus_id)

        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:

            data=Review_Model.objects.create(user=request.user,bus=bus,rating=rating,comment=comment)
           
            return redirect('review_details', pk=bus.id) #bus.id for need to redirecting page because url gives for id 
        
        else:

            print('Error: Rating or Comment is not correct')
        
            return render(request,'review.html',{'bus':bus})
        

class Review_DetailsView(View):

    def get(self,request,**kwargs):

        bus_id=kwargs.get('pk')

        review=Review_Model.objects.filter(bus=bus_id)

        return render(request,'review_details.html',{'review':review})
    
class Review_DeleteView(View):

    def get(self,request,**kwargs):

        review_id=kwargs.get('pk')

        review=Review_Model.objects.get(id=review_id, user=request.user)

        bus_id=review.bus.id

        review.delete()

        return redirect('review_details', pk=bus_id)
