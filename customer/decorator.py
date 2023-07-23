from django.shortcuts import redirect,render
import re
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

def checkmobile(func):
    def wrap(request, *args, **kwargs):
        user_Agent= request.META.get('HTTP_USER_AGENT', '')
        mobile=re.search(r'mobile|android|iphone|ipad|ipod', user_Agent, re.IGNORECASE)
        if mobile:
            return func(request, *args, **kwargs)
        else:
            return redirect('customer:pchome')
            
    return wrap

def is_customer(user):
    return user.is_authenticated and user.is_customer

def customer_required(view_func):
    decorated_view = user_passes_test(is_customer, login_url=reverse_lazy('customer:login'))
    return decorated_view(view_func)    