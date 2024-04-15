from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from airline.models import Ticket, Passenger, Flight
from django.contrib.auth import logout

def home(request):
    return render(request,"home.html")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('personal_cabinet')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def personal_cabinet(request):
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user=request.user)
        return render(request, 'profile.html', {'tickets': tickets})
    else:
        return redirect('login')

@login_required
def profile(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'profile.html', {'tickets': tickets})

def custom_logout_view(request):
    logout(request)
    return redirect('home')

def about(request):
    return render(request,"about.html")

def find_flights(request):
    if request.method == 'GET':
        origin_city = request.GET.get('origin_city')
        destination_city = request.GET.get('destination_city')

        # Query flights based on origin and destination cities
        flights = Flight.objects.filter(origin_city=origin_city, destination_city=destination_city)

        # Serialize flight data
        flight_data = [{'origin_city': flight.origin_city,
                        'destination_city': flight.destination_city,
                        'depart_time': flight.depart_time.strftime('%H:%M'),
                        'duration': str(flight.duration),
                        'plane': flight.plane,
                        'airline': flight.airline} for flight in flights]

        return JsonResponse(flight_data, safe=False)

@login_required
def my_booking(request):

    tickets = Ticket.objects.filter(user=request.user)

    tickets_data = [
        {
            'id': ticket.id,
            'user': str(ticket.user),
            'flight': str(ticket.flight),
            'passengers': [str(passenger) for passenger in ticket.passengers.all()],
            'seat_class': ticket.seat_class,
            'booking_date': ticket.booking_date.strftime('%Y-%m-%d %H:%M:%S'),
            'flight_ddate': ticket.flight_ddate.strftime('%Y-%m-%d') if ticket.flight_ddate else None,
            'flight_adate': ticket.flight_adate.strftime('%Y-%m-%d') if ticket.flight_adate else None,

        }
        for ticket in tickets
    ]
    return JsonResponse(tickets_data, safe=False)