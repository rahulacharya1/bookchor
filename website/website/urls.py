from django.contrib import admin
from django.urls import path
from book.views import *
from book.admin_views import *
from book.auth_views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('', home, name='home'),
    path("filter/", filter, name="filter"),
    path("filter/<slug:slug>", filter, name="category_filter"),
    path("book/<slug:slug>", book_view, name="book_view"),
    
    # Auth-Work
    
    path("auth/login/", login_view, name='login'),
    path("auth/register/", register_view, name='register'),
    path("auth/logout/", logout_view, name='logout'),
    
    # Admin-Work
    
    path("admin/", dashboard, name='dashboard'),
    
    path("admin/authors/", manageAuthor, name='admin_manage_author'),
    path("admin/authors/insert/", insertAuthor, name='admin_insert_author'),
    
    path("admin/generes/", manageGenere, name='admin_manage_genere'),
    path("admin/generes/insert/", insertGenere, name='admin_insert_genere'),
    
    path("admin/books/", manageBook, name='admin_manage_book'),
    path("admin/books/insert/", insertBook, name='admin_insert_book'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
