from django.shortcuts import render,redirect
from . models import Customer,Product,Categories,Cart,CartItem,Coupon,UserCoupon,Order,OrderItem
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from smsuser.models import User,Supermarket,Banner
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.forms.models import model_to_dict
import random
from django.core.paginator import Paginator
import string
from django.db.models import Sum
from django.core import serializers
from datetime import datetime,time,timedelta
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.db.models import Count
import re
from django.urls import reverse
from . decorator import checkmobile



# Create your views here.
@checkmobile
@login_required(login_url='/customer/login')
def index(request):
    user_Agent= request.META.get('HTTP_USER_AGENT', '')
    mobile=re.search(r'mobile|android|iphone|ipad|ipod', user_Agent, re.IGNORECASE)
    if mobile:
        supermarkets=Supermarket.objects.values('id', 'slug', 'name','address')
        if request.method=='POST':
            super=Supermarket.objects.get(id=request.POST['selectsm'])
            Custom=Customer.objects.get(user=request.user)
            Custom.City=super.address
            Custom.save()
            request.session['supermarket']=super.id

        request.session['discount']=0
        today = datetime.now().date()
        supermarket=Supermarket.objects.filter(id=request.session['supermarket']).values('address').first().get('address')
        last_30_days_start = today - timedelta(days=30)
        productss=Product.objects.filter(Supermarket_name__id=request.session['supermarket'],onstock=True).order_by('-Discount')[:10]
        cart_items = CartItem.objects.filter(cart__customer=request.session['customer'], product__in=productss)
        quantities = {item.product_id: item.quantity for item in cart_items}  
        random_products = Product.objects.filter(Supermarket_name__id=request.session['supermarket'],onstock=True).order_by('?')[:10]
        most_ordered_products = Product.objects.filter(orderitem__order__created_at__gte=last_30_days_start,Supermarket_name_id=request.session['supermarket'],onstock=True).annotate(order_count=Count('orderitem__product')).order_by('-order_count')[:10]
        used_coupons = UserCoupon.objects.filter(user__user=request.user, used=True).values('coupon')        
        coupon=Coupon.objects.filter(active=True,supermarket_id=request.session['supermarket']).exclude(id__in=used_coupons)
        catagory=Categories.objects.filter(Supermarket_name_id=request.session['supermarket'])
        banners=Banner.objects.all()
        return render( request,'customer/index.html',{'catagory':catagory,'catagorycount':catagory.count(),'products':productss,'quantity':quantities,'most_ordered':most_ordered_products,'random':random_products,'coupon':coupon,'supermarket':supermarket,'super':supermarkets,'banners':banners})
    else:
        return redirect('customer:pchome')

@login_required(login_url='/customer/login')
def customerhomepc(request):
    supermarkets=Supermarket.objects.values('id', 'slug', 'name','address')
    if request.method=='POST':
        super=Supermarket.objects.get(id=request.POST['selectsm'])
        Custom=Customer.objects.get(user=request.user)
        Custom.City=super.address
        Custom.save()
        request.session['supermarket']=super.id

    request.session['discount']=0
    today = datetime.now().date()
    supermarket=Supermarket.objects.filter(id=request.session['supermarket']).values('address').first().get('address')
    last_30_days_start = today - timedelta(days=30)
    productss=Product.objects.filter(Supermarket_name__id=request.session['supermarket'],onstock=True).order_by('-Discount')[:10]
    cart_items = CartItem.objects.filter(cart__customer=request.session['customer'], product__in=productss)
    quantities = {item.product_id: item.quantity for item in cart_items}  
    random_products = Product.objects.filter(Supermarket_name__id=request.session['supermarket'],onstock=True).order_by('?')[:10]
    most_ordered_products = Product.objects.filter(orderitem__order__created_at__gte=last_30_days_start,Supermarket_name_id=request.session['supermarket'],onstock=True).annotate(order_count=Count('orderitem__product')).order_by('-order_count')[:10]
    used_coupons = UserCoupon.objects.filter(user__user=request.user, used=True).values('coupon')        
    coupon=Coupon.objects.filter(active=True,supermarket_id=request.session['supermarket']).exclude(id__in=used_coupons)
    catagory=Categories.objects.filter(Supermarket_name_id=request.session['supermarket'])
    banners=Banner.objects.all()
    return render( request,'customer/index.html',{'catagory':catagory,'catagorycount':catagory.count(),'products':productss,'quantity':quantities,'most_ordered':most_ordered_products,'random':random_products,'coupon':coupon,'supermarket':supermarket,'super':supermarkets,'banners':banners})

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'




@login_required(login_url='/customer/login')
def products(request):
    web=''
    user_Agent= request.META.get('HTTP_USER_AGENT', '')
    mobile=re.search(r'mobile|android|iphone|ipad|ipod', user_Agent, re.IGNORECASE)
    if mobile:
        web=False
    else:
        web=True

        
    request.session['discount']=0
    
    if is_ajax(request=request):
        catagoryvalue=request.GET['catagory'] 
        if catagoryvalue != '':
            product=Product.objects.filter(Supermarket_name__id=request.session['supermarket'],Product_category__slug=catagoryvalue,onstock=True).order_by('-modified_date')
        else:
            product=Product.objects.filter(Supermarket_name__id=request.session['supermarket'],onstock=True).order_by('-modified_date')
        catagory=Categories.objects.all()
        customer=Customer.objects.get(user=request.user)
        paginator = Paginator(product, 4)
        page_number = request.GET.get('page', 1)
        product_page = paginator.get_page(page_number)
        cart_items = CartItem.objects.filter(cart__customer=customer.id, product__in=product)
        quantities = {item.product_id: item.quantity for item in cart_items} 
        
        product_items = [
        {
            'id': product.id,
            'name': product.Product_name,
            'initialprice':product.Price,
            'price': product.final_total,
            'slug':product.slug,
            'brand':product.brand,
            'img':product.product_image.url,
            'minvalue':product.Min_value,
            'unit':product.Unit_type
            # ... other attributes you want to include
        }   
        for product in product_page
    ]
        
        has_next_page = product_page.has_next()

        return JsonResponse({
            'products': product_items,
            'has_next_page': has_next_page,
            'quantities':quantities
        })
    else:     
   
        total=0
        try:
            catagoryy=request.GET['catagory']
            customer=Customer.objects.get(user=request.user)
            print(catagoryy)
            catagory=Categories.objects.filter(Supermarket_name_id=request.session['supermarket'])
        
            product=Product.objects.filter(Supermarket_name__id=request.session['supermarket'],Product_category__slug=catagoryy,onstock=True).order_by('-modified_date')
        
                
            print(product)
        except:
            product=Product.objects.filter(Supermarket_name__id=request.session['supermarket'],onstock=True).order_by('-modified_date') 
            catagory=Categories.objects.filter(Supermarket_name_id=request.session['supermarket'])
            customer=Customer.objects.get(user=request.user)
        try:    
            cart=Cart.objects.get(customer=customer.id)  
            carts=CartItem.objects.filter(cart=cart)  
            count= carts.count()
        except:
            count=0    
        try:
            for cart in carts:
                item_cost = cart.quantity * cart.product.final_total
                total += item_cost
                request.session['grandtotal']=total
                request.session['finaltotal']=total

            
        
        except:
            pass
        
        cart_items = CartItem.objects.filter(cart__customer=customer.id, product__in=product)
        quantities = {item.product_id: item.quantity for item in cart_items}  
        print(quantities)  
        paginator = Paginator(product, 4)
        pagenumber=request.GET.get('page',1) 
        productpage=paginator.get_page(pagenumber)
        
        return render( request,'customer/products.html',{'porducts':productpage,'catagory':catagory,'quantity':quantities,'total':round(total,2),'count':count,'web':web})

@login_required(login_url='/customer/login')
def product_detail(request,slug):
    request.session['discount']=0
    product=Product.objects.get(slug=slug,Supermarket_name__id=request.session['supermarket'],onstock=True)
    try:
        carts=CartItem.objects.get(cart__customer__user=request.user,product=product)
    except:
        carts={'quantity':0} 
    return render( request,'customer/product_details.html',{'product_data':product,'quandity':carts})

@login_required(login_url='/customer/login')
def cart(request):
    request.session['discount']=0
    time_slot=''
    if request.method=='POST':
        delivery=request.POST['delivery']
        if delivery== 'later':
            
            time_slot=request.POST['timeslot']
            
        else:
            time_slot='Quick Delivery'
        coupon_code = request.POST.get('coupon_id')   
        super=Supermarket.objects.get(id=request.session['supermarket'])
        lastobj=Order.objects.latest('id')
        lastid=lastobj.id
           
        orderid='order' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))+str(lastid)
        customer=Customer.objects.get(id=request.session['customer'])
        totalprice= request.session.get('finaltotal', 0)
        # vat=totalprice*0.05
        # totalprice+=vat
        if coupon_code:
            coupons=Coupon.objects.get(id=coupon_code)
            orderdetails=Order.objects.create(Supermarketname_id=request.session['supermarket'],OrderId=orderid,user_id=request.session['customer'],total_price=round(totalprice,2),delivery_option=delivery,
                                              time_slot=time_slot,discount=coupons.discount,couponcodeapplied=True)
            usercoup=UserCoupon.objects.create(user_id=request.session['customer'],coupon_id=coupon_code,used=True,order=orderdetails)
        else:
            orderdetails=Order.objects.create(Supermarketname_id=request.session['supermarket'],OrderId=orderid,user_id=request.session['customer'],total_price=totalprice,delivery_option=delivery,time_slot=time_slot)
        cartss=Cart.objects.get(customer__user=request.user)
        cartitem=CartItem.objects.filter(cart=cartss)
        for cart_item in cartitem:
            order_item = OrderItem.objects.create(
                order=orderdetails,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.final_total
            )
        cartss.delete()
        del request.session['finaltotal']
        del request.session['grandtotal']

  
        return redirect('customer:orderplaced')

    total=0
    actualtotal=0
    try:
        carts=Cart.objects.get(customer__user=request.user)
    except:
        carte=Cart.objects.create(customer_id=request.session['customer'])  
        carts=Cart.objects.get(customer__user=request.user)  
    custmerdet=Customer.objects.get(id=request.session['customer'])
    cartdetails=CartItem.objects.filter(cart=carts)
    time_slot_choices = Order.TIMESLOT_CHOICES
    deliveryoptions=Order.DELIVERY
    current_time = datetime.now().time()
    available_time_slots = []
    for choice in Order.TIMESLOT_CHOICES:
        time_slot = choice[1]
        print(time_slot)
        start_time_str, end_time_str = time_slot.split('-')
        start_time = datetime.strptime(start_time_str.strip(), '%I:%M %p').time()
        middletime = (datetime.combine(datetime.min, start_time) + timedelta(hours=1)).time()

        print(start_time,middletime)
        
        if middletime >= current_time:
            available_time_slots.append(time_slot)
            print(available_time_slots)
    try:
        total = request.session['grandtotal']
        request.session['finaltotal']=total
        for cart in cartdetails:
            item_costs = cart.quantity * cart.product.Price
            actualtotal += item_costs
    except:
        for cart in cartdetails:
            item_cost = cart.quantity * cart.product.final_total
            total += item_cost
        for cart in cartdetails:
            item_costs = cart.quantity * cart.product.Price
            actualtotal += item_costs    
            request.session['grandtotal']=total
            request.session['finaltotal']=total
    used_coupons = UserCoupon.objects.filter(user__user=request.user, used=True).values('coupon')        
    coupon=Coupon.objects.filter(min_purchase__lte=total,active=True).exclude(id__in=used_coupons)
    discountedprice=actualtotal-total
   

    return render( request,'customer/cart.html',{'cart':cartdetails,'cartcount':cartdetails.count(),'total':round(total,2),'coupon':coupon,'customer':custmerdet,
                                                 'timeslot':time_slot_choices,'delivery':deliveryoptions,'available':available_time_slots,'discount':round(discountedprice,2)})

@login_required(login_url='/customer/login')
def applycoupon(request):
    total=0
    if request.method=='POST':
        couponid=request.POST['couponid']
        coupons=Coupon.objects.get(id=couponid)
        total=request.session['grandtotal']
        discount=(float(coupons.discount)/100)*total
        finaltotal=round(total-discount,2)
        print(finaltotal)
        request.session['finaltotal']=float(finaltotal)
        final_total_str = str(finaltotal)
        finaldiscount=str(discount)
        request.session['discount']=float(coupons.discount)
    return JsonResponse({'data':'success','finaltotal':final_total_str,'total':round(total,2),'discount':round(float(finaldiscount),2)})  

    

@login_required(login_url='/customer/login')
def addcart(request):
    msgfrom=request.POST.get('from',False)
    actualtotal=0
    cart=''
    if request.session['discount']:
        discount=request.session['discount']
    else:
        discount=0    
    print(discount)    
    if request.method=='POST':
        productid=request.POST['productid']
        product=Product.objects.get(id=productid)
        customer=Customer.objects.get(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        finaltotal=request.session.get('finaltotal', 0)
        grandtotals=request.session.get('grandtotal',0)
        finaltotal=grandtotals
        if not item_created:
            cart_item.quantity+=1
            cart_item.save()
            finaltotal+=cart_item.product.final_total
        cartdetails=CartItem.objects.filter(cart_id=cart.id)   
        if msgfrom: 
            for cartss in cartdetails:
                item_costs = cartss.quantity * cartss.product.Price
                actualtotal += item_costs  
        carts=CartItem.objects.filter(cart=cart)
        count=carts.count()
        subtotal=cart_item.product.final_total * cart_item.quantity
        grandtotal=sum(item.product.final_total * item.quantity for item in carts)
        print(grandtotal)
        discountamount=discount/100*finaltotal
        finaltotal-=discountamount

        request.session['grandtotal']=grandtotal
        request.session['finaltotal']=finaltotal
        

        return JsonResponse({'data':'success','total':round(grandtotal,2),'count':count,'subtotal':round(subtotal,2),'finaltotal':round(finaltotal,2),'dicountedprice':round(discountamount,2),'discountfinal':round(actualtotal,2)})  
    else:
        productid=request.GET.get('productid')
        qundity=request.GET.get('quantity')
        product=Product.objects.get(id=productid)
        customer=Customer.objects.get(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            
            cart_item.quantity=int(qundity)
            cart_item.save()
        carts=CartItem.objects.filter(cart=cart)
        count=carts.count()
        subtotal=cart_item.product.final_total * cart_item.quantity
        grandtotal=sum(item.product.final_total * item.quantity for item in carts)

        request.session['grandtotal']=grandtotal 
        request.session['finaltotal']=grandtotal
                
        return JsonResponse({'data':'success','quantity':cart_item.quantity})

@login_required(login_url='/customer/login')    
def removefromcart(request):
    msgfrom=request.POST.get('from',False)
    actualtotal=0
    if request.session['discount']:
        discount=request.session['discount']
    else:
        discount=0    
    if request.method=='POST':
        productid=request.POST['productid']
        customer=Customer.objects.get(user=request.user)
        cart=CartItem.objects.filter(product_id=productid,cart__customer=customer.id).exists()
        if cart:
            carts=CartItem.objects.get(product_id=productid,cart__customer=customer.id)
            carts.quantity -=1
            carts.save()
            total = request.session['grandtotal'] 
            total -= carts.product.final_total
            request.session['grandtotal']  = total 
            request.session['finaltotal']=total
            finaltotal = request.session['finaltotal']
            discountedprice = (discount/100)*finaltotal
            finaltotal-=discountedprice
            request.session['finaltotal']=finaltotal
            subtotal=carts.quantity * carts.product.final_total
            if carts.quantity==0:
                carts.delete()
            cartdetails=CartItem.objects.filter(cart__customer=customer)     
            if msgfrom: 
                for cartss in cartdetails:
                    item_costs = cartss.quantity * cartss.product.Price
                    actualtotal += item_costs    
            cartss=CartItem.objects.filter(cart__customer=customer.id)
            count=cartss.count()
            return JsonResponse({'data':'success','total':round(total,2),'count':count,'subtotal':round(subtotal,2),'finaltotal':round(finaltotal,2),'dicountedprice':round(discountedprice,2),'discountfinal':round(actualtotal,2)})
        else :
            return JsonResponse({'data':'notexist'})
        
        
        
            
@login_required(login_url='/customer/login')
def selectsup(request):
    supermarket=Supermarket.objects.values('id', 'slug', 'name','address')
    if request.method=='POST':
        super=Supermarket.objects.get(id=request.POST['selectsm'])
        Custom=Customer.objects.get(user=request.user)
        Custom.City=super.address
        Custom.save()
        request.session['supermarket']=super.id
        user_Agent= request.META.get('HTTP_USER_AGENT', '')
        mobile=re.search(r'mobile|android|iphone|ipad|ipod', user_Agent, re.IGNORECASE)
        if not mobile:
            url=reverse('customer:customerpcweb')+'?=web=true'
            return redirect('customer:customerpcweb')
        else:
            return redirect('customer:home')
    return render( request,'customer/selectsm.html',{'super':supermarket})

def customerlogin(request):
    if 'customer' not in request.session:
        if request.method=='POST':
            email=request.POST['email']
            password='binharris$%09*&*&%%%%$'
            customer_exist= Customer.objects.filter(customer_email=email,is_customer=True).exists()
            if customer_exist:
                user = authenticate(request, username=email, password=password)
                print(user)
                if user is not None and user.is_customer:
                    login(request, user)
                    customer=Customer.objects.get(user=request.user)
                    request.session['customer']=customer.id
                    return redirect('customer:selectsm') 
                else:   
                    HttpResponse('error`')

            else:
                user=User.objects.create_user(username=email,password=password,is_customer=True)
                customer=Customer.objects.create(customer_email=email,user=user)
                if user is not None and user.is_customer:
                    login(request, user)
                    customers=Customer.objects.get(user=request.user)
                    request.session['customer']=customers.id
                    return redirect('customer:selectsm') 
            

            

        return render( request,'customer/login.html')
    else:
        return redirect('customer:home')

@login_required(login_url='/customer/login')
def orderplaced(request):
    return render( request,'customer/orderplaced.html')

def pchome(request):
    user_Agent= request.META.get('HTTP_USER_AGENT', '')
    mobile=re.search(r'mobile|android|iphone|ipad|ipod', user_Agent, re.IGNORECASE)
    if mobile:
        return redirect('customer:home')
    else:
        return render( request,'customer/pchome.html')
            

        


@login_required(login_url='/customer/login')
def ordercancel(request,oid):
    order=Order.objects.get(OrderId=oid)
    order.status='Rejected'
    order.save()
    return redirect('customer:orders')

@login_required(login_url='/customer/login')
def orderdetails(request,oid):
    total=0
    order=Order.objects.get(OrderId=oid)
    orderitems=OrderItem.objects.filter(order=order)
    for orders in orderitems:
        total += orders.quantity*orders.price
    discount=(order.discount/100)*total
    print(orderitems)
    return render( request,'customer/orderdetails.html',{'order':order,'grandtotal':order.total_price,'orderdetails':orderitems,'discount':round(float(discount),2),'total':round(total,2),'discountedprice':round(float(total-discount),2),'count':orderitems.count()})

@login_required(login_url='/customer/login')
def customerorders(request):
    order=Order.objects.filter(user_id=request.session['customer']).order_by('-created_at')
    orderdetails=OrderItem.objects.filter(order__in=order)
    orderdet={item.order_id:item.order.total_price for item in orderdetails}
    product_count = orderdetails.values('order_id').annotate(count=Count('product'))
    # Create a dictionary with order IDs as keys and product    counts as values
    product_counts_dict = {item['order_id']: item['count'] for item in product_count}
    print(product_counts_dict)

    return render( request,'customer/orders.html',{'orderdetails':order,'count':order.count(),'total':orderdet,'productscount':product_counts_dict})


@login_required(login_url='/customer/login')
def formsubmit(request):
    if request.method=='POST':
        bhtapp=request.POST.get('bht')
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        building=request.POST.get('house')
        street=request.POST.get('address')
        city= request.POST.get('city')
        landmark=request.POST.get('landmark')
        province=request.POST.get('province')
        district=request.POST.get('district')
        code=request.POST.get('postalcode')
        print(bhtapp,name)
        

        customer=Customer.objects.get(id=request.session['customer'])
        if bhtapp == '1':
            customer.customer_name=name
            customer.Mobile=phone
            customer.House=building
            customer.City=city
            customer.BHT_Appartment=True
            customer.save()
        else:
            customer.customer_name=name
            customer.Mobile=phone
            customer.House=building
            customer.City=city   
            customer.Province=province
            customer.District=district
            customer.Street=street
            customer.Postalcode=code
            customer.BHT_Appartment=False
            customer.Landmark=landmark
            customer.save()
        customers=Customer.objects.get(id=request.session['customer'])    
        cutomerlist=model_to_dict(customers)  
        return JsonResponse({'data':cutomerlist})
    return JsonResponse({'data':'invalidrequest'})


@login_required(login_url='/customer/login')

def searchproducts(request):

   total=0
   if request.method == 'POST':
        query=request.POST['query']
        searchresults=Product.objects.filter(Q(Product_name__icontains=query) | Q(brand__icontains=query) | Q(Product_category__category_name__icontains=query))[:20]
        keyword = []
        

        for product in searchresults:
            # Extract keywords from product attributes
            if len(query)>=5:
                keyword.append(product.Product_name)
           
            keyword.extend(word for word in product.Product_name.split() if len(word) >= 4)
            keyword.extend(word for word in product.Product_category.category_name.split() if len(word) >= 4)
            keyword.extend(word for word in product.brand.split() if len(word) >= 3)
            

        # Remove duplicates and limit the number of keywords to 10
        unique_keywords = list(set(keyword))

        # Sort the keywords with matching query at the beginning
        sorted_keywords = sorted(unique_keywords, key=lambda x: query.lower() not in x.lower())

        return JsonResponse({'data':sorted_keywords[:10]}, safe=False)
   querys=request.GET.get('query')
   queries=querys.split()
   search=Q()
   for term in queries:
       search|=Q(Product_name__icontains=term)
       
   customer=Customer.objects.get(user=request.user)
   searchresults=Product.objects.filter(search | Q(brand__icontains=querys) | Q(Product_category__category_name__icontains=querys),Supermarket_name__id=request.session['supermarket'])[:20]
   try:    
        cart=Cart.objects.get(customer=customer.id)  
        carts=CartItem.objects.filter(cart=cart)  
        count= carts.count()
   except:
        count=0    
   try:
        for cart in carts:
            item_cost = cart.quantity * cart.product.final_total
            total += item_cost
        
    
   except:
        pass
    
   cart_items = CartItem.objects.filter(cart__customer=customer.id, product__in=searchresults)
   quantities = {item.product_id: item.quantity for item in cart_items}  
   print(quantities)
   return render( request,'customer/search.html',{'porducts':searchresults,'quantity':quantities,'total':total,'count':count,'query':querys})  

def customerlogout(request):
   logout(request)  
   return redirect('customer:login')

            



