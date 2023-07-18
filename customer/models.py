from datetime import timezone
from django.db import models
from smsuser.models import Supermarket,User

# Create your models here.

class Customer(models.Model):
    customer_email=models.CharField(max_length=50)
    user=models.OneToOneField(User, on_delete=models.CASCADE,default='')
    customer_name = models.CharField(max_length=50,null=True,default='')
    Mobile = models.CharField(max_length=50,null=True,default='')
    Street = models.CharField(max_length=50,null=True,default='')
    City = models.CharField(max_length=50,null=True,default='')
    House=models.CharField(max_length=50,null=True,default='')
    BHT_Appartment = models.BooleanField(default=True)
    Landmark=models.CharField(max_length=50,null=True,default='')
    Province=models.CharField(max_length=50,null=True,default='')
    District=models.CharField(max_length=50,null=True,default='')
    Postalcode=models.CharField(max_length=50,null=True,default='')

    

class Categories(models.Model):    
    category_name=models.CharField(max_length=50)
    category_ID=models.CharField(max_length=20,null=False)
    category_image=models.ImageField(upload_to="customer/",null=True)
    category_description=models.TextField(null=True)
    slug=models.CharField(max_length=50,null=False)
    Supermarket_name=models.ForeignKey(Supermarket,on_delete=models.CASCADE,null=True)

  

class Product(models.Model):
    Product_name=models.CharField(max_length=40)
    Product_ID=models.CharField(max_length=20,unique=False)
    slug=models.CharField(max_length=50,null=True,unique=True)
    brand=models.CharField(max_length=30, default='BHT')
    Min_value=models.CharField(max_length=50)
    Supermarket_name=models.ForeignKey(Supermarket,on_delete=models.CASCADE)
    Product_category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    onstock=models.BooleanField(default=True)
    Unit_type= models.CharField(max_length=20)
    Price=models.FloatField()
    Description=models.TextField(null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    product_image=models.ImageField(upload_to="customer/",null=True)
    Discount=models.FloatField()  
    final_total = models.FloatField()

    
    

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')

    def total_price(self):
        return sum(item.subtotal() for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def subtotal(self):
        return self.price * self.quantity
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    TIMESLOT_CHOICES = [
        ('10 AM-12 PM', '10:00 AM - 12:00 PM'),
        ('12 PM-2 PM', '12:00 PM - 2:00 PM'),
        ('2 PM-4 PM', '2:00 PM - 4:00 PM'),
        ('4 PM-6 PM', '4:00 PM - 6:00 PM'),
        ('6 PM-8 PM', '6:00 PM - 8:00 PM'),
        ('8 PM-10 PM', '8:00 PM - 10:00 PM'),
        ('10 PM-12 AM', '10:00 PM - 12:00 AM'),


        # Add more time slot choices as needed
    ]

    DELIVERY=[('now', 'Delivery Now'), ('later', 'Delivery Later')]

    
    Supermarketname=models.ForeignKey(Supermarket,on_delete=models.CASCADE)
    OrderId=models.CharField(max_length=20,null=True,unique=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    delivery_option = models.CharField(max_length=10, choices=DELIVERY,null=True)
    time_slot = models.CharField(max_length=50, choices=TIMESLOT_CHOICES, blank=True, null=True)
    paymentmethod=models.CharField(max_length=4,default='COD')
    products = models.ManyToManyField(Product, through='OrderItem')
    couponcodeapplied=models.BooleanField(default=False)
    discount=models.DecimalField(max_digits=5, decimal_places=2,default=0)
    
    # Add more fields as needed

    def __str__(self):
        return f"Order #{self.OrderId} - User: {self.user.customer_name}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.price * self.quantity    
    

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    supermarket=models.ForeignKey(Supermarket,on_delete=models.CASCADE,default='')
    expiry_date = models.DateTimeField()
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    active = models.BooleanField(default=True)

    def is_valid(self):
        return self.active and self.expiry_date > timezone.now()

class UserCoupon(models.Model):
    user =  models.ForeignKey(Customer,on_delete=models.CASCADE, null= True)
    coupon = models.ForeignKey(Coupon,on_delete = models.CASCADE, null = True)
    order  = models.ForeignKey(Order,on_delete=models.SET_NULL,null = True,related_name='order_coupon')
    used = models.BooleanField(default = False)  


    
        






