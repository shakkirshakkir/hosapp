from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Doctor(models.Model):
    Name=models.CharField(max_length=100)
    mobile=models.IntegerField()
    special=models.CharField(max_length=100)
    def __str__(self):
        return self.Name
class Patient(models.Model):
    Name=models.CharField(max_length=100)
    gender=models.CharField(max_length=10)
    mobile=models.IntegerField(null=True)
    address=models.TextField(max_length=100) 
    def __str__(self):
        return self.Name

class Appointment(models.Model):
    Doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    Patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    def __str__(self):
        return self.Doctor.Name+"__"+self.Patient.Name
class Payment(models.Model):
    # Payment model fields
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()

    def __str__(self):
        return f"Payment of {self.amount} made on {self.payment_date}"


class AppointmentRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_requested = models.DateTimeField(auto_now_add=True)
    requested_date = models.DateField()
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)
    # payment_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)

  

    def __str__(self):
        return f"Appointment Request by {self.user.username} on {self.requested_date}"

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name