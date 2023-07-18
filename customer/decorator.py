from django.shortcuts import redirect,render
import re

def checkmobile(func):
    def wrap(request, *args, **kwargs):
        user_Agent= request.META.get('HTTP_USER_AGENT', '')
        mobile=re.search(r'mobile|android|iphone|ipad|ipod', user_Agent, re.IGNORECASE)
        if mobile:
            return func(request, *args, **kwargs)
        else:
            return redirect('customer:pchome')
            
    return wrap