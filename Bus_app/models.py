from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True,unique=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'),('Female', 'Female')], blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    image=models.ImageField(upload_to='Profile_Photo',null=True,blank=True,default='profile_images/default.jpg')

    def __str__(self):
        return self.username
    

class Route(models.Model):

    source = models.CharField(max_length=100)

    destination = models.CharField(max_length=100)

    duration = models.DurationField(null=True)

    departure_time = models.TimeField()  #start

    arrival_time = models.TimeField() #end

    Available_date=models.DateField(null=True)

    
    def __str__(self):
        return f"{self.source} → {self.destination} ({self.Available_date})"



class Bus_Model(models.Model):

    Bus_No=models.CharField(max_length=50,unique=True)

    Operator_name=models.CharField(max_length=100)

    Bus_image=models.ImageField(upload_to='bus_images',null=True,blank=True,default='bus_images/default.jpg')

    Bus_Types=models.CharField(max_length=20,choices=[('SEATER','SEATER'),('SLEEPER','SLEEPER'),('AC','AC'),('NONAC','NONAC')])

    Seat_No=models.CharField(max_length=10,null=True,blank=True)

    available_seates=models.IntegerField(null=True,blank=True)

    Total_seat=models.IntegerField()

    Price=models.DecimalField(max_digits=8,decimal_places=2)

    Route_Fk=models.ForeignKey(Route,on_delete=models.CASCADE)

    def __str__(self):
        return self.Bus_No

class Bus_BookingModel(models.Model):

    user_Fk=models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    bus_Fk=models.ForeignKey(Bus_Model,on_delete=models.CASCADE)

    booking_date=models.DateField(auto_now_add=True)

    seat_no=models.CharField(max_length=50)

    passengers=models.CharField(max_length=50)

    total_price=models.CharField(max_length=50,blank=True,null=True)


class Review_Model(models.Model):

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1 to 5 stars
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus_Model, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Payment_Model(models.Model):

    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    booking=models.ForeignKey(Bus_BookingModel,on_delete=models.CASCADE)

    order_id=models.CharField(max_length=100)

    payment_id=models.CharField(max_length=100,null=True,blank=True)

    payment_status=models.CharField(max_length=100,default='PENDING')

    amount=models.IntegerField(null=True,blank=True)

    created_date=models.DateField(auto_now_add=True)

