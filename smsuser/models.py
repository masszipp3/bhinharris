from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    is_supermarket = models.BooleanField(default=False)
    email = models.CharField(max_length=100)
    is_customer=models.BooleanField(default=False)
    # Add any additional fields you need for the supermarket user

class Supermarket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=20)
    slug=models.CharField(max_length=20)

class Banner(models.Model):
    image = models.ImageField(upload_to="customer/",null=True)
    title = models.CharField(max_length=100,null=True)
    offerbrand = models.CharField(max_length=20,null=True)
    offerdetails = models.CharField(max_length=20,null=True)

  