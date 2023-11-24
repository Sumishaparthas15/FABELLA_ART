from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .manager import UserManager 
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.db.models import Sum


class Profile(AbstractUser):
    username           = models.CharField(null=True, blank=True, max_length=150)
    password           = models.CharField(max_length=128, verbose_name='password')
    email              = models.EmailField(unique=True,null=True,blank=True)
    number             = models.CharField(max_length=10,null=True,blank=True)
    is_verified        = models.BooleanField(default=False)
    email_token        = models.CharField(max_length=100, null=True, blank=True)
    forgot_password    = models.CharField(max_length=100, null=True, blank=True)
    last_login_time    = models.DateTimeField(null=True, blank=True)
    last_logout_time   = models.DateTimeField(null=True, blank=True)
    profile_photo      = models.ImageField(upload_to='products', null=True, blank=True)
    referral_code      = models.CharField(max_length=100, null=True, unique=True)
    referral_amount    = models.IntegerField(default=0)
    wallet_bal= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def _str_(self):
        return self.email
    
class Address(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(null=True,blank=True)
    number = models.CharField(max_length=20)
    address1 = models.CharField(max_length=100,blank=True, null=True)
    
    country = models.CharField(max_length=50,default=None)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10,default=None)
    

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

class Category(models.Model):
    category_name=models.CharField(max_length=100,unique=True)
    category_offer_description = models.CharField(max_length=100, null=True, blank=True)
    category_offer = models.PositiveBigIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)  # New field
    
    def get_url(self):
        return reverse('products_by_category', args=[str(self.id)])
   

    def _str_(self):
        return self.category_name
    
class Sub_category(models.Model):
    main_category=models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_category_name=models.CharField(max_length=100,unique=True)
    
    def _str_(self):
        return self.sub_category_name

class Product(models.Model):
   
    product_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default='')
    category     = models.ForeignKey(Category,on_delete=models.CASCADE , blank=True , null=True)
    Sub_category   = models.ForeignKey(Sub_category,on_delete=models.CASCADE , null=True , blank=True)
    stock = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/' , blank=True , null= True)
    
    deleted        =     models.BooleanField(default=False)
    product_offer =      models.DecimalField(max_digits=5, decimal_places=2,max_length=100, blank=True, null=True)
    

    def _iter_(self):
        yield self.id
     
class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
   
    
    images = models.ImageField(upload_to='products/')
    

class Cart(models.Model):
       user =  models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
       product =  models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
       cart_id = models.CharField(max_length=250,blank=True)    
       date_added = models.DateField(auto_now_add=True)
       quantity =  models.IntegerField(default=0)
       image = models.ImageField(upload_to='products',null=True, blank=True ) 
       
       @property
       def sub_total(self):
            return self.product.price * self.quantity

       def _str_(self):
          return f"Cart: {self.user.username} - {self.product} - Quantity: {self.quantity}"


   
class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for monetary amounts
    payment_type = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    date = models.DateField(default=date.today)
    

    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('on_hold', 'On Hold')
    )

    status = models.CharField(max_length=100, choices=ORDER_STATUS, default='pending')
    message = models.TextField(null=True)  # Use TextField, not TextFields

    # You have some missing fields like tracking_no, created_at, and updated_at
    tracking_no = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id} - Tracking No: {self.tracking_no}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
   # Use DecimalField for the price
    image = models.ImageField(upload_to='products', null=True, blank=True)

    def __str__(self):
        return f'Order Item for Order {self.order.id} - Product: {self.product.name}'
    
class WishList(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products',null = True,blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Wishlist Item:{self.product.product_name}"
    
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_text = models.TextField()
    review_rating = models.CharField(choices=RATING,max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_review_rating(self):
        return self.review_rating

class ReplyMessage(models.Model):
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE)
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)  # You can set a default admin user ID here
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField()
    minimum_amount  =  models.PositiveIntegerField(default=500)
    expiration_date = models.DateField()
    status = models.BooleanField(default=True)
    

    def __str__(self):
        return self.code    

class Offer(models.Model):
    title = models.CharField(max_length=100)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    

    def __str__(self):
        return self.title 

class Wallet(models.Model):
    user  =models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_credit = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20,blank=True)

    def _str_(self):
        return f"{self.amount} {self.is_credit}"

    def _iter_(self):
        yield self.pk        
        
class Banner(models.Model):
    image           = models.ImageField(upload_to='products/', blank=True, null=True)
    description     =models.CharField(max_length=100)

class Contact(models.Model):
    user  =models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    message = models.CharField(max_length=1000, null=True, blank=True)
