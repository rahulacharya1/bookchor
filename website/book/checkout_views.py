from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import AddressForm


@login_required(login_url='login')
def addToCart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    
    if book:
        order_qs = Order.objects.filter(user_id=request.user, payment_id=None)
        # why total price is showing 0.0 after adding book to cart?
        if order_qs.exists():
            order = order_qs[0]
            order_item_qs = OrderItem.objects.filter(order_id=order, book_id=book)
            
            if order_item_qs.exists():
                order_item = order_item_qs[0]
                order_item.quantity += 1
                order_item.save()
            else:
                OrderItem.objects.create(order_id=order, book_id=book, quantity=1)
                
            order.total_price = order.get_total_payable_price()
            order.save()
                
        else:
            order = Order.objects.create(user_id=request.user, total_price=0)
            OrderItem.objects.create(order_id=order, book_id=book, quantity=1)
            
    else:
        return redirect('book_view', slug=slug)
    
    return redirect('cart')


@login_required(login_url='login')
def minusFromCart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if book:
        order_qs = Order.objects.filter(user_id=request.user, payment_id=None)
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
def removeFromCart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if book:
        order_qs = Order.objects.filter(user_id=request.user, payment_id=None)
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


@login_required(login_url='login')
def checkout(request):
    author = Author.objects.all()
    genere = Genere.objects.all()
    order_qs = Order.objects.filter(user_id=request.user, payment_id=None)
    if order_qs.exists():
        order = order_qs[0]

    if request.method == "POST":
        address_id = request.POST.get("address")
        payment_method = request.POST.get("payment_method")

        payment = Payment.objects.create(
            user_id=request.user,
            amount=order.get_total_payable_price(),
            payment_method=payment_method,
            mode= (payment_method if payment_method != "cod" else "Cash on Delivery"),
            transaction_id=""
        )

        order.payment_id = payment
        order.address_id = Address.objects.get(id=address_id)
        order.save()
        return redirect('success')
          
    order_qs = Order.objects.filter(user_id=request.user, payment_id=None)
    addresses = Address.objects.filter(user_id=request.user)
    if order_qs.exists():
        order = order_qs[0]
        context = {
            "order": order,
            "addresses": addresses,
            "authors": author,
            "generes": genere
        }
        return render(request, "checkout.html", context)
    else:
        return redirect("success") 


@login_required
def addAddress(request):
    author = Author.objects.all()
    genere = Genere.objects.all()
    form = AddressForm(request.POST or None)
    if form.is_valid():
        address = form.save(commit=False)
        address.user_id = request.user
        address.save()
        return redirect("checkout")
    return render(request, "add_address.html", {"form": form, "authors": author, "generes": genere})


def edit_address(request, id):
    address = Address.objects.filter(id=id, user_id=request.user).first()

    if not address:
        return redirect('checkout')  # simple fallback

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('checkout')
    else:
        form = AddressForm(instance=address)

    return render(request, 'edit_address.html', {
        'form': form,
    })
    
    
def delete_address(request, id):
    address = Address.objects.filter(id=id, user_id=request.user).first()

    if address:
        address.delete()

    return redirect('checkout')


@login_required
def success(request):
    author = Author.objects.all()
    genere = Genere.objects.all()
    return render(request, "order_success.html", {"authors": author, "generes": genere})

