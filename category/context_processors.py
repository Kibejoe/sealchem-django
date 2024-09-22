#Context processrs make the variables globally available to all the templates

from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links) #The first links is the variable of the context processors and the second is the data


