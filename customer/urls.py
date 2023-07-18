from django.urls import path
from . import views

app_name='customer'

urlpatterns=[
    path('',views.index,name='home'),
    path('products',views.products,name='products'),
    path('customerpc',views.customerhomepc,name='customerpcweb'),
    path('product/<str:slug>',views.product_detail,name='product_details'),
    path('mycart',views.cart,name='mycart'),
    path('select',views.selectsup,name='selectsm'),
    path('login',views.customerlogin,name='login'),
    path('orderplaced',views.orderplaced,name='orderplaced'),
    path('addtocart',views.addcart,name='addtocart'),
    path('removecart',views.removefromcart,name='removecart'),
    path('applycoupon',views.applycoupon,name='applycoupon'),
    path('formsubmit',views.formsubmit,name='formsubmit'),
    path('search',views.searchproducts,name='search'),
    path('orders',views.customerorders,name='orders'),
    path('<str:oid>/orderdetails',views.orderdetails,name='orderdetails'),
    path('<str:oid>/ordercancel',views.ordercancel,name='ordercancel'),
    path('pchome',views.pchome,name='pchome'),
    path('logout',views.customerlogout,name='logout'),





    
]