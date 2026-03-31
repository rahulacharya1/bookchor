from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
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


@login_required(login_url='login')
def minusFromCart(req, slug):
    book = get_object_or_404(Book, slug=slug)
    if book:
        order_qs = Order.objects.filter(user_id=req.user, payment_id=None)
        if order_qs.exists():
            order = order_qs[0]
            order_item_qs = OrderItem.objects.filter(order_id=order, book_id=book)
            if order_item_qs.exists():
                order_item = order_item_qs[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                else:
                    order_item.delete()
                return redirect('cart')
    else:
        return redirect('cart')


@login_required(login_url='login')
def removeFromCart(req, slug):
    book = get_object_or_404(Book, slug=slug)
    if book:
        order_qs = Order.objects.filter(user_id=req.user, payment_id=None)
        if order_qs.exists():
            order = order_qs[0]
            order_item_qs = OrderItem.objects.filter(order_id=order, book_id=book)
            if order_item_qs.exists():
                order_item = order_item_qs[0]
                order_item.delete()
                return redirect('cart')
    else:
        return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    pass


@login_required(login_url='login')
def applyCoupon(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        coupon_qs = Coupon.objects.filter(code__iexact=code, active=True)
        if coupon_qs.exists():
            coupon = coupon_qs[0]
            order_qs = Order.objects.filter(user_id=request.user, payment_id=None)
            if order_qs.exists():
                order = order_qs[0]
                order.coupon_id = coupon
                order.save()
                return redirect('cart')
            else:
                return redirect('cart')
        else:
            return redirect('cart')
    else:
        return redirect('cart')


@login_required(login_url='login')
def removeCoupon(request):
    order_qs = Order.objects.filter(user_id=request.user, payment_id=None)
    if order_qs.exists():
        order = order_qs[0]
        order.coupon_id = None
        order.save()
        return redirect('cart')
    else:
        return redirect('cart')


