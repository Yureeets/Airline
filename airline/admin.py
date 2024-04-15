from django.contrib import admin
from .models import Flight, Passenger, Ticket

admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Ticket)
