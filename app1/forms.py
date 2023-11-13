from django import forms
from .models import * 
from django import forms
from .models import Banner # Import your Address model

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['firstname', 'lastname', 'email', 'number', 'address1', 'country', 'state', 'city', 'zip']

        

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['review_text', 'review_rating']

        from django import forms
from .models import Banner

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['description', 'image']