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

