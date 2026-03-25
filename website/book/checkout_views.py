from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required


@login_required
def addToCart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    
    if book:
        order_qs = Order.objects.filter(user_id=request.user, payment_id=None)
        
        if order_qs.exists():
            order = order_qs[0]
            order_item_qs = OrderItem.objects.filter(order_id=order, book_id=book)
            
            if order_item_qs.exists():
                order_item = order_item_qs[0]
                order_item.quantity += 1
                order_item.save()
            else:
                OrderItem.objects.create(order_id=order, book_id=book, quantity=1)
                
        else:
            order = Order.objects.create(user_id=request.user, total_price=0)
            OrderItem.objects.create(order_id=order, book_id=book, quantity=1)
            
    else:
        return redirect('book_view', slug=slug)
    
    return redirect('cart')


@login_required
def minusFromCart(request, slug):
    pass


@login_required
def removeFromCart(request, slug):
    pass


@login_required
def checkout(request):
    return render(request, "checkout.html")


@login_required
def applyCoupon(request):
    pass


@login_required
def removeCoupon(request):
    pass


@login_required
def checkCoupon(request):
    pass


