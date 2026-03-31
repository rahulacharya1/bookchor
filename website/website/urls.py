from django.contrib import admin
from django.urls import path
from book.views import *
from book.admin_views import *
from book.auth_views import *
from book.checkout_views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('superadmin/', admin.site.urls),
    path('', home, name='home'),
    path("filter/", filter, name="filter"),
    path("filter/<slug:slug>", filter, name="category_filter"),
    path("book/<slug:slug>", book_view, name="book_view"),
    path("cart/", cart, name='cart'),
    
    # Auth-Work
    
    path("auth/login/", login_view, name='login'),
    path("auth/register/", register_view, name='register'),
    path("auth/logout/", logout_view, name='logout'),
    
    # Checkout-Work
    
    path("checkout/", checkout, name='checkout'),
    path("checkout/add-to-cart/<slug:slug>/", addToCart, name='add_to_cart'),
    path("checkout/minus-from-cart/<slug:slug>/", minusFromCart, name='minus_from_cart'),
    path("checkout/remove-from-cart/<slug:slug>/", removeFromCart, name='remove_from_cart'),
    path("checkout/apply-coupon/", applyCoupon, name='apply_coupon'),
    path("checkout/remove-coupon/", removeCoupon, name='remove_coupon'),

    # Admin-Work
    
    path("admin/", dashboard, name='dashboard'),
    path("admin/logout/", admin_logout_view, name='admin_logout'),
    
    path("admin/authors/", manageAuthor, name='admin_manage_author'),
    path("admin/authors/insert/", insertAuthor, name='admin_insert_author'),
    path("admin/authors/edit/<int:id>/", editAuthor, name='admin_edit_author'),
    path("admin/authors/delete/<int:id>/", deleteAuthor, name='admin_delete_author'),
    
    path("admin/generes/", manageGenere, name='admin_manage_genere'),
    path("admin/generes/insert/", insertGenere, name='admin_insert_genere'),
    path("admin/generes/edit/<int:id>/", editGenere, name='admin_edit_genere'),
    path("admin/generes/delete/<int:id>/", deleteGenere, name='admin_delete_genere'),
    
    path("admin/books/", manageBook, name='admin_manage_book'),
    path("admin/books/insert/", insertBook, name='admin_insert_book'),
    path("admin/books/edit/<int:id>/", editBook, name='admin_edit_book'),
    path("admin/books/delete/<int:id>/", deleteBook, name='admin_delete_book'),
    
    path("admin/coupons/", manageCoupon, name='admin_manage_coupon'),
    path("admin/coupons/insert/", insertCoupon, name='admin_insert_coupon'),
    path("admin/coupons/edit/<int:id>/", editCoupon, name='admin_edit_coupon'),
    path("admin/coupons/delete/<int:id>/", deleteCoupon, name='admin_delete_coupon'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
