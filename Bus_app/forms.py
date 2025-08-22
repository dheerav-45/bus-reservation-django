from django import forms

from Bus_app.models import *

#########   Email Registraion   ###########

class User_Email_RegisterForm(forms.ModelForm):

    class Meta:

        model=CustomUser

        fields =['username','email','password','gender','age','dob']


class Email_OtpVerifyForm(forms.Form):

    otp=forms.CharField(max_length=50)
        
class LoginEmailForm(forms.Form):

   
    email = forms.EmailField(max_length=50,
                                widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    password = forms.CharField(max_length=20,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
######### phone Registeration #############


class User_Phone_Number_RegisterForm(forms.ModelForm):

    class Meta:

        model=CustomUser

        fields=['username','phone_number','password','gender','age','dob']

class Phone_OtpVerifyForm(forms.Form):

    otp=forms.CharField(max_length=50)


class Phone_LoginForm(forms.Form):

    phone_number=forms.CharField(max_length=50)

    password=forms.CharField(max_length=50)


######## Email_Reset #######
class Email_Forgot_PasswordForm(forms.Form):

    email=forms.EmailField()


class Email_Forgot_Password_OTP_verifyForm(forms.Form):

    otp=forms.CharField(max_length=50)

class Email_Password_ResetForm(forms.Form):

    new_password=forms.CharField(max_length=50)

    confirm_password=forms.CharField(max_length=50)

######## Phone_password Reset #######

class Phone_Forgot_PasswordForm(forms.Form):

    phone_number=forms.CharField(max_length=50)

class Phone_Forgot_Password_OTP_verifyForm(forms.Form):

    otp=forms.CharField(max_length=50)

class Phone_Password_ResetForm(forms.Form):

    new_password=forms.CharField(max_length=50)

    confirm_password=forms.CharField(max_length=50)


#####################################

class Bus_RouteForm(forms.ModelForm):

    class Meta:

        model=Route

        fields=['source','destination','duration','departure_time','arrival_time','Available_date']

        widgets = {
                    'source': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter source location'}),
                    'destination': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter destination location'}),
                    'duration': forms.TextInput(attrs={'class': 'form-control','placeholder': 'e.g., 01:30:00'}),
                    'departure_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
                    'arrival_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
                    'Available_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
                    }
    

############### Bus #################


class Bus_CreationForm(forms.ModelForm):

    class Meta:

        model =Bus_Model

        fields=['Bus_No','Operator_name','Bus_image','Bus_Types','available_seates','Total_seat','Price','Route_Fk']

        widgets = {
            'Bus_No': forms.TextInput(attrs={'class': 'form-control'}),
            'Operator_name': forms.TextInput(attrs={'class': 'form-control'}),
            'Bus_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'Bus_Types': forms.Select(attrs={'class': 'form-control'}),
            'available_seates': forms.NumberInput(attrs={'class': 'form-control'}),
            'Total_seat': forms.NumberInput(attrs={'class': 'form-control'}),
            'Price': forms.NumberInput(attrs={'class': 'form-control'}),
            'Route_Fk': forms.Select(attrs={'class': 'form-control'}),
        }


class Bus_BookingForm(forms.ModelForm):

    class Meta:

        model=Bus_BookingModel

        fields=['user_Fk','bus_Fk','seat_no','passengers']
        
    
class ReviewForm(forms.ModelForm):

    class Meta:

        model=Review_Model

        fields=['user','bus','rating','comment']