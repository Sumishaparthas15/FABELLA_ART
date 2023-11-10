from django import forms
from .models import *  # Import your Address model

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['firstname', 'lastname', 'email', 'number', 'address1', 'country', 'state', 'city', 'zip']

        

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['review_text', 'review_rating']