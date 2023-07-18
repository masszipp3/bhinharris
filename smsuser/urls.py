from django.urls import path
from . import views

app_name='smsuser'

urlpatterns=[
  path('',views.index,name='home'),
  path('products',views.productlist,name='productslist'),
  path('addproduct',views.addproduct,name='addproduct'),
  path('categories',views.categories,name='categories'),
  path('addcategory',views.addcategories,name='addcategories'),
  path('<int:cid>/editcategory',views.updatecategory,name='editcategory'),
  path('<int:pid>/editproduct',views.updateproduct,name='editproduct'),
  path('<int:pid>/productdetails',views.productdetails,name='productdetails'),
  path('coupon',views.coupon,name='coupons'),
  path('addcoupon',views.addcoupon,name='addcoupon'),
  path('<int:cid>/updatecoupon',views.updatecoupon,name='updatecoupon'),
  path('orders',views.orders,name='orders'),
  path('addbanner',views.addbanner,name='addbanner'),
  path('report',views.report,name='report'),
  path('logout',views.smlogout,name='logout'),
  path('login',views.logins,name='login'),
  path('register',views.signup,name='signup'),
  path('<int:cid>/delete',views.delete,name='deletecatagory'),
  path('<int:pid>/deleteproduct',views.deleteproduct,name='deleteproduct'),
  path('<int:pid>/outstock',views.outofstock,name='outofstock'),
  path('<int:pid>/instock',views.instock,name='instock'),
  path('<int:cid>/couponactive',views.activecoupon,name='activatecoupon'),
  path('<int:cid>/deactivatecoupon',views.deactivecoupon,name='deactivatecoupon'),
  path('<int:cid>/deletecoupon',views.deletecoupon,name='deletecoupon'),
  path('<str:oid>/orderdetails',views.orderdetails,name='orderdetails'),
  path('<str:oid>/orderaccept',views.orderaccept,name='orderaccept'),
  path('<str:oid>/orderreject',views.orderreject,name='orderreject'),
  path('checkcatagory',views.checkcatagoryslug,name='checkcatagory'),
  path('checkproduct',views.checkproductslug,name='checkproduct'),
  path('<str:title>/deletebanner',views.deletebanner,name='deletebanner')












]