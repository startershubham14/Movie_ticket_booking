from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from .models import Movie

def home(request):
    movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

from django.shortcuts import get_object_or_404
from .models import Showtime

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = movie.showtimes.all().order_by('date', 'time')
    return render(request, 'core/movie_detail.html', {'movie': movie, 'showtimes': showtimes})
from .models import Seat, Booking

def select_seats(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    all_seats = Seat.objects.all()
    booked_seats = Booking.objects.filter(showtime=showtime).values_list('seats__id', flat=True)

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        if request.user.is_authenticated:
            booking = Booking.objects.create(user=request.user, showtime=showtime)
            booking.seats.set(selected_seats)
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'select_seats.html', {
        'showtime': showtime,
        'all_seats': all_seats,
        'booked_seats': list(booked_seats)
    })

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count

@staff_member_required
def admin_dashboard(request):
    total_movies = Movie.objects.count()
    total_showtimes = Showtime.objects.count()
    total_bookings = Booking.objects.count()

    top_movies = Movie.objects.annotate(num_bookings=Count('showtimes__booking')).order_by('-num_bookings')[:5]

    return render(request, 'core/admin_dashboard.html', {
        'total_movies': total_movies,
        'total_showtimes': total_showtimes,
        'total_bookings': total_bookings,
        'top_movies': top_movies,
    })

from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

def get_seat_data(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    all_seats = list(Seat.objects.all().values('id', 'row', 'number'))
    booked_ids = list(Booking.objects.filter(showtime=showtime).values_list('seats__id', flat=True))
    return JsonResponse({'seats': all_seats, 'booked': booked_ids})


@require_POST
def ajax_book_seats(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    data = json.loads(request.body)
    showtime_id = data.get('showtime_id')
    seat_ids = data.get('seats', [])
    
    showtime = get_object_or_404(Showtime, id=showtime_id)
    
    # Check for double booking
    already_booked = Booking.objects.filter(showtime=showtime, seats__id__in=seat_ids).exists()
    if already_booked:
        return JsonResponse({'error': 'One or more seats are already booked.'}, status=400)

    booking = Booking.objects.create(user=request.user, showtime=showtime)
    booking.seats.set(seat_ids)
    return JsonResponse({'message': 'Booking successful'})
