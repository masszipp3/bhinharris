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