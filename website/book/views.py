from django.shortcuts import render
from .models import *

# Create your views here.

def home(request):
    data = {
        "title":"Home",
        "generes":Genere.objects.all(),
        "books":Book.objects.all(),
        "authors":Author.objects.all()
    }
    return render(request, "home.html", data)


def filter(request, slug=None):
    if slug is None:
        search_query = request.GET.get("search", "")
        data = {
            "generes":Genere.objects.all(),
            "books":Book.objects.filter(title__icontains=search_query),
            "authors":Author.objects.filter(name__icontains=search_query),
            "title":search_query
        }
        return render(request, "filter.html", data)
    else:
        data = {
            "generes":Genere.objects.all(),
            "books":Book.objects.filter(genere__slug=slug),
            "authors":Author.objects.filter(authors__genere__slug=slug).distinct(),
            "title":Genere.objects.get(slug=slug).title
        }
        return render(request, "filter.html", data)
    
