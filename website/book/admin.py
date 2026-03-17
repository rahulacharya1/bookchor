from django.contrib import admin
from .models import *

# Register your models here.

class GenereAdmin(admin.ModelAdmin):
    list_display = ("title","slug")
    prepopulated_fields = {"slug":("title",)}
    
admin.site.register(Genere, GenereAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name","slug")
    prepopulated_fields = {"slug":("name",)}
    
admin.site.register(Author, AuthorAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ("title","price","discount_price","genere","author","isbn","language")
    prepopulated_fields = {"slug":("title",)}
    
admin.site.register(Book, BookAdmin)

