from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from . models import User, Supermarket,Banner
from customer.models import Order,OrderItem
from django.shortcuts import get_object_or_404
from customer.models import Categories,Product,Coupon
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from datetime import datetime   
from django.http import JsonResponse
from django.db.models import Q,Sum
from django.forms.models import model_to_dict
from django.core import serializers
from django.utils import timezone
from django.utils.timezone import now
from datetime import date

# Create your views here.
@login_required(login_url='/smsuser/login')
def index(request):
    try:
        supermrk=Supermarket.objects.get(user=request.user)
    except Supermarket.DoesNotExist:
        return redirect('smsuser:login')    
    
    current_year = now().year
    year_total_count = Order.objects.filter(created_at__year=current_year,Supermarketname__id=supermrk.id).count()
    year_total_Sales=Order.objects.filter(created_at__year=current_year,Supermarketname__id=supermrk.id).aggregate(total=Sum('total_price')).get('total',0)
    monthlysalescount = []
    monthlysales = []
    monthlysalesacceptedcount=[]
    monthlysalescancelledcount=[]
    
    
    if request.method=='POST':
        status=request.POST['status']

        if status=='count':
        
            for month in range(1,13):
                    month_start=now().replace(year=current_year, month=month,day=1, hour=0, minute=0, second=0, microsecond=0)
                    if month<12:
                        next_month_start=month_start.replace(month=month+1)
                    else:
                        next_month_start=month_start.replace(year=current_year+1,month=month) 
                    monthsale=Order.objects.filter(created_at__gte=month_start,created_at__lte=next_month_start,Supermarketname__id=supermrk.id).count()   
                    # salepercentage=(monthsale/year_total_count)*100
                    monthsaleacc=Order.objects.filter(created_at__gte=month_start,created_at__lte=next_month_start,status='Accepted',Supermarketname__id=supermrk.id).count()
                    monthsalecanc=Order.objects.filter(created_at__gte=month_start,created_at__lte=next_month_start,status='Rejected',Supermarketname__id=supermrk.id).count()
                    monthlysalescount.append(int(monthsale)) 
                    monthlysalesacceptedcount.append(int(monthsaleacc))
                    monthlysalescancelledcount.append(int(monthsalecanc))
            return JsonResponse({'data':monthlysalescount,'accepted':monthlysalesacceptedcount,'rejected':monthlysalescancelledcount})
        
        elif status=='sales':
            print('dd')
            for month in range(1,13):
                    month_start=now().replace(year=current_year, month=month,day=1, hour=0, minute=0, second=0, microsecond=0)
                    if month<12:
                        next_month_start=month_start.replace(month=month+1)
                    else:
                        next_month_start=month_start.replace(year=current_year+1,month=month) 
                    monthsale=Order.objects.filter(created_at__gte=month_start,created_at__lte=next_month_start,status='Accepted',Supermarketname__id=supermrk.id).aggregate(total=Sum('total_price')).get('total',0)
                    if monthsale is None:
                        monthsale=0
                    
                    # salepercentage=(monthsale/year_total_Sales)*100
                    monthlysales.append(int(monthsale)) 
            return JsonResponse({'data':monthlysales})

    # super=Supermarket.objects.get(id=request.user)
    today=date.today()
    print(today)
    month_start=now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly=Order.objects.filter(created_at__gte=month_start,Supermarketname__id=supermrk.id)
    monthsale=Order.objects.filter(created_at__gte=month_start,status='Accepted',Supermarketname__id=supermrk.id).aggregate(total=Sum('total_price')).get('total',0)
    monthlycount=monthly.count()
    Orderss=Order.objects.filter(Supermarketname__user=request.user).order_by('-created_at')
    paginator = Paginator(Orderss, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    Orders=Order.objects.filter(created_at__date=today,Supermarketname__id=supermrk.id).count()
    
    todaysale=Order.objects.filter(created_at__date=today,status='Accepted',Supermarketname__id=supermrk.id).aggregate(total=Sum('total_price')).get('total', 0.0)
    if todaysale is None:
         todaysale=0
    if monthsale is None:
        monthsale=0     
        
    
    return render(request,'smsuser/index.html',{'ordercount':Orders,'todaysale':round(todaysale,2),'monthsale':round(monthsale,2),'monthcount':monthlycount,'orders':page_obj,'supermarketdetails':supermrk})

@login_required(login_url='/smsuser/login')
def productlist(request):
    if request.method=='POST':
        keyword=request.POST['keyword']
        
        searchresults=Product.objects.filter(Q(Product_name__icontains=keyword) | Q(brand__icontains=keyword) | Q(Product_ID__icontains=keyword),Supermarket_name__user=request.user)[:20]
        serialized_results=[]
        for product in searchresults:
            serialized_product = model_to_dict(product)
            serialized_product['product_image'] = str(product.product_image)  # Convert the ImageFieldFile to a string
            serialized_results.append(serialized_product)
        print(serialized_results)
        return JsonResponse({'searchdata':serialized_results})
    msg = request.GET.get('msg', '')
    products=Product.objects.filter(Supermarket_name__user=request.user).order_by('-modified_date')
    paginator = Paginator(products, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    supermrk=Supermarket.objects.get(user=request.user)
    return render(request,'smsuser/productlist.html',{'productpage':page_obj,'supermarketdetails':supermrk})

@login_required(login_url='/smsuser/login')
def addproduct(request):
    msg=''
    supermrk=Supermarket.objects.get(user=request.user)
    catagory=Categories.objects.all()
    if request.method=='POST':
        porduct_name=request.POST['productname']
        product_id=request.POST['productid']
        product_price=request.POST['price']
        slug=request.POST['slug']
        description= request.POST['description']
        category=request.POST['catagory']
        unit=request.POST['unit']
        minquandity=request.POST['minquantity']
        product_pic=request.FILES['productpic']
        discount=request.POST['discount']
        finalprice=request.POST['finalprice']
        brand = request.POST['brand']
        product_slug = Product.objects.filter(slug=slug).exists()
        category_id=Product.objects.filter(Product_ID=product_id).exists()

        if product_slug or category_id:
            msg='Product Already Exists'
        else:    
        
            Products=Product.objects.create(Product_name=porduct_name,Product_ID=product_id,slug=slug,Min_value=minquandity,Price=product_price,Discount=discount,brand=brand,final_total=finalprice,
                                         Description=description,Unit_type=unit,Product_category_id =category,onstock=True,product_image=product_pic,Supermarket_name=supermrk)
        
            return redirect('smsuser:productslist')



    supermrk=Supermarket.objects.get(user=request.user)
    return render(request,'smsuser/addproduct.html',{'cat':catagory,'supermarketdetails':supermrk})

@login_required(login_url='/smsuser/login')
def categories(request):
   msg = request.GET.get('msg', '')
   catagories=Categories.objects.filter(Supermarket_name__user=request.user).order_by('-id')
   
   paginator = Paginator(catagories, 10) 
   page_number = request.GET.get('page')
   page_obj = paginator.get_page(page_number)
   supermrk=Supermarket.objects.get(user=request.user)
   return render(request,'smsuser/categories.html',{'catagories': page_obj,'supermarketdetails':supermrk})

@login_required(login_url='/smsuser/login')
def addcategories(request):
    try:
        msg=''
        if request.method=='POST':
            name=request.POST['catagoryname']
            description=request.POST['description']
            slug=request.POST['slug']
            categoryid=request.POST['categoryid']
            image=request.FILES['catagorypic']
            super=Supermarket.objects.get(user=request.user)
            category = Categories.objects.filter(slug=slug,Supermarket_name__id=super.id).exists()
            category_id=Categories.objects.filter(category_ID=categoryid,Supermarket_name__id=super.id).exists()
           
            if category or category_id:
                msg='Category Already Exist'
                return redirect('smsuser:categories')
            else:
                category_=Categories.objects.create(category_name=name,category_ID=categoryid,Supermarket_name_id=super.id, slug=slug,category_image=image,category_description=description)    
                msg='New Category Added'
                return redirect('smsuser:categories')
    except:
        pass        
    supermrk=Supermarket.objects.get(user=request.user)
    return render(request,'smsuser/addcategory.html',{'supermarketdetails':supermrk})

@login_required(login_url='/smsuser/login')
def productdetails(request,pid):
    product=Product.objects.get(id=pid)
    supermrk=Supermarket.objects.get(user=request.user)
    return render(request,'smsuser/productdetails.html',{'product':product,'supermarketdetails':supermrk})    
    

@login_required(login_url='/smsuser/login')
def updateproduct(request,pid):
    try:
        catagory=Categories.objects.filter()
        product=Product.objects.get(id=pid)
        if request.method=='POST':
            product.Product_name=request.POST['productname']
            product.Product_ID=request.POST['productID']
            product.Product_category_id=request.POST['productcat']
            product.Price=request.POST['price']
            product.Description=request.POST['description']
            product.Unit_type=request.POST['unit']
            product.Min_value=request.POST['minquantity']
            product.final_total=request.POST['finalprice']
            product.Discount=request.POST['discount']
            if 'productpic' in request.FILES:
                product.product_image = request.FILES['productpic']
                # Save the updated product
            product.save()
            return redirect('smsuser:productslist')
    except:
        return redirect('smsuser:productslist')
    supermrk=Supermarket.objects.get(user=request.user)
    return render(request,'smsuser/productedit.html',{'product':product,'catagory':catagory,'supermarketdetails':supermrk})

@login_required(login_url='/smsuser/login')
def updatecategory(request,cid):
    try:
        catagory=Categories.objects.get(id=cid)
        print(catagory)
        
        if request.method == 'POST':
            catagory.category_name=request.POST['category_name']
            catagory.category_description=request.POST['category_description']
            catagory.slug=request.POST['slug']
            catagory.category_ID=request.POST['category_ID']
            if 'category_image' in request.FILES:
                catagory.category_image = request.FILES['category_image']


            # Save the updated category
            catagory.save()
            return redirect('smsuser:categories')
    except:
        pass
    supermrk=Supermarket.objects.get(user=request.user)
    return render(request,'smsuser/editcategory.html',{'catdata':catagory,'supermarketdetails':supermrk})

@login_required(login_url='/smsuser/login')
def coupon(request):
    supermrk=Supermarket.objects.get(user=request.user)
    coupn=Coupon.objects.filter(supermarket__user=request.user)
    return render(request,'smsuser/coupons.html',{'coupons':coupn,'supermarketdetails':supermrk})

@login_required(login_url='/smsuser/login')
def delete(request,cid):
    try:
        catagory=Categories.objects.get(id=cid)
        catagory.delete()
        return redirect('smsuser:categories')  
    except:
        return redirect('smsuser:categories') 
    
@login_required(login_url='/smsuser/login')
def deleteproduct(request,pid):
    try:
        product=Product.objects.get(id=pid)
        product.delete()
        return redirect('smsuser:productslist')  
    except:
        return redirect('smsuser:categories')   

@login_required(login_url='/smsuser/login')
def instock(request,pid):
    try:
        product=Product.objects.get(id=pid)
        product.onstock=True
        product.save()
        return redirect('smsuser:productslist')  
    except:
        return redirect('smsuser:productlist')  
    
@login_required(login_url='/smsuser/login')
def activecoupon(request,cid):
    try:
        coupons=Coupon.objects.get(id=cid)
        coupons.active=True
        coupons.save()
        return redirect('smsuser:coupons')  
    except:
        return redirect('smsuser:coupons')    

login_required(login_url='/smsuser/login')
def deactivecoupon(request,cid):
    try:
        coupons=Coupon.objects.get(id=cid)
        coupons.active=False
        coupons.save()
        return redirect('smsuser:coupons')  
    except:
        return redirect('smsuser:coupons')   

@login_required(login_url='/smsuser/login')
def deletecoupon(request,cid):
    try:
        coupon=Coupon.objects.get(id=cid)
        coupon.delete()
        return redirect('smsuser:coupons')  
    except:
        return redirect('smsuser:coupons')             

@login_required(login_url='/smsuser/login')
def outofstock(request,pid):
    try:
        product=Product.objects.get(id=pid)
        product.onstock=False
        product.save()
        return redirect('smsuser:productslist')  
    except:
        return redirect('smsuser:categories')            

@login_required(login_url='/smsuser/login')
def addcoupon(request):
    if request.method=='POST':
        couponcode=request.POST['couponcode']
        discount=request.POST['discount']
        min_value=request.POST['minvalue']
        validity=request.POST['validity']
        supermark=Supermarket.objects.get(user=request.user)

        coupon=Coupon.objects.create(code=couponcode,discount=discount,min_purchase=min_value,expiry_date=validity,
                                     active=True,supermarket=supermark)
        return redirect('smsuser:coupons')

    supermrk=Supermarket.objects.get(user=request.user)
    return render(request,'smsuser/addcoupon.html',{'supermarketdetails':supermrk})

@login_required(login_url='/smsuser/login')
def updatecoupon(request,cid):
    coupon=Coupon.objects.get(id=cid)
    formatted_date = coupon.expiry_date.strftime("%Y-%m-%d")
    print(formatted_date)
    if request.method=='POST':
        coupon.code=request.POST['code']
        coupon.discount=request.POST['discount']
        coupon.min_purchase=request.POST['minvalue']
        coupon.expiry_date=request.POST['validity']
        coupon.save()
        return redirect('smsuser:coupons')
    supermrk=Supermarket.objects.get(user=request.user)
    return render(request,'smsuser/updatecoupon.html',{'coupon':coupon,'date':formatted_date,'supermarketdetails':supermrk})

@login_required(login_url='/smsuser/login')
def orders(request):
    if request.method=='POST':
        keyword=request.POST['keyword']
        
        searchresults=Order.objects.filter(Q(OrderId__icontains=keyword) | Q(user__customer_name__icontains=keyword))[:10].values('OrderId', 'user__customer_name','id')
        serialized_results=[dict(order) for order in searchresults]
        
        return JsonResponse({'searchdata':serialized_results},safe=False)

    Orders=Order.objects.filter(Supermarketname__user=request.user).order_by('-created_at')
    print(Orders)
    paginator = Paginator(Orders, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    supermrk=Supermarket.objects.get(user=request.user)
    return render(request,'smsuser/orders.html',{'orders':page_obj,'supermarketdetails':supermrk})

@login_required(login_url='/smsuser/login')
def orderdetails(request,oid):
    total=0
    order=Order.objects.get(OrderId=oid)
    orderitems=OrderItem.objects.filter(order=order)
    for orders in orderitems:
        total += orders.quantity*orders.price
    discount=(order.discount/100)*total
    print(orderitems)
    supermrk=Supermarket.objects.get(user=request.user)
    return render(request,'smsuser/orderdetails.html',{'order':order,'grandtotal':order.total_price,'orderdetails':orderitems,'discount':round(float(discount),2),'total':round(total,2),'discountedprice':round(float(total-discount),2),'supermarketdetails':supermrk})

@login_required(login_url='/smsuser/login')
def orderaccept(request,oid):
    order=Order.objects.get(OrderId=oid)
    order.status='Accepted'
    order.save()
    return redirect('smsuser:orderdetails',oid)

@login_required(login_url='/smsuser/login')
def orderreject(request,oid):
    order=Order.objects.get(OrderId=oid)
    order.status='Rejected'
    order.save()
    return redirect('smsuser:orderdetails',oid)
    


@login_required(login_url='/smsuser/login')
def addbanner(request):
    if request.method=='POST':
        if request.FILES.get('top') or request.POST.get('brandtop'):
            brand=request.POST.get('brandtop','')
            Bannerobj,created= Banner.objects.get_or_create(title='Top')
            if request.FILES.get('top'):
                Bannerobj.image=request.FILES['top']
            Bannerobj.offerbrand=brand
            Bannerobj.save()

        if request.FILES.get('mid') or request.POST.get('brandmid'):
            brand=request.POST.get('brandmid','')
            Bannerobj,created= Banner.objects.get_or_create(title='Mid')
            if request.FILES.get('mid'):
                Bannerobj.image=request.FILES['mid']
            Bannerobj.offerbrand=brand
            Bannerobj.save()    

        if request.FILES.get('bottom') or request.POST.get('brandbottom'):
            brand=request.POST.get('brandbottom','')
            Bannerobj,created= Banner.objects.get_or_create(title='Bottom')
            if request.FILES.get('bottom'):
                Bannerobj.image=request.FILES['bottom']
            Bannerobj.offerbrand=brand  
            Bannerobj.save()   
        return redirect('smsuser:addbanner')    
    bannerTop=Banner.objects.filter(title='Top')
    supermrk=Supermarket.objects.get(user=request.user)
    bannermid=Banner.objects.filter(title='Mid')
    bannerbottom=Banner.objects.filter(title='Bottom')     
    return render(request,'smsuser/addbanner.html',{'bannertop':bannerTop,'bannermid':bannermid,'bannerbottom':bannerbottom,'supermarketdetails':supermrk})

@login_required(login_url='/smsuser/login')
def deletebanner(request,title):
    Bannerobj=Banner.objects.get(title=title)
    Bannerobj.delete()
    return redirect('smsuser:addbanner')

@login_required(login_url='/smsuser/login')
def report(request):
    return render(request,'smsuser/feedback.html')

def signup(request):
  msg=''
  try:
        if request.method == 'POST':
            username=request.POST['username']
            password=request.POST['password']
            name = request.POST['name']
            address=request.POST['address']
            contact=request.POST['phone']
            user = User.objects.create_user(username=username, password=password, is_supermarket=True)
            supermarket=Supermarket.objects.create(name=name,user=user,address=address,contact_number=contact)
            return redirect('smsuser:login')
        else:
            msg='Some error encountered Check the details you provided'
  except:       
        msg='some tecnical error encountered'        


  return render(request,'smsuser/signup.html',{'data':msg})

def logins(request):
    msg=''
    if request.method == 'POST':
        # print('hh')
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None and user.is_supermarket:
                login(request, user)
                return redirect('smsuser:home') 
        else:   
                msg='Wrong Username or password'


    return render(request,'smsuser/login.html',{'status':msg})

@login_required(login_url='/smsuser/login')
def smlogout(request):
   logout(request)  
   return redirect('smsuser:login')

@login_required(login_url='/smsuser/login')
def checkcatagoryslug(request):
    if request.method == 'POST':
        slug = request.POST.get('slug', 0)
        catid = request.POST.get('catid', 0)
        if catid != 0:
            cata = Categories.objects.filter(category_ID=catid,Supermarket_name__user=request.user).exists()
            if cata:
                return JsonResponse({'msg': 'Taken'})
            else:
                return JsonResponse({'msg': 'Available'})
        if slug !=0:
            slugs = Categories.objects.filter(slug=slug,Supermarket_name__user=request.user).exists()
            if slugs:
                return JsonResponse({'msg':'Taken'})
            else:
                return JsonResponse({'msg':'Available'})
    else:
        return JsonResponse('error')   

@login_required(login_url='/smsuser/login')
def checkproductslug(request):
    if request.method == 'POST':
        slug = request.POST.get('slug', 0)
        proid = request.POST.get('proid', 0)
        if proid != 0:
            product = Product.objects.filter(Product_ID=proid,Supermarket_name__user=request.user).exists()
            if product:
                return JsonResponse({'msg': 'Taken'})
            else:
                return JsonResponse({'msg': 'Available'})
        if slug !=0:
            slugs = Product.objects.filter(slug=slug,Supermarket_name__user=request.user).exists()
            if slugs:
                return JsonResponse({'msg':'Taken'})
            else:
                return JsonResponse({'msg':'Available'})
    else:
        return JsonResponse('error')          

            
          

       
           