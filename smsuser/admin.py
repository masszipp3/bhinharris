from django.contrib import admin
# from django.contrib.auth.models import User
from .models import Supermarket,User

admin.site.register(Supermarket)
admin.site.register(User)
