from django.shortcuts import render , redirect
from django.contrib.auth.models import User
import random
from django.conf import settings
from app1.models import *
from django.core.exceptions import ObjectDoesNotExist
import http.client
from django.contrib import messages , auth
from django.shortcuts import redirect,render
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login,logout
from django.core.paginator import Paginator
from django.core.mail import send_mail
import smtplib
import secrets
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import crypt
import random
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from random import randint
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.http import Http404
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import * 
from django.http import JsonResponse
import razorpay
from django.db.models import F, Sum


import json
from decimal import Decimal

# ADMIN LOGIN
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def admin_login(request):
    if 'admin' in request.session:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
           
           
            user = authenticate(request, email= email, password=password)
    
            if user is not None and user.is_superuser:
                login(request, user)  
                request.session['admin'] = email
                return redirect('dashboard')  
            else:
                messages.error(request, 'Email or password is invalid')
                return render(request, 'main/admin_login.html')
        else:
            return render(request,'main/admin_login.html')
# ADMIN LOGOUT
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def admin_logout(request):
    if 'admin' in request.session:
        request.session.flush()
    logout(request)
    return redirect('admin_login')

def dashboard(request):
    return render(request,'main/dashboard.html')
# CUSTOMER
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def customer(request):
    customer_list = Profile.objects.all()
    print(customer_list)
    paginator = Paginator(customer_list, 500)  # Show 10 customers per page
    page = request.GET.get('page')
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    return render(request, 'main/customer.html', {'customers': customers})
def block_customer(request, customer_id):
    customer = get_object_or_404(Profile, id=customer_id)
    customer.is_active = False
    customer.save()
    return redirect('customer')
def unblock_customer(request, customer_id):
    customer = get_object_or_404(Profile, id=customer_id)
    customer.is_active = True
    customer.save()
    return redirect('customer')

# CATEGORY
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def category(request):
    if 'admin' in request.session:
        categories = Category.objects.all().order_by('id')
        
        
        paginator = Paginator(categories, per_page=3)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'categories': page_obj,
        }
        return render(request, 'main/category.html', context)
    else:
        return redirect('admin')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache          
def add_category(request):
    if 'admin' in request.session:
        if request.method  == 'POST':
           
            category_name       =   request.POST.get('category_name')
            category = Category.objects.create(category_name = category_name)   
            category.save() 

            return redirect('category')  
        return render(request, 'main/addcategory.html') 
    else:
        return redirect ('admin')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def update_category(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return HttpResponse("Error")

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            category.category_name           =  category_name
        category.save()
        return redirect('category')

    context = {'category': category}
    return render(request, 'main/editcategory.html', context)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def edit_category(request, category_id):
    if 'admin' in request.session:
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return render(request, 'category_not_found.html')

        context = {'category': category}
        return render(request,'main/editcategory.html', context)
    else:
        return redirect ('admin')
def delete_category(request,category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'category_not_found.html')

    category.delete()

    
    return redirect('category')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def sub_category(request):
    if 'admin' in request.session:
        subcategories = Sub_category.objects.all()
        maincategories = Category.objects.all()
        maincategory_names = {}
        maincategory_ids = {}
        for sub in subcategories:
            maincategory_names[sub.id] = sub.main_category.category_name
            maincategory_ids[sub.id] = sub.main_category.id
                  
        paginator = Paginator(subcategories, per_page=3)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'categories': page_obj,
            'subcategories' : subcategories,
            'maincategories' :maincategories,
            'maincategory_names': maincategory_names,
            'maincategory_ids': maincategory_ids,
        }
        

        return render(request,'main/subcategory.html',context)
    else:
        return redirect('admin')
def add_sub_category(request):
    main_category=Category.objects.all()
    context={
        'main_category':main_category
    }
       
    if 'admin' in request.session: 
        if request.method  == 'POST':
            cat      = request.POST.get('categories')
            print(cat)
            sub_category_name   =request.POST.get('name')
            main = Category.objects.get(id=cat)

            
            sub = Sub_category.objects.create(main_category=main,sub_category_name=sub_category_name)
            sub.save() 

            return redirect('sub_category')  
        return render(request,'main/addsubcategory.html',context)
    else:
        return redirect ('admin')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def edit_sub_category(request, sub_category_id):
    cat = Category.objects.all()
    if 'admin' in request.session:
        try:
            sub_category =  Sub_category.objects.get(id=sub_category_id)
        except  Sub_category.DoesNotExist:
            return render(request, 'category_not_found.html')

        context = {'sub_category': sub_category,'cat':cat,
        }
        return render(request, 'main/editsubcategory.html', context)
    else:
        return redirect ('admin')   
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def update_sub_category(request, sub_category_id):
    main_category = Category.objects.all()
    sub_category = Sub_category.objects.get(id=sub_category_id)  # Use get() instead of filter()

    if request.method == 'POST':
        new_name = request.POST.get('sub_category_name')
        new_main_id = request.POST.get('main_category')
        sub_category.sub_category_name = new_name
        # sub_category.main_category_id = new_main_id
        sub_category.save()

        return redirect('sub_category')

    return render(request, 'main/editsubcategory.html')
def delete_sub_category(request, sub_id):
    try:
        sub_category = Sub_category.objects.get(id=sub_id)
    except Sub_category.DoesNotExist:
        return render(request, 'category_not_found.html')

    sub_category.delete()

    sub_category = Sub_category.objects.all()
    context = {'categories': sub_category}

    return redirect('sub_category')

#  PRODUCT
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def product(request):
    if 'admin' in request.session:
        
        products = Product.objects.all().order_by('id')       
        paginator = Paginator(products, 3)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        

        context = {
            'page_obj': page_obj,
            'products':products,
             
        }
        return render(request, 'main/product.html', context)
    else:
        return redirect('admin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def add_product(request):
    categories = Category.objects.all()

    if 'admin' in request.session:
        if request.method == 'POST':
            product_name = request.POST.get('product_name')
            description = request.POST.get('description')
            subcategory_id = request.POST.get('subcategory_id')
            stock = request.POST.get('stock')
            price = request.POST.get('price')
            images = request.FILES.getlist('images')  # Get all uploaded images
            size = request.POST.get('size')  # Add size

            try:
                subcategory_id = Sub_category.objects.get(id=subcategory_id)
                main_category_id = subcategory_id.main_category_id
            except Sub_category.DoesNotExist:
                return HttpResponse("Sub Category not found")

            product = Product.objects.create(
                product_name=product_name,
                description=description,
                Sub_category=subcategory_id,
                category_id=main_category_id,
                stock=stock,
                price=price,
                size=size,  # Add size
            )

            for image in images:
                Images.objects.create(product=product, images=image)

            return redirect('product')

        context = {'categories': categories}
        return render(request, 'main/addproduct.html', context)
    else:
        return redirect('admin')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def edit_product(request, product_id):
    if 'admin' in request.session:
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
        
            return render(request, 'product_not_found.html')    
        
        categories = Category.objects.all()
        context = {
            'product'    : product,
            'categories' : categories,
        }

        return render(request, 'main/editproduct.html', context)
    else:
        return redirect('admin')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.description = request.POST.get('description')
        category_name = request.POST.get('category')
        category = Category.objects.get(category_name=category_name)
        product.category = category
        product.stock = request.POST.get('stock')
        product.price = request.POST.get('price')
        size = request.POST.get('size')  # Add size
        images = request.FILES.getlist('images')  # Get multiple images

        if size:
            product.size = size  # Update the size field

        # Only update the images if new ones are provided
        if images:
            product.image = images[0]  # Update the first image

        product.save()

        # If new images are provided, update them
        for image in images[1:]:
            Images.objects.create(product=product, images=image)

        return redirect('product')
    else:
        context = {
            'product': product
        }
        return render(request, 'main/product.html', context)
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return render(request, 'category_not_found.html')

    product.delete()

    return redirect('product')

#ORDERS 
def orders(request):
    if 'admin' in request.session:
        orders = Order.objects.all()

        
        print(orders)

        context = {
            'orders': orders,
        }

        return render(request, 'main/adminorder.html', context)
    else:
        # Handle the case where "admin" is not in the session (e.g., redirect or display an error message)
        # For example, you can redirect to a login page or display an error message.
        return render(request, 'main/admin_order_not_authorized.html')
def update_order_status(request):
    if request.method == "POST":
        print(request.POST)  # Debug: Print the POST data to the console
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            
            messages.success(request, f"Order #{order.id} status has been updated to {new_status}.")
        except Order.DoesNotExist:
            messages.error(request, f"Order with ID {order_id} does not exist.")
        
    return redirect('orders')  

def search_customer(request):
    q = request.GET.get('q', '')  # Get the 'q' parameter from the request or set it to an empty string

    # Filter customers based on the query 'q'
    customers = Profile.objects.filter(username__icontains=q) 

    context = {
        'customers': customers
    }

    return render(request, 'main/customer.html', context)
@never_cache
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def coupon(request):
    if 'admin' in request.session:
        coupons = Coupon.objects.all().order_by('id')
        context = {'coupons': coupons}
        return render(request,'main/coupon.html', context)
    else:
        return redirect('admin')

def addcoupon(request):
    if request.method == 'POST':
        code    = request.POST.get('Couponcode')
        discount  = request.POST.get('dprice')
        minimum_amount = request.POST.get('amount')
        expiration_date = request.POST.get('date')  
        coupon = Coupon(code=code, discount=discount, minimum_amount=minimum_amount,expiration_date=expiration_date)
        coupon.save()
        return redirect('coupon')
    


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def editcoupon(request,coupon_id):
    if 'admin' in request.session:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
        except Section.DoesNotExist:
            return render(request, 'subcategory_not_found.html')
        context = {'coupon': coupon}
        return render(request, 'main/edit_coupon.html', context)
    else:
        return redirect ('admin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def update_coupon(request, id):
    # Use get_object_or_404 to retrieve the coupon or return a 404 page if it doesn't exist
    coupon = get_object_or_404(Coupon, id=id)
    if request.method == 'POST':
        code = request.POST.get('Couponcode')
        discount = request.POST.get('price')
        minimum_amount = request.POST.get('amount')
        expiration_date = request.POST.get('date')
        # Check if coupon_code and discount_price are not null before updating
        if code:
            coupon.code = code
        if discount:
            coupon.discount = discount
        coupon.minimum_amount = minimum_amount
        coupon.expiration_date = expiration_date
        coupon.save()  # Save the updated coupon object here
        return redirect('coupon')
    context = {'coupon': coupon}
    return render(request, 'main/edit_coupon.html', context)

def delete_coupon(request,coupon_id):
    try:
        coupon= Coupon.objects.get(id=coupon_id)
    except Coupon.DoesNotExist:
        return render(request, 'category_not_found.html')
    coupon.delete()
    coupons = Coupon.objects.all()
    context = {'coupons': coupons}
    return redirect('coupon')


#-----------------------------------------------------------------------------------------------------------
#------------------------------------------------USER SIDE--------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

def base(request):
    return render(request,'base.html')
def home(request):
    return render(request,'main/home.html')

# PRODUCT
def shop(request, category_id=None):
    products = None
    product_count = 0

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
        product_count = products.count()
    else:
        products = Product.objects.all()
        product_count = products.count()

    # Price filter
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if min_price is not None:
        products = products.filter(price__gte=min_price)
    if max_price is not None:
        products = products.filter(price__lte=max_price)

    context = {
        'products': products,
        'product_count': product_count,
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, 'main/shop.html', context)

def product_list(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 12)  # 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'main/shop.html', {'products': products})
def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_images = product.images_set.all()  # Access the related images using 'images_set'
    review_form = ProductReviewForm()

    context = {
        'product': product,
        'product_images': product_images,
        'review_form': review_form,
    }

    return render(request, 'main/productdetails.html', context)


# SIGN UP
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def signup(request):
    if 'email' in request.session:
        return redirect('home')
    elif request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('number')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if not (name and email and password and phone_number and confirmpassword):
            messages.info(request, "!Please Fill Required Fields")
            return redirect('signup')

        if password != confirmpassword:
            messages.info(request, "Password Mismatch")
            return redirect('signup')

        if Profile.objects.filter(email=email).exists():
            messages.info(request, "Email Already Taken")
            return redirect('signup')
        if Profile.objects.filter(number=phone_number).exists():
            messages.info(request, "Phone Number Already Taken")
            return redirect('signup')

        # Create the user using CustomUser model
        user = Profile.objects.create_user(email=email, password=password, username=name, number=phone_number)
        user.save()

        message = generate_otp()
        sender_email = "sumishasudha392@gmail.com"
        receiver_mail = email
        password_email = "xhywblrweffmdeyj"

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password_email)
                server.sendmail(sender_email, receiver_mail, message)

        except smtplib.SMTPAuthenticationError:
            messages.error(request, 'Failed to send OTP email. Please check your email configuration.')
            return redirect('login')

        request.session['email'] = email
        request.session['otp'] = message
        messages.success(request, 'OTP is sent to your email')

        return redirect('verify_signup')

    return render(request, 'main/signup.html')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def verify_signup(request):
    context = {
        'messages': messages.get_messages(request)
    }
    if request.method == "POST":
        
        user      = Profile.objects.get(email=request.session['email'])
      
        x         =  request.session.get('otp')
        otp       =  request.POST.get('otp')

        
      
        if otp == x:
           
            user.is_verified = True
            user.save()
            del request.session['email'] 
            del request.session['otp']
        
            login(request,user)
            messages.success(request, "Signup successfull!")
            return redirect('userlogin')
        else:
            user.delete()
            messages.info(request,"invalid otp")
            del request.session['email']
            return redirect('signup')
    return render(request,'main/verify_otp.html',context)
def generate_otp(length = 6):
    return ''.join(secrets.choice("0123456789") for i in range(length)) 
def user_login(request):
    if 'email' in request.session:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')  # Use 'email' instead of 'username'
        password = request.POST.get('password')

        try:
            user = Profile.objects.get(email=email)
            if not user.is_superuser:
                if user.check_password(password):
                    # Log in the user
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Email and password are invalid!')
            else:
                messages.error(request, "Sorry! You can't login here.")  # Corrected the error message string
        except ObjectDoesNotExist:  # Handle the case where the profile doesn't exist
            messages.error(request, 'This email does not have a linked account.')

    return render(request, 'main/login.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache 
def userlogout(request):
    if 'email' in request.session:
        request.session.flush()
        logout(request)
    return redirect('userlogin')

# USER PROFILE
def profile(request):
    user = request.user
    if not user.is_superuser:
        
        category = Category.objects.all().order_by('-id')
        context = {
            'main_category':category
        }
    else:
        return redirect('verified_login')
    return render(request,'main/userprofile.html',context)
@login_required(login_url='verified_login')
def profile_update(request):  
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        mobile = request.POST.get('phoneNo')
        email = request.POST.get('email')  
        password = request.POST.get('currentPassword')
        user_id = request.user.id
        user = Profile.objects.get(id=user_id) 
        user.full_name = full_name
        user.ph_no = mobile
        user.email = email
        if password == None and password != "":
            user.set_password = password
        user.save()
        
    return redirect('profile')

# ADDRESS
@login_required(login_url='verified_login')   
def address(request):
    address_list = Address.objects.filter(user=request.user).order_by('-id')
    context = {
        'address_list':address_list,
    }
    return render(request,'main/useraddress.html',context)
@login_required(login_url='verified_login')
def add_address(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        
        
        new = Address.objects.create(
            user = request.user,
            firstname = fname,
            lastname = lname,
            email = email,
            number = phone,
            address1 = address,
            country = country,
            state = state,
            city = city,
            zip = pincode
        )
        new.save()
        return redirect('add_address') 
        
    return render(request,'main/addaddress.html')  
def shipping_add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            # Process the form data and save the address
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('shipping_add_address')
    else:
        form = AddressForm()

    return render(request, 'main/billingaddress.html', {'form': form})   
@login_required(login_url='verified_login')
def edit_address(request,id):
    user = request.user
    newaddress = Address.objects.get(id=id,user=user)
    context = {
        'newaddress':newaddress,
    }
    return render(request,'main/editaddress.html',context)
@login_required(login_url='verified_login')
def update_address(request,id):
    update = Address.objects.get(id=id,user=request.user)
    if request.method == 'POST':
        update.firstname = request.POST.get('fname')
        update.lastname = request.POST.get('lname')
        update.email = request.POST.get('email')
        update.number = request.POST.get('phone')
        update.address1 = request.POST.get('address')
        update.country = request.POST.get('country')
        update.state = request.POST.get('state')
        update.city = request.POST.get('city')
        update.zip = request.POST.get('pincode')
        
        update.save()
        
        return redirect('address')   
@login_required(login_url='verified_login')   
def delete_address(request,id):
    try:
        address = Address.objects.get(id=id)
        address.delete()
    except address.DoesNotExist:
        return HttpResponse("Address Not Found")
    return redirect('address')
def verified_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

    
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            # Redirect to a specific page after login (e.g., the user's profile)
            return redirect('profile')  # Change 'profile' to the name of your profile view

        # If authentication fails, you can handle it here, such as displaying an error message

    return render(request, 'main/login.html')
@login_required
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the user's session with the new password
            messages.success(request, 'Your password was successfully changed.')
            return redirect('changepassword')  # Redirect back to the change password page
        else:
            messages.error(request, 'Please correct the error(s) below.')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'main/changepassword.html', {'form': form})




def search_product(request):
    if 'query' in request.GET:
        query = request.GET['query']


        if query:
            products = Product.objects.filter(Q(description__icontains=query) | Q(product_name__icontains=query))
            product_count = products.count()
       
    context = {
        'products':products,
        'product_count':product_count,
    }

    return render(request, 'main/shop.html',context)

# WISHLIST
def wishlist(request):
    user = request.user
    wish = WishList.objects.filter(user=user)
    return render(request, "main/wishlist.html", {"wish": wish})
def add_to_wish(request, product_id):
    print(product_id)
    try:
        product = Product.objects.get(id=product_id)
        print(product)

    except Product.DoesNotExist:
        # Handle the case where the product doesn't exist, for example, you can raise a 404 error.
        raise Http404("Product does not exist")

    user = request.user
    wishlist, created = WishList.objects.get_or_create(product=product, user=user)
    wishlist.save()
    return redirect("wishlist")
def remove_from_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        wish = WishList.objects.get(product=product, user=request.user)
    else:
        wish = WishList.object.get(product=product)
    wish.delete()
    return redirect("wishlist")

# FEEDBACK
def feedback(request):
    user = request.user
    feed = ProductReview.objects.filter(user=user)
    return render(request, "main/reviews.html", {"feed": feed})

def save_review(request, product_id):
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Assuming you are using the built-in user authentication
            review.product_id = product_id  # Set the product ID
            review.save()

            # Use reverse to get the URL of the product_details view
            product_details_url = reverse('product_details', args=[product_id])

            return redirect(product_details_url)
    else:
        form = ProductReviewForm()

    context = {'review_form': form}
    return render(request, 'main/productdetails.html', context)
    
def category_view(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'main/shop.html', {'category': category, 'products': products})









#cart
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart(request):
    if 'discount' in request.session:
        del request.session['discount']
    user = request.user
    cart_items = Cart.objects.filter(user=user).order_by('id')
    subtotal = 0
    total_dict = {}
    for cart_item in cart_items:
        if cart_item.quantity > cart_item.product.stock:
            messages.warning(request, f"{cart_item.product.product_name} is out of stock.")
            cart_item.quantity = cart_item.product.stock
            cart_item.save()
            item_price = Decimal(0) 
        
        else:
            item_price = cart_item.product.price * cart_item.quantity
            total_dict[cart_item.id] = item_price
            subtotal += item_price # Initialize item price as a Decimal


    shipping_cost = 100
    total = subtotal + shipping_cost
    coupons = Coupon.objects.all()
    
    if 'discount' in request.session:
        discount = float(request.session['discount'])  # Convert discount to float
        total -= discount 
    for cart_item in cart_items:
        cart_item.total_price = total_dict.get(cart_item.id, 0)
        cart_item.save()
        print(cart_items,"........cart item")
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total,
        'coupons': coupons,   
    }
    return render(request, 'main/cart.html', context)
@never_cache
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_to_cart(request, product_id):
    try: 
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('product_not_found')

    quantity = request.POST.get('quantity', 1)
    if not quantity:
        quantity = 1
    else:
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if created:
        cart_item.quantity = int(quantity)
    else:
        cart_item.quantity += int(quantity)

    cart_item.save()
    return redirect('cart')


def update_cart(request, product_id):
    cart_item = None
    cart_item = get_object_or_404(Cart, product_id=product_id, user=request.user)
    print(cart_item,"....................")
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity'))
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'message': 'Invalid quantity.'}, status=400)
    if quantity < 1:
        return JsonResponse({'message': 'Quantity must be at least 1.'}, status=400)
    cart_item.quantity = quantity
    cart_item.save()
    return JsonResponse({'message': 'Cart item updated.'}, status=200)

@never_cache
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def remove_from_cart(request,product_id):
    try:
        cart_item = Cart.objects.get(id=product_id, user=request.user)
        cart_item.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart')

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkout(request): 
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    subtotal = 0
    for cart_item in cart_items:
        
            itemprice = (cart_item.product.price) * (cart_item.quantity)
            subtotal = subtotal + itemprice
    shipping_cost = 10 
    discount = request.session.get('discount', 0)
    if discount:
        total =  subtotal + shipping_cost - discount if subtotal else 0    
    else:
        total =  subtotal + shipping_cost  if subtotal else 0
    addresses = Address.objects.filter(user=user)
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount_amount'  :  discount,
        'total': total,
        'addresses': addresses,          
     }
    return render(request, 'main/checkout.html', context)

def shippingaddress(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        
        
        new = Address.objects.create(
            user = request.user,
            firstname = fname,
            lastname = lname,
            email = email,
            number = phone,
            address1 = address,
            country = country,
            state = state,
            city = city,
            zip = pincode
        )
        new.save()
        return redirect('checkout')  # Redirect to the appropriate URL after successful form submission
    else:
        # Render the form when the request method is not POST
        return render(request, 'checkout.html')  

#placeorder

@login_required
def placeorder(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    subtotal = 0
    for cart_item in cart_items:
        if cart_item.product.price is None:
            messages.error(request, 'One of the products in the cart does not have a price set.')
            return redirect('cart')
        itemprice = cart_item.product.price * cart_item.quantity
        subtotal += itemprice

    shipping_cost = 10
    total = subtotal + shipping_cost if subtotal else 0
    discount = request.session.get('discount', 0)
    if discount:
        total -= discount

    if request.method == 'POST':
        payment = request.POST.get('payment')
        address_id = request.POST.get('addressId')

        if not address_id:
            messages.info(request, 'Input Address!!!')
            return redirect('check_out')

        address = Address.objects.get(id=address_id)

        order = Order.objects.create(
            user=user,
            address=address,
            amount=total,
            payment_type=payment,
        )
        for cart_item in cart_items:
            product = cart_item.product
            if product.stock < cart_item.quantity:
                messages.error(request, f'Not enough stock for {product.name}.')
                return redirect('cart')

            product.stock -= cart_item.quantity
            product.save()

            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                image=cart_item.product.image
            )
        cart_items.delete()
        return redirect('success')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('cart')
#payment
def proceedtopay(request):
    print('hjbdshkbskdjg')
    cart = Cart.objects.filter(user=request.user)
    total = 0
    shipping = 10
    subtotal=0
    for cart_item in cart:
        
            itemprice = (cart_item.product.price) * (cart_item.quantity)
            subtotal = subtotal + itemprice
    for item in cart:
        discount = request.session.get('discount', 0)
    total=subtotal+shipping 
    if discount:
        total -= discount 
    return JsonResponse({
        'total' : total

    })



def razorpay(request,address_id):
    print("reachedddddddddddddddddddddddddddddddddd")
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    subtotal=0
    for cart_item in cart_items:
       
            itemprice = (cart_item.product.price) * (cart_item.quantity)
            subtotal = subtotal + itemprice
    shipping_cost = 10 
    total = subtotal + shipping_cost if subtotal else 0
    
    discount = request.session.get('discount', 0)
    
    if discount:
        total -= discount 

    payment  =  'razorpay'
    user     = request.user
    cart_items = Cart.objects.filter(user=user)
    address = Address.objects.get(id=address_id)
    order = Order.objects.create(
        user          =     user,
        address       =     address,
        amount        =     total,
        payment_type  =     payment,
    )
    for cart_item in cart_items:
        product = cart_item.product
        product.stock -= cart_item.quantity
        product.save()

        order_item = OrderItem.objects.create(
            order         =     order,
            product       =     cart_item.product,
            quantity      =     cart_item.quantity,
            image         =     cart_item.product.image  
        )
    
    cart_items.delete()
    return redirect('success')

def success(request):
    orders = Order.objects.order_by('-id')[:1]
    context = {
        'orders'  : orders,
    }
    return render(request,'main/placeorder.html',context)
#order
def userorder(request):
    
        user = request.user 
        orders = Order.objects.filter(user = user).order_by('-id')
        context ={
            'orders':orders,
        }
        return render(request,'main/userorder.html',context)
def userorderdetails(request,order_id):
    order = get_object_or_404(Order, id=order_id) 
    context = {
        'order': order,  # Pass the order to the template context
    }

    
    return render(request,'main/userorderdetails.html',context)

def cancel_order(request, order_id):
    if request.method == 'POST':
        try:
            order = get_object_or_404(Order, id=order_id)  # Use get_object_or_404 to retrieve the order
            order.status = 'cancelled'
            order.save()
        except Order.DoesNotExist:
            pass
        else:
            return redirect('userorder')  # Redirect to 'userorder' when the order is successfully canceled
    return redirect('userorderdetails', order_id=order_id)  # Redirect to 'userorderdetails' when the request is not POST or if the order is not found
    
def return_product(request, order_id):
    order_item = get_object_or_404(OrderItem, id=order_id)
    
    if not order_item.returned:
        order_item.product.stock += order_item.quantity
        order_item.product.save()
        order_item.returned = True
        order_item.save()
    
    return redirect(request,'userorderdetails', order_id=order_item.order.id)


#COUPON

def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        print(code)
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code')
            return redirect('checkout')
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        subtotal = 0
        shipping_cost = 10
        total_dict = {}
        coupons = Coupon.objects.all()
        for cart_item in cart_items:
            
                item_price = cart_item.product.price * cart_item.quantity
                total_dict[cart_item.id] = item_price
                subtotal += item_price
        if subtotal >= coupon.minimum_amount:
            messages.success(request, 'Coupon applied successfully')
            request.session['discount'] = coupon.discount
            print( request.session['discount'])
            total = subtotal - coupon.discount + shipping_cost
        else:
            messages.error(request, 'Coupon not available for this price')
            total = subtotal + shipping_cost
        for cart_item in cart_items:
            cart_item.total_price = total_dict.get(cart_item.id, 0)
            cart_item.save()
        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'total': total,
            'coupons': coupons,
            'discount_amount': coupon.discount,
        }
        return render(request, 'main/cart.html', context)
    return redirect('cart')    
    

