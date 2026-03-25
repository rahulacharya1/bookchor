from django.shortcuts import render
from .models import *
import re

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
        if search_query:
            if re.match(r"^[0-9]{10}(\d{3})?$", search_query):
                book = Book.objects.filter(isbn=search_query).first()
                
                if book:
                    data = {
                        "book":book,
                        "generes":Genere.objects.all(),
                        "authors":Author.objects.all(),
                        "related_books": Book.objects.filter(genere=book.genere).exclude(slug=book.slug)[:10]
                    }
                    return render(request, "book_view.html", data)
        data = {
            "generes":Genere.objects.all(),
            "books":Book.objects.filter(title__icontains=search_query),
            "authors":Author.objects.filter(name__icontains=search_query),
            "title":search_query
        }
        return render(request, "filter.html", data)
    
    genere = Genere.objects.filter(slug=slug).first()
    
    if genere:
        data = {
            "generes":Genere.objects.all(),
            "books":Book.objects.filter(genere=genere),
            "authors":Author.objects.all(),
            "title":genere.title
        }
        return render(request, "filter.html", data)
    else:
        author = Author.objects.filter(slug=slug).first()
        data = {
            "generes":Genere.objects.all(),
            "books":Book.objects.filter(author=author),
            "authors":Author.objects.all(),
            "title":author.name
        }
        return render(request, "filter.html", data)
    

def book_view(request, slug):
    data = {
        "book": Book.objects.filter(slug=slug).first(),
        "generes": Genere.objects.all(),
        "authors": Author.objects.all(),
        "related_books": Book.objects.filter(genere=Book.objects.get(slug=slug).genere).exclude(slug=slug)[:10]
    }
    return render(request, "book_view.html", data)



def cart(request):
    return render(request, "cart.html")

