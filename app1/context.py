from profile import Profile
from django.shortcuts import render
from .models import Address, Category
from django.shortcuts import get_object_or_404


def menu_links(request):
    links = Category.objects.all()
    return dict(links = links)


