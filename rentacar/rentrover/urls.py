from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('userhome/', views.homepage_user, name='userhome'),
    path('booking/<int:id>/', views.booking, name='booking'),
    path('car-agency-signup/', views.car_agency_signup, name='car_agency_signup'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('payment/<int:car_id>/', views.payment_view, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('caragency/', views.homepage_agency, name='caragencyhome'),
    path('add-car/', views.add_car, name='add_car'),
    path('payments/', views.view_all_payments, name='admin_payments'),
    path('all-bookings/', views.all_bookings, name='all_bookings'),
    path('delete-car/<int:car_id>/', views.delete_car, name='delete_car'),

]
