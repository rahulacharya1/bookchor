from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Genere(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.title

    
class Author(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    image = models.ImageField(null=True, blank=True, upload_to="author")
    email = models.EmailField(null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.name

    
class Book(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    description = models.TextField()
    no_of_pages = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="authors")
    genere = models.ForeignKey(Genere, on_delete=models.CASCADE, related_name="categorys")
    image = models.ImageField(upload_to="books")
    edition = models.CharField(default="Latest Edition")
    isbn = models.CharField(max_length=200)
    language = models.CharField(default="English")
    
    def __str__(self):
        return self.title
    

class Address(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    contact = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
    
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.FloatField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.code


class Payment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Payment {self.user_id.username} - {self.amount}"
    
    
class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    order_date = models.DateField(auto_now_add=True)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
    coupon_id = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"Order {self.user_id.username} - {self.total_price}"
    
    def get_total_price(self):
        total_price = 0
        for item in self.order_items.all():
            if item.book_id.discount_price:
                total_price += item.book_id.discount_price * item.quantity
            else:
                total_price += item.book_id.price * item.quantity
        return round(total_price, 1)
    

    def get_shipping_charge(self):
        if self.get_total_price() < 500:
            return 45
        else:
            return 0

    def get_tax_price(self):
        return round(self.get_total_price() * 0.18, 0)
    
    def get_discount_amount(self):
        if self.coupon_id:
            return self.coupon_id.discount_amount
        else:
            return 0

    def get_total_payable_price(self):
        return self.get_total_price() + self.get_shipping_charge() + self.get_tax_price() - self.get_discount_amount()
    
    
class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Order Item {self.order_id.id} {self.book_id.title} - {self.quantity}"
    
