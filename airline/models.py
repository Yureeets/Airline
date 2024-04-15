from django.db import models
from django.contrib.auth.models import User


class Flight(models.Model):
    origin_city = models.CharField(max_length=64)
    origin_code = models.CharField(max_length=3)
    origin_country = models.CharField(max_length=64)

    destination_city = models.CharField(max_length=64)
    destination_code = models.CharField(max_length=3)
    destination_country = models.CharField(max_length=64)

    depart_time = models.TimeField()
    duration = models.DurationField()
    plane = models.CharField(max_length=24)
    airline = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.origin_city}, {self.origin_country} ({self.origin_code}) to {self.destination_city}, {self.destination_country} ({self.destination_code})"


class Passenger(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.get_gender_display()}"  # Use get_gender_display()



class Ticket(models.Model):
    SEAT_CLASS = (
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('first', 'First')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    passengers = models.ManyToManyField(Passenger, related_name="flight_tickets")
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS)
    booking_date = models.DateTimeField(auto_now_add=True)
    flight_ddate = models.DateField(blank=True, null=True)
    flight_adate = models.DateField(blank=True, null=True)

