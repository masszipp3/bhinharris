# from django.shortcuts import redirect,render
# import re

# def checkmobile(func):
#     def wrap(request, *args, **kwargs):
#         supermrk=Supermarket.objects.get(user=request.user)
#         if mobile:
#             return func(request, *args, **kwargs)
#         else:
#             return redirect('customer:pchome')
            
#     return wrap

from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
def is_supermarket(user):
    return user.is_authenticated and user.is_supermarket

def adminlog_required(view_func):
    decorated_view = user_passes_test(is_supermarket, login_url=reverse_lazy('smsuser:login'))
    return decorated_view(view_func)    