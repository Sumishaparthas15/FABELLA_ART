
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .import views 



urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='logout'),

    path('dashboard/',views.dashboard,name='dashboard'),
    path('customer/', views.customer, name='customer'),
    path('customer/block/<int:customer_id>/', views.block_customer, name='block_customer'),
    path('customer/unblock/<int:customer_id>/', views.unblock_customer, name='unblock_customer'),
    
    path('category/',views.category,name='category'),
    path('add_category/',views.add_category,name='add_category'),
    path('category/<int:id>/update_category/',views.update_category,name='update_category'),
    path('category/<int:category_id>/edit_category/', views.edit_category, name='edit_category'),
    path('category/<int:category_id>/delete_category/',views.delete_category,name='delete_category'),

    path('sub_category/', views.sub_category, name='sub_category'),
    path('add_sub_category/', views.add_sub_category, name='add_sub_category'),
    path('category/<int:sub_category_id>/update_sub_category/', views.update_sub_category, name='update_sub_category'),
    path('category/<int:sub_category_id>/edit_sub_category/', views.edit_sub_category, name='edit_sub_category'),
    path('category/<int:sub_id>/delete_sub_category/',views.delete_sub_category,name='delete_sub_category'),

    path('product/',views.product,name='product'),
    path('add_product/',views.add_product,name='add_product'),
    path('product/<int:product_id>/edit_product/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/update_product/',views.update_product,name='update_product'),
    path('product/<int:product_id>/delete_product/',views.delete_product,name='delete_product'),
    path('orders/',views.orders,name='orders'),
    path('update_order_status/', views.update_order_status, name='update_order_status'),
    path('search-customer/', views.search_customer, name='search_customer'),
    

    
    # -----------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------------------
    
    
    
    path('base/',views.base,name='base'),
    path('',views.home,name='home'),
    #shop
    path('shop/', views.shop, name='shop'),
    path('product_list/', views.product_list, name='product_list'),
   
    path('product/<int:product_id>/', views.product, name='product'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
    path('search/', views.search_product, name='search_product'),
    path('save_review/<int:product_id>/', views.save_review, name='save_review'),
    path('shop/<int:category_id>/', views.shop, name='products_by_category'),
    
    
    #sign in
    path('signup/', views.signup, name='signup'),
    path('verify_signup/', views.verify_signup, name='verify_signup'),
    path('generate_otp/', views.generate_otp, name='generate_otp'),
    path('login/', views.user_login, name='userlogin'),
    path('userlogout/',views.userlogout,name='userlogout'),
    path('verified_login/', views.verified_login, name='verified_login'),
    
    #profile
    path('profile/', views.profile, name='profile'),
    path('profile_update/',  views.profile_update, name='profile_update'),
    path('changepassword/',views.changepassword,name='changepassword'),

    #address
    path('address/', views.address, name='address'),
    path('addaddress/', views.add_address, name='add_address'),
    path('address/edit/<int:id>/', views.edit_address, name='edit_address'),
    path('address/update/<int:id>/', views.update_address, name='update_address'),
    path('address/delete/<int:id>/', views.delete_address, name='delete_address'),
    
    #wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wish, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('feedback/', views.feedback, name='feedback'),

    
    #cart
    path('cart/',views.cart,name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),

    #checkout
    path('checkout',views.checkout,name='checkout'),
    path('shippingaddress/', views.shippingaddress, name='shippingaddress'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('success/',views.success,name='success'),
    # path('razorpay/<int:address_id>/<str:order_id>/<int:total_amount>/', views.razorpay, name='razor_pay'),

    path('proceed-to-pay',views.proceedtopay,name='proceedtopay'),
    path('razorpay/<int:address_id>/',views.razorpay,name='razorpay'),
    

    #order
    path('userorder/', views.userorder, name='userorder'),
    path('userorderdetails/<int:order_id>/', views.userorderdetails, name='userorderdetails'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('return_product/<int:order_id>/', views.return_product, name='return_product'),

    #coupon
    path('coupon/',views.coupon,name = 'coupon'),
    path('addcoupon/',views.addcoupon,name='addcoupon'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('coupon/<int:coupon_id>/edit/', views.editcoupon, name='edit_coupon'), 
    path('coupon/<int:id>/update_coupon/', views.update_coupon, name='update_coupon'),
    path('coupon/<int:coupon_id>/delete/', views.delete_coupon, name='delete_coupon'),
    

    #wallet
    path('wallet/', views.wallet, name='wallet'),
  
  

    
     
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
