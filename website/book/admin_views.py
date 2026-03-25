from django.shortcuts import render, redirect
from book.models import *
from book.forms import *
from django.core.paginator import Paginator
from django.contrib.auth import logout
from functools import wraps
from django.http import HttpResponseForbidden


def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("<h1>You must be logged in to access this page</h1>")
        if not request.user.is_superuser:
            return HttpResponseForbidden("<h1>You do not have permission to access this page<h1>")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@superuser_required
def dashboard(request):
    data = {}
    data['total_books'] = Book.objects.count()
    data['total_authors'] = Author.objects.count()
    data['total_generes'] = Genere.objects.count()
    data['users'] = User.objects.all()
    return render(request, 'admin/dashboard.html', data)


@superuser_required
def admin_logout_view(request):
    logout(request)
    return redirect('login')


# ------------------------------ Author Work ----------------------------------


@superuser_required
def manageAuthor(request):
    data = {}
    authors = Author.objects.all()
    paginator = Paginator(authors, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data['authors'] = page_obj
    return render(request, 'admin/author/manage_author.html', data)


@superuser_required
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
    return render(request, 'admin/author/insert_author.html', data)


@superuser_required
def editAuthor(request, id):
    author = Author.objects.get(id=id)
    form = AuthorForm(request.POST or None, request.FILES or None, instance=author)
    
    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.slug = data.name.lower().replace(" ", "-")
            data.save()
            return redirect('admin_manage_author')
        
    return render(request, "admin/author/edit_author.html", {'form': form})


@superuser_required
def deleteAuthor(request, id):
    Author.objects.get(id=id).delete()
    return redirect('admin_manage_author')
    

# ------------------------------ Genere Work ----------------------------------


@superuser_required
def manageGenere(request):
    data = {}
    generes = Genere.objects.all()
    paginator = Paginator(generes, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data['generes'] = page_obj
    return render(request, 'admin/genere/manage_genere.html', data)


@superuser_required
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
    return render(request, 'admin/genere/insert_genere.html', data)


@superuser_required
def editGenere(request, id):
    genere = Genere.objects.get(id=id)
    form = GenereForm(request.POST or None, request.FILES or None, instance=genere)
    
    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.slug = data.title.lower().replace(" ", "-")
            data.save()
            return redirect('admin_manage_genere')
        
    return render(request, "admin/genere/edit_genere.html", {'form': form})


@superuser_required
def deleteGenere(request, id):
    Genere.objects.get(id=id).delete()
    return redirect('admin_manage_genere')


# ------------------------------ Book Work ----------------------------------


@superuser_required
def manageBook(request):
    data = {}
    books = Book.objects.all()
    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data['books'] = page_obj
    return render(request, 'admin/book/manage_book.html', data)


@superuser_required
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
    return render(request, 'admin/book/insert_book.html', data)


@superuser_required
def editBook(request, id):
    book = Book.objects.get(id=id)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    
    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.slug = data.title.lower().replace(" ", "-")
            data.save()
            return redirect('admin_manage_book')
        
    return render(request, "admin/book/edit_book.html", {'form': form})


@superuser_required
def deleteBook(request, id):
    Book.objects.get(id=id).delete()
    return redirect('admin_manage_book')
