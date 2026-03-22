from django.shortcuts import render, redirect
from book.models import *
from book.forms import *
from django.core.paginator import Paginator


def dashboard(request):
    data = {}
    data['total_books'] = Book.objects.count()
    data['total_authors'] = Author.objects.count()
    data['total_generes'] = Genere.objects.count()
    return render(request, 'admin/dashboard.html', data)


def manageAuthor(request):
    data = {}
    authors = Author.objects.all()
    paginator = Paginator(authors, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data['authors'] = page_obj
    return render(request, 'admin/manage_author.html', data)


def insertAuthor(request):
    data = {}
    form = AuthorForm(request.POST or None, request.FILES or None)
    data['form'] = form
    
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.slug = data.name.lower().replace(" ", "-")
            data.save()
            return redirect('admin_manage_author')
    return render(request, 'admin/insert_author.html', data)


def manageGenere(request):
    data = {}
    generes = Genere.objects.all()
    paginator = Paginator(generes, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data['generes'] = page_obj
    return render(request, 'admin/manage_genere.html', data)


def insertGenere(request):
    data = {}
    form = GenereForm(request.POST or None, request.FILES or None)
    data['form'] = form
    
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.slug = data.title.lower().replace(" ", "-")
            data.save()
            return redirect('admin_manage_genere')
    return render(request, 'admin/insert_genere.html', data)


def manageBook(request):
    data = {}
    books = Book.objects.all()
    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data['books'] = page_obj
    return render(request, 'admin/manage_book.html', data)


def insertBook(request):
    data = {}
    form = BookForm(request.POST or None, request.FILES or None)
    data['form'] = form
    
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.slug = data.title.lower().replace(" ", "-")
            data.save()
            return redirect('admin_manage_book')
    return render(request, 'admin/insert_book.html', data)

