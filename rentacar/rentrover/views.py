from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import Booking

from .models import Car, Payment
from .forms import (
    CarAgencySignupForm,
    FeedbackForm,
    PaymentForm,
    CarAgencyUser,
    BookingForm,
    CarForm
)

# Homepage Views

def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    return redirect('caragencyhome')  

def homepage(request):
    return render(request, 'home.html')

def homepage_agency(request):
    cars = Car.objects.all()
    return render(request, 'car_agency_homepage.html', {'cars': cars})

def homepage_user(request):
    cars = Car.objects.all()
    return render(request, 'user_homepage.html', {'car': cars})

# Auth Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Logged in as regular user.")
            return redirect('userhome')

        try:
            agency_user = CarAgencyUser.objects.get(username=username)
            if agency_user.check_password(password):
                request.session['car_agency_user_id'] = agency_user.id
                messages.success(request, "Logged in as car agency user.")
                return redirect('caragencyhome')
            else:
                messages.error(request, "Invalid credentials.")
        except CarAgencyUser.DoesNotExist:
            messages.error(request, "Invalid credentials.")

    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        User.objects.create_user(username=username, password=password, email=email)
        return redirect('login')
    return render(request, 'signup.html')

# Car Agency Signup
def car_agency_signup(request):
    if request.method == 'POST':
        form = CarAgencySignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CarAgencySignupForm()
    return render(request, 'agency_signup.html', {'form': form})

# Booking View
@login_required
def booking(request, id):
    car = get_object_or_404(Car, pk=id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.save()
            return redirect('payment', car_id=car.id)
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'form': form, 'car': car})

# Feedback View
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'feedback.html', {'form': FeedbackForm(), 'success': True})
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

@login_required
def payment_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    # Fetch the latest booking for the current user and the selected car
    latest_booking = Booking.objects.filter(user=request.user, car=car).order_by('-id').first()
    
    if not latest_booking:
        return render(request, 'payment.html', {
            'form': None,
            'error': 'No booking found for this car.',
            'car': car
        })

    total_cost = latest_booking.total_cost

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.amount = total_cost  # Ensure user can't tamper with value
            payment.save()
            return redirect('payment_success')
    else:
        form = PaymentForm(initial={'amount': total_cost})

    return render(request, 'payment.html', {
        'form': form,
        'car': car
    })

# Payment Success
def payment_success(request):
    return render(request, 'payment_success.html')

# Admin: View all payments
@staff_member_required
def view_all_payments(request):
    payments = Payment.objects.all().order_by('-paid_at')
    return render(request, 'admin_payments.html', {'payments': payments})

# Car Agency: Add Car
@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('caragencyhome')
    else:
        form = CarForm()
    return render(request, 'addcar.html', {'form': form})

@staff_member_required  # restricts to admin/agency users
def all_bookings(request):
    bookings = Booking.objects.select_related('car', 'user').all()
    return render(request, 'all_bookings.html', {'bookings': bookings})

