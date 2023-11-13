
from .models import Address, Category,Sub_category


def menu_links(request):
    links = Category.objects.all()
    return dict(links = links)

def menu_link(request):
    link = Sub_category.objects.all()
    return dict(link = link)



