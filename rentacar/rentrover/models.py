from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission,User

    
class CarAgencyUser(AbstractUser):
    agency_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)

    groups = models.ManyToManyField(Group, related_name="car_agency_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="car_agency_users_permissions", blank=True)

    def __str__(self):
        return self.agency_name


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments',null=True)
    name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)  # MM/YY format
    cvv = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.name} - {self.amount}"

    
class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    rent_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='image', blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        days = (self.end_date - self.start_date).days + 1
        self.total_cost = days * self.car.rent_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.car} from {self.start_date} to {self.end_date}"
