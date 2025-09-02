# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CarAgencyUser,Feedback,Payment,Car,Booking

class CarAgencySignupForm(UserCreationForm):
    agency_name = forms.CharField(max_length=255)
    address = forms.CharField(widget=forms.Textarea)
    contact_number = forms.CharField(max_length=15)

    class Meta:
        model = CarAgencyUser
        fields = ['username', 'email', 'agency_name', 'address', 'contact_number', 'password1', 'password2']

    # This save method should be properly indented inside the form class
def save(self, commit=True):
    user = super().save(commit=False)
    user.agency_name = self.cleaned_data['agency_name']
    user.address = self.cleaned_data['address']
    user.contact_number = self.cleaned_data['contact_number']
        
    if commit:
        user.save()
        
    return user

        
       
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'card_number', 'expiry_date', 'cvv', 'amount']
        widgets = {
            'card_number': forms.PasswordInput(),
            'cvv': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['readonly'] = True



class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'brand', 'model', 'year', 'rent_per_day', 'available', 'image']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }