from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime  # Import datetime module


class Categories(models.Model):
    name = models.CharField(max_length=50)
    

    def __str__(self):
        return self.name


class swag(models.Model):  # Fixed class name capitalization
    name = models.CharField(max_length=100, unique=True, default='default_name')
    pdf = models.FileField(upload_to="swag/pdf", null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=3)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField(default='True')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-date_created']


class Customer(models.Model):  # Fixed class name capitalization
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Fixed typo in 'last_name'





class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)  # Fixed typo in 'default'
    image = models.ImageField(upload_to='uploads/product', default='')
    
    def __str__(self):
        return self.name


class Order(models.Model):  # Fixed class name capitalization
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)  # Fixed datetime import
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)  # Convert product to string


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Wishlist of {self.user.username}"
class Cart(models.Model):
    """
    Represents a shopping cart linked to a user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def total_items(self):
        """
        Returns the total quantity of items in the cart.
        """
        return sum(item.quantity for item in self.cartitem_set.all())

    def total_price(self):
        """
        Returns the total price of items in the cart.
        """
        return sum(item.subtotal() for item in self.cartitem_set.all())


class CartItem(models.Model):
    """
    Represents a single item in the cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        """
        Returns the subtotal cost of the item (price * quantity).
        """
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"

