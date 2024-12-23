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
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from .models import Banner
from .forms import BannerForm
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from email.mime.text import MIMEText
import io
import base64
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from django.http import FileResponse
from django.db import DataError
from decimal import Decimal
from datetime import datetime
import json
import matplotlib.pyplot as plt
from django.http import HttpResponseBadRequest

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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def dashboard(request):
    if 'admin' in request.session:
        products = Product.objects.order_by('-id')
        
        order_labels = [f'Order {product.id}' for product in products]
        order_amounts = [product.price for product in products]  
        stock_labels = [product.product_name for product in products]
        stock_amounts = [product.stock for product in products]
        order_data = json.dumps(order_amounts)
        stock_data = json.dumps(stock_amounts)
        context = {
            'order_labels': order_labels,
            'order_data': order_data,
            'stock_labels': stock_labels,
            'stock_data': stock_data,
        }
        return render(request, 'main/dashboard.html', context)
    else:
        return redirect('admin_login')
# CUSTOMER
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def customer(request):
    # Check if 'admin' is in the request session
    if 'admin' not in request.session:
        # If 'admin' is not in the session, redirect to the admin login page
        return redirect('admin_login')  # Change 'admin_login' to the actual URL name of your admin login page

    # Retrieve all customer profiles
    customer_list = Profile.objects.all()

    # Paginate the customer list
    paginator = Paginator(customer_list, 10)  # Show 10 customers per page
    page = request.GET.get('page')

    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        customers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
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
        return redirect('admin_login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def add_category(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            category_name = request.POST.get('category_name')
            category_offer_description = request.POST.get('category_offer_description')
            category_offer = request.POST.get('category_offer')

            # Create a new Category instance with the provided data
            category = Category.objects.create(
                category_name=category_name,
                category_offer_description=category_offer_description,
                category_offer=category_offer
            )
            
            # Save the new category to the database
            category.save()

            return redirect('category')
        
        return render(request, 'main/addcategory.html')
    
    else:
        return redirect('admin_login')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def update_category(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return HttpResponse("Error")

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_offer_description  =request.POST.get('category_offer_description')
        category_offer  =request.POST.get('category_offer')
        if category_name:
            category.category_name           =  category_name
            category.category_offer_description  =category_offer_description
            category.category_offer              =category_offer
            
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
        return redirect ('admin_login')

def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.is_deleted = True  # Use the correct field name for soft delete
        category.save()
    except Category.DoesNotExist:  # Fix the case of Category.DoesNotExist
        return render(request, 'category_not_found.html')

    return redirect('category')

def restore_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.is_deleted = False  # Use the correct field name for soft delete
        category.save()
    except Category.DoesNotExist:  # Fix the case of Category.DoesNotExist
        pass

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
        return redirect('admin_login')
def add_sub_category(request):
    main_category=Category.objects.all()
    context={
        'main_category':main_category
    }
       
    if 'admin' in request.session: 
        if request.method == 'POST':
            cat = request.POST.get('categories')
            print("Selected category ID:", cat)
            sub_category_name = request.POST.get('name')
            print("New subcategory name:", sub_category_name)
            main = Category.objects.get(id=cat)

            # Print existing subcategories for debugging
            existing_subcategories = Sub_category.objects.filter(main_category=main)
            print("Existing subcategories:", existing_subcategories)

            sub = Sub_category.objects.create(main_category=main, sub_category_name=sub_category_name)
            sub.save() 

            return redirect('sub_category')  
        return render(request, 'main/addsubcategory.html', context)

    else:
        return redirect ('admin_login')
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
        return redirect ('admin_login')   
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def update_sub_category(request, sub_category_id):
    main_category = Category.objects.all()
    sub_category = Sub_category.objects.get(id=sub_category_id)  # Use get() instead of filter()

    if request.method == 'POST':
        new_name = request.POST.get('sub_category_name')
        new_main_id = request.POST.get('main_category')
        sub_category.sub_category_name = new_name
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
        return redirect('admin_login')
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
            images = request.FILES.get('images')  
            product_offer = request.POST.get('product_offer')

            try:
                subcategory_id = Sub_category.objects.get(id=subcategory_id)
                main_category_id = subcategory_id.main_category_id
            except Sub_category.DoesNotExist:
                return HttpResponse("Sub Category not found")

            # Check if a product with the same name already exists
            if Product.objects.filter(product_name=product_name).exists():
                messages.error(request, f"A product with the name '{product_name}' already exists.", extra_tags='custom-error')
                return redirect('add_product')

            # If the product name is unique, proceed with creating the product
            product = Product.objects.create(
                product_name=product_name,
                description=description,
                Sub_category=subcategory_id,
                category_id=main_category_id,
                stock=stock,
                price=price,
                product_offer=product_offer,
                image=images  
            )

            for image in request.FILES.getlist('images'):
                Images.objects.create(product=product, images=image)

            return redirect('product')

        context = {'categories': categories}
        return render(request, 'main/addproduct.html', context)
    else:
        return redirect('admin_login')
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
        return redirect('admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.description = request.POST.get('description')
        
        if request.POST.get('category'):
            category_name = request.POST.get('category')
            category = Category.objects.get(category_name=category_name)
            product.category = category

        product.color = request.POST.get('color')
        product.stock = request.POST.get('stock')
        product.product_offer = request.POST.get('product_offer')  # Modified from 'offer' to 'product_offer'
        product.price = request.POST.get('price')
        
        image = request.FILES.get('image')
        if image:
            product.image = image
        
        product.save()
        
        mul_image = request.FILES.getlist('images')
        if mul_image:
            for image in mul_image:
                im = Images(product=product, images=image)
                im.save()

        return redirect('product')
    
    else:
        context = {
            'product': product,
        }
        return render(request, 'main/product.html', context)


def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.deleted = True
        product.save()
    except Product.DoesNotExist:
         return render(request, 'product_not_found.html')
    return redirect('product')

def restore_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.deleted = False  
        product.save()
    except Product.DoesNotExist:
        pass
    return redirect('product')
#ORDERS 
def orders(request):
    if 'admin' in request.session:
        orders = Order.objects.all().order_by('-id')
        context = {
            'orders': orders,
        }

        return render(request, 'main/adminorder.html', context)
    else:
        
        return redirect ('admin_login')
def update_order_status(request):
    if request.method == "POST":
        print(request.POST)  
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        try:
            order = Order.objects.get(id=order_id)
            previous_status = order.status  
            order.status = new_status
            order.save()
            if new_status == 'cancelled' and previous_status != 'cancelled':
                try:
                    wallet = Wallet.objects.create(
                        user=order.user,
                        order=order,
                        amount=order.amount,
                        is_credit=True,  
                        status='refund' 
                    )
                    messages.success(request, f"Order #{order.id} cancelled and amount credited to the wallet.")
                except Exception as e:
                    messages.error(request, f"Error creating wallet transaction: {e}")
            else:
                messages.success(request, f"Order #{order.id} status has been updated to {new_status}.")
                
        except Order.DoesNotExist:
            messages.error(request, f"Order with ID {order_id} does not exist.")
        
    return redirect('orders')


def search_customer(request):
    q = request.GET.get('q', '')  
    customers = Profile.objects.filter(username__icontains=q) 

    context = {
        'customers': customers
    }

    return render(request, 'main/customer.html', context)
def search_sub_category(request):
    q = request.GET.get('q', '')  
    print(f"Search query: {q}")  # Check if the search query is received

    sub_category = Sub_category.objects.filter(sub_category_name__icontains=q)
    print(f"Subcategories: {sub_category}")  # Check if the correct subcategories are retrieved

    context = {
        'sub_category': sub_category
    }

    return render(request, 'main/subcategory.html', context)


@never_cache
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def coupon(request):
    if 'admin' in request.session:
        coupons = Coupon.objects.all().order_by('id')
        context = {'coupons': coupons}
        return render(request,'main/coupon.html', context)
    else:
        return redirect('admin_login')

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
        return redirect ('admin_login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def update_coupon(request, id):
    coupon = get_object_or_404(Coupon, id=id)
    if request.method == 'POST':
        code = request.POST.get('Couponcode')
        discount = request.POST.get('price')
        minimum_amount = request.POST.get('amount')
        expiration_date = request.POST.get('date')
        if code:
            coupon.code = code
        if discount:
            coupon.discount = discount
        coupon.minimum_amount = minimum_amount
        coupon.expiration_date = expiration_date
        coupon.save()  
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

#BANNER

class BannerView(View):
    template_name = 'main/banner.html'

    def get(self, request, *args, **kwargs):
        if 'admin' in request.session:
            banners = Banner.objects.all()
            context = {'banner': banners}
            return render(request, self.template_name, context)
        else:
            return redirect('admin_login')

class AddBannerView(View):
    template_name = 'main/add_banner.html'

    def get(self, request, *args, **kwargs):
        if 'admin' in request.session:
            return render(request, self.template_name)
        else:
            return redirect('admin_login')

    def post(self, request, *args, **kwargs):
        if 'admin' in request.session:
            form = BannerForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('banner')
            else:
                return render(request, self.template_name, {'form': form})
        else:
            return redirect('admin_login')

class EditBannerView(View):
    template_name = 'main/edit_banner.html'

    def get(self, request, banner_id, *args, **kwargs):
        if 'admin' in request.session:
            try:
                banner = Banner.objects.get(id=banner_id)
            except Banner.DoesNotExist:
                return render(request, 'product_not_found.html')
            context = {'banner': banner}
            return render(request, self.template_name, context)
        else:
            return redirect('admin_login')

   

class UpdateBannerView(View):
    template_name = 'main/banner.html'

    def post(self, request, banner_id, *args, **kwargs):
        banner = Banner.objects.get(id=banner_id)
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            return redirect('banner')
        else:
            context = {'banner': banner, 'form': form}
            return render(request, self.template_name, context)

class DeleteBannerView(View):
    def get(self, request, banner_id, *args, **kwargs):
        try:
            banner = Banner.objects.get(id=banner_id)
            banner.delete()
        except Banner.DoesNotExist:
            return render(request, 'category_not_found.html')
        return redirect('banner')

from django.shortcuts import render, redirect
from .models import Contact

def adminside_message(request):
    # Check if 'admin' is in the request session
    if 'admin' not in request.session:
        # If 'admin' is not in the session, redirect to the admin login page
        return redirect('admin_login')  # Change 'admin_login' to the actual URL namfe of your admin login page

    # Retrieve all customer messages
    customer_messages = Contact.objects.all()

    # Provide the messages to the template in the context
    context = {
        'customer_messages': customer_messages
    }

    # Render the adminside_message template
    return render(request, 'main/adminside_message.html', context)


# Create bar chart function
def create_bar_chart(labels, data, title):
    plt.figure(figsize=(8, 6))
    plt.bar(labels, data, color='skyblue')
    plt.xlabel('Products')
    plt.ylabel('Amount')
    plt.title(title)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return f'data:image/png;base64,{chart_image}'


# pie chart function
def create_pie_chart(labels, data, title):
    plt.figure(figsize=(8, 8))
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return f'data:image/png;base64,{chart_image}'


def report_generator(request, orders):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    story = []

    data = [["Order ID", "Total Quantity", "Product IDs", "Product Names", "Amount"]]

    for order in orders:
        # Retrieve order items associated with the current order
        order_items = OrderItem.objects.filter(order=order)
        total_quantity = sum(item.quantity for item in order_items)

        if order_items.exists():
            product_ids = ", ".join([str(item.product.id) for item in order_items])
            product_names = ", ".join([str(item.product.product_name) for item in order_items])
        else:
            product_ids = "N/A"
            product_names = "N/A"

        data.append([order.id, total_quantity, product_ids, product_names, order.amount])

    # Create a table with the data
    table = Table(data, colWidths=[1 * inch, 1.5 * inch, 2 * inch, 3 * inch, 1 * inch])

    # Style the table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoF),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(table_style)

    # Add the table to the story and build the document
    story.append(table)
    doc.build(story)

    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='orders_report.pdf')

def report_pdf_order(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse('Invalid date format.')
        orders = Order.objects.filter(date__range=[from_date, to_date]).order_by('-id')
        return report_generator(request, orders)

def chart_demo(request):
    orders = Order.objects.order_by('-id')[:5]
    labels = []
    data = []
    for order in orders:
        labels.append(str(order.id))
        data.append(order.amount)
    context = {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }
    return render(request, 'main/chart_demo.html', context)



#-----------------------------------------------------------------------------------------------------------
#------------------------------------------------USER SIDE--------------------------------------------------
#-----------------------------------------------------------------------------------------------------------

def base(request):
    return render(request,'base.html')
def home(request):
    banners = Banner.objects.all()  # Retrieve all banner objects from the database

    context = {
        'banner': banners,
    }
    return render(request,'main/home.html',context)

# PRODUCT


def shop(request, category_id=None):
    
    products = None
    product_count = 0
    all_products = Product.objects.all()

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, deleted=False)
        product_count = products.count()
    else:
        products = Product.objects.filter(deleted=False)
        product_count = products.count()
        products = all_products
    for product in products:
        discounted_price = None
        if product.category.category_offer:
            discounted_price = (product.price - (product.price*product.category.category_offer/100))
        product.discounted_price = discounted_price
        offer_price = None
        if product.product_offer:
            offer_price        =  product.price -(product.price * product.product_offer/100)
        product.offer_price    =  offer_price

    # Price filter
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if min_price is not None:
        products = products.filter(price__gte=min_price)
    if max_price is not None:
        products = products.filter(price__lte=max_price)

    # Fetch category and product offers
    category_offer = None
    product_offer = None

    if category_id:
        category_offer = category.category_offer

    context = {
        'products': products,
        'all_products': all_products,
        'product_count': product_count,
        'min_price': min_price,
        'max_price': max_price,
        'category_offer': category_offer,
        'product_offer': product_offer,
    }

    return render(request, 'main/shop.html', context)

def product_list(request):
    product_list = Product.objects.filter(deleted=False)
    paginator = Paginator(product_list, 12)  # 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'main/shop.html', {'products': products})

def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_images = product.images_set.all()  # Access the related images using 'images_set'
    discounted_price = None
    offer_price = None
    if product.category.category_offer:
        discounted_price = (product.price - (product.price*product.category.category_offer/100))
    product.discounted_price = discounted_price
    if product.product_offer:
        offer_price        = product.price -(product.price * product.product_offer/100)
    product.offer_price    = offer_price

    context = {
        'product': product,
        'product_images': product_images,
        'discounted_price': discounted_price, 
        
    }

    return render(request, 'main/productdetails.html', context)



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

        try:
            if not (name and email and password and phone_number and confirmpassword):
                messages.info(request, "Please Fill Required Fields")
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

            # Create the user using the CustomUser model
            user = Profile.objects.create_user(email=email, password=password, username=name, number=phone_number)
            user.save()

            # Generate OTP and send email
            message = generate_otp()
            sender_email = "sumishasudha392@gmail.com"
            receiver_email = email
            password_email = "ebvd zdgw thrs sgsf"

            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_email, password_email)
                    server.sendmail(sender_email, receiver_email, message)

            except smtplib.SMTPAuthenticationError:
                messages.error(request, 'Failed to send OTP email. Please check your email configuration.')
                return redirect('signup')

            # Store session data and notify user of OTP
            request.session['email'] = email
            request.session['otp'] = message
            messages.success(request, 'OTP is sent to your email')

            return redirect('verify_signup')

        except DataError as e:
            # Handle DataError related to phone number length
            messages.error(request, 'Invalid phone number. Please enter a valid phone number.')
            return redirect('signup')

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
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
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
                    if user is not None:
                        login(request, user)
                        request.session['email']=email
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
        logout(request)
           
        request.session.flush()

    return redirect('userlogin')
# USER PROFILE
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
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
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
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
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
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
        return redirect('address') 
        
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
        old_password = request.POST.get('old')
        new_password = request.POST.get('new_password1')
        confirm_password = request.POST.get('new_password2')

        # Get the user from the request
        customer = request.user

        if customer.check_password(old_password):
            if new_password == confirm_password:
                customer.set_password(new_password)
                customer.save()

                # Update the user's session with the new password
                update_session_auth_hash(request, customer)

                messages.success(request, 'Password changed successfully.')
                return redirect('home')
            else:
                messages.error(request, 'New password and confirm password do not match.')
                return redirect('changepassword')
        else:
            messages.error(request, 'Old password is incorrect.')
            return redirect('changepassword')

    return render(request, 'main/changepassword.html')
def forgotpassword(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            customer = Profile.objects.get(email=email) 
            if customer.email == email:
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
                    return redirect('signup') 
                request.session['email'] =  email
                request.session['otp']   =  message
                messages.success (request, 'OTP is sent to your email')
                return redirect('reset_password')         
        except Profile.DoesNotExist:
            messages.info(request,"Email is not valid")
            return redirect('userlogin')
    else:
        return redirect('userlogin')

def reset_password(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        stored_otp = request.session.get('otp')
        if entered_otp == stored_otp:
            if new_password == confirm_password:
                email = request.session.get('email')
                try:
                    customer = Profile.objects.get(email=email)
                    customer.set_password(new_password)
                    customer.save()
                    del request.session['email'] 
                    del request.session['otp']
                    messages.success(request, 'Password reset successful. Please login with your new password.')
                    return redirect('userlogin')
                except Profile.DoesNotExist:
                    messages.error(request, 'Failed to reset password. Please try again later.')
                    return redirect('userlogin')
            else:
                messages.error(request, 'New password and confirm password do not match.')
                return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please enter the correct OTP.')
            return redirect('reset_password')
    else:
        return render(request, 'main/forgotpassword.html')    


@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search_product(request, category_id=None):
    products = None
    product_count = 0

    if 'query' in request.GET:
        query = request.GET['query']

        if query:
            if category_id:
                category = get_object_or_404(Category, id=category_id)
                products = Product.objects.filter(
                    Q(description__icontains=query) | Q(product_name__icontains=query),
                    category=category,
                    deleted=False
                )
            else:
                # If no category_id is provided, filter products based on the query only
                products = Product.objects.filter(
                    Q(description__icontains=query) | Q(product_name__icontains=query),
                    deleted=False
                )

    # Fetch category and product offers
    category_offer = None
    product_offer = None

    if category_id:
        category_offer = category.category_offer

    # Apply offer calculations to each product
    for product in products:
        discounted_price = None
        if category_offer:
            discounted_price = (product.price - (product.price * category_offer / 100))
        product.discounted_price = discounted_price

        offer_price = None
        if product.product_offer:
            offer_price = product.price - (product.price * product.product_offer / 100)
        product.offer_price = offer_price

    context = {
        'search_results': products,
        'product_count': products.count(),
        'category_offer': category_offer,
        'product_offer': product_offer,
    }

    return render(request, 'main/search.html', context)


# WISHLIST
@login_required(login_url='verified_login')

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

@login_required(login_url='verified_login')
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
        if cart_item.product.category.category_offer:
            item_price = (cart_item.product.price - (cart_item.product.price*cart_item.product.category.category_offer/100)) * cart_item.quantity
            total_dict[cart_item.id] = item_price
            subtotal += item_price
        elif cart_item.product.product_offer:
            item_price = (cart_item.product.price - (cart_item.product.price * cart_item.product.product_offer/100)) * cart_item.quantity
            total_dict[cart_item.id] = item_price
            subtotal += item_price
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
@login_required(login_url='verified_login')



def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('product_not_found')

    quantity = request.POST.get('quantity', 1)

    # Check if the product is in stock
    if product.stock >= int(quantity) >= 0:
        # Proceed with adding the product to the cart
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

        if created:
            cart_item.quantity = int(quantity)
        else:
            cart_item.quantity += int(quantity)

        cart_item.save()

        # Remove the item from the wishlist
        if request.user.is_authenticated:
            wish = get_object_or_404(WishList, product=product, user=request.user)
            wish.delete()

        return redirect('cart')
    else:
        # Product is out of stock, render the out_of_stock template
        return render(request, 'main/out_of_stock.html', {'product': product})

def update_cart(request, product_id):
    cart_item = None
    cart_item = get_object_or_404(Cart, product_id=product_id, user=request.user)
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
@login_required(login_url='verified_login')
def checkout(request): 
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    subtotal = 0
    for cart_item in cart_items:
        if cart_item.product.category.category_offer:
            item_price = (cart_item.product.price - (cart_item.product.price*cart_item.product.category.category_offer/100)) * cart_item.quantity
            subtotal += item_price
        elif cart_item.product.product_offer:
            itemprice =  (cart_item.product.price - (cart_item.product.price * cart_item.product.product_offer/100)) * cart_item.quantity
            subtotal=subtotal+itemprice
        else:
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
        if cart_item.product.category.category_offer:
            item_price = (cart_item.product.price - (cart_item.product.price*cart_item.product.category.category_offer/100)) * cart_item.quantity
            subtotal += item_price
        elif cart_item.product.product_offer:
            itemprice =  (cart_item.product.price - (cart_item.product.price * cart_item.product.product_offer/100)) * cart_item.quantity
            subtotal=subtotal+itemprice
        else:
            itemprice = (cart_item.product.price) * (cart_item.quantity)
            subtotal = subtotal + itemprice

    shipping_cost = 100
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
    
    cart = Cart.objects.filter(user=request.user)
    total = 0
    shipping = 10
    subtotal=0
    for cart_item in cart:
        if cart_item.product.category.category_offer:
            item_price = (cart_item.product.price - (cart_item.product.price*cart_item.product.category.category_offer/100)) * cart_item.quantity
            subtotal += item_price
        elif cart_item.product.product_offer:
            itemprice =  (cart_item.product.price - (cart_item.product.price * cart_item.product.product_offer/100)) * cart_item.quantity
            subtotal=subtotal+itemprice
        else:
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
    
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    subtotal=0
    for cart_item in cart_items:
        if cart_item.product.category.category_offer:
            item_price = (cart_item.product.price - (cart_item.product.price*cart_item.product.category.category_offer/100)) * cart_item.quantity
            subtotal += item_price
        elif cart_item.product.product_offer:
            itemprice =  (cart_item.product.price - (cart_item.product.price * cart_item.product.product_offer/100)) * cart_item.quantity
            subtotal=subtotal+itemprice
        else:
            itemprice = (cart_item.product.price) * (cart_item.quantity)
            subtotal = subtotal + itemprice
    shipping_cost = 100 
    total = subtotal + shipping_cost if subtotal else 0
    
    discount = request.session.get('discount', 0)
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
@login_required(login_url='verified_login')
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
    user = request.user
    usercustm = Profile.objects.get(email=user)
    
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        # Handle the case where the order with the given ID does not exist
        return HttpResponseNotFound("Order not found")

    if order.status == 'completed' and order.payment_type == 'cod':
        wallet = Wallet.objects.create(
            user=user,
            order=order,
            amount=order.amount,
            status='Credited',
        )
        wallet.save()
        order.status = 'cancelled'
        order.save()
        Order_item_amount = Decimal(order.amount)
        usercustm.wallet_bal += Order_item_amount
        usercustm.save()
    elif order.payment_type == 'razorpay':
        wallet = Wallet.objects.create(
            user=user,
            order=order,
            amount=order.amount,
            status='Credited',
        )
        wallet.save()
        order.status = 'cancelled'
        order.save()
        Order_item_amount = Decimal(order.amount)
        usercustm.wallet_bal += Order_item_amount
        usercustm.save()

    restock_products(order)
    order.status = 'cancelled'
    order.save()
    return redirect('userorderdetails', order.id)

def restock_products(order):
    order_items = OrderItem.objects.filter(order=order)
    for order_item in order_items:
        product = order_item.product
        product.stock += order_item.quantity
        product.save() 

def return_product(request, order_id):
    user = request.user
    usercustm = Profile.objects.get(email=user)
    order = Order.objects.get(id=order_id)
    if (order.status == 'delivered' or order.status == 'completed') and (order.payment_type == 'cod' or order.payment_type == 'razorpay'):
        wallet = Wallet.objects.create(
            user=user,
            order=order,
            amount=order.amount,
            status='Credited'
        )
        wallet.save()
        order.status = 'returned'
        order.save()
        refund = Decimal(order.amount)
        usercustm.wallet_bal += refund
        usercustm.save()
        restock_products(order)
    
    return redirect('userorderdetails', order_id=order.id)

#Wallet

def wallet(request):
    user = request.user
    customer = Profile.objects.get(email=user)
    print(customer)
    # In the wallet view
    wallet_transactions = Wallet.objects.filter(user=customer, order__isnull=False).order_by('-created_at')

    
    
    context = {
        'wallet_transactions': wallet_transactions,
        'customer': customer,
    }
    return render(request, 'main/wallet.html', context)


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
            if cart_item.quantity > cart_item.product.stock:
                messages.warning(request, f"{cart_item.product.product_name} is out of stock.")
                cart_item.quantity = cart_item.product.stock
                cart_item.save()
            if cart_item.product.category.category_offer:
                item_price = (cart_item.product.price - (cart_item.product.price*cart_item.product.category.category_offer/100)) * cart_item.quantity
                total_dict[cart_item.id] = item_price
                subtotal += item_price
            elif cart_item.product.product_offer:
                item_price = (cart_item.product.price - (cart_item.product.price * cart_item.product.product_offer/100)) * cart_item.quantity
                total_dict[cart_item.id] = item_price
                subtotal += item_price
            else:
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
    
def invoice(request, id):
    # 1. Fetch the order and items
    user = request.user
    orders = Order.objects.filter(id=id)
    order_items = OrderItem.objects.filter(order=id)
     
    for order in orders:
        address= order.address

        for item in order_items:
            # 2. Render the order and items to an HTML template
            rendered = render_to_string('main/invoice.html', {'order': order, 'item': item, 'address': address})

            # 3. Convert the rendered HTML to PDF
            output = io.BytesIO()
            pdf = pisa.CreatePDF(rendered, output)
            pdf_data = output.getvalue()
            # 4. Send the PDF as an email attachment
            msg = MIMEMultipart()
            msg['From'] = 'sumishasudha392@@gmail.com'
            msg['To'] = order.user.email
            msg['Subject'] = 'Invoice from FABELLA_ART'
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(pdf_data)
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment; filename=invoice.pdf')
            msg.attach(attachment)
            try:
                smtp_server = 'smtp.gmail.com'
                smtp_port = 587
                smtp_username = 'sumishasudha392@gmail.com'
                smtp_password = 'xhywblrweffmdeyj'
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                server.quit()
            except Exception as e:
                return HttpResponse(f'Email sending failed: {str(e)}')
    return HttpResponse('Emails sent successfully!')
def download_invoice_view(request, order_id):
    # Retrieve order details and generate the invoice HTML
    order = Order.objects.get(id=order_id)
    # ... (additional logic to retrieve order details) ...

    rendered = render_to_string('main/invoice.html', {'order': order})

    # Convert HTML to PDF
    pdf_data = io.BytesIO()
    pdf = pisa.CreatePDF(rendered, pdf_data)

    # Set response headers for PDF download
    response = HttpResponse(pdf_data.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{order_id}.pdf'
    return response
@login_required(login_url='verified_login')
def contact(request):
    context = {}  
    if request.method=='POST':
        user=request.user
        message = request.POST.get('message')
        contact = Contact(user=user,message=message)
        contact.save()
        

        return redirect('contact') 
    return render(request,'main/contact.html',context)
def reply(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        message_content = request.POST.get('message')

        subject = 'Message from FABELLA_ART'
        from_email = 'sumishasudha392@gmail.com'
        to_email = user_email

        # Create the MIME message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message_content, 'plain'))

        # try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'sumishasudha392@gmail.com'
        smtp_password = 'xhywblrweffmdeyj'
        # Connect to the server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()

    messages.success(request, 'Email sent successfully.')
    return redirect('adminside_message')
 