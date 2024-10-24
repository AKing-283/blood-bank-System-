from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Model for Blood Group
class BloodGroup(models.Model):
    name = models.CharField(max_length=5, unique=True)  # Blood group names should be unique (e.g., "O+", "AB-")

    def __str__(self):
        return self.name


# Model for blood request from a person
class RequestBlood(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    state = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=500, blank=True)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)  # Use DateField for dates

    def __str__(self):
        return self.name


# Model for Donors
class Donor(models.Model):
    donor = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    date_of_birth = models.DateField()  # Date of birth should be a DateField
    phone = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField(max_length=500, default="")
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    image = models.ImageField(upload_to="donor_images/")  # Use a dedicated folder for donor images
    ready_to_donate = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.donor.username} - {self.blood_group}"


# Blood request model associated with a user
class BloodRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    state = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=500, blank=True)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


# Custom email validator for Gmail only
def validate_gmail_email(value):
    if not value.endswith('@gmail.com'):
        raise ValidationError("Email must be a @gmail.com address")


# Profile model with different user types
class Profile(models.Model):
    USER_TYPES = (
        ('hospital', 'Hospital'),
        ('donor', 'Donor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    email = models.EmailField(validators=[validate_gmail_email], null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='donor')

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
