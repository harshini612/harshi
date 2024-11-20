# swag/views.py
from rest_framework.decorators import api_view
from .models import swag
from .serializers import swagserializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.http import JsonResponse
from .models import Cart, CartItem, Product
from django.contrib.auth.decorators import login_required



@api_view(['GET', 'POST'])
def swag_list(request):
    if request.method == "GET":
        swag_items = swag.objects.all()
        serializer = swagserializer(swag_items, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = swagserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "success"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'PUT', 'DELETE'])
def swag_details(request, id=None):
   if request.method =="GET":
        swag = get_object_or_404(swag, id=id)
        serializer = swagserializer(swag,many=False)
        return Response(serializer.data)
   if request.method == "PUT":
        swag= get_object_or_404(swag,id=id)
        serializer = swagserializer(swag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "success"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

   '''if request.method == "PATCH":
        swag=get_object_or_404(swag,id=id)
        serializer = swagserializer(swag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "success"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)'''

   if request.method == "DELETE":
        swag=get_object_or_404(swag,id=id)
        swag.delete()
        return Response({"msg": "successfully deleted"}, status=status.HTTP_201_CREATED)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the user and log them in
            user = form.save()
            login(request, user)
            return redirect("home")  # Redirect to the home page after successful registration
        else:
            # Return the form with error messages
            return render(request, "swag/register.html", {"form": form})
    else:
        form = RegisterForm()  # Render an empty form for GET request
    return render(request, "swag/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Invalid username or password")
        else:
            form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "swag/login.html", {"form": form})

def home(request):
    return render(request, "swag/home.html")
def womens_views (request):
     return render(request, 'womens.html')
def mens_view (request):
     return render(request, 'mens.html')
def kids_view(request):
    return render(request, 'kids.html')
def sales_view(request):
    return render(request, 'sales.html')

def electronics_view(request):
    return render(request, 'electronics.html')

def accessories_view(request):
    return render(request, 'accessories.html')
def categories_view(request):
    return render(request, 'categories.html')
def costumercare_view(request):
    return render(request, 'costumercare.html')
def cart_view(request):
    return render(request, 'cart.html')
def becomeseller_view(request):
    return render(request, 'becomeseller.html')
def arrival_view(request):
    return render(request, 'arrival.html')
def sales_view(request):
    return render(request, 'sales.html')


def search_view(request):
    query = request.GET.get('q')
    if query: 
        results = swag.objects.filter(name__icontains=query) 
    else: 
        results = swag.objects.all()
    return render(request, 'search_results.html', {'results': results})

def autocomplete_view(request):
    query = request.GET.get('q')
    if query:
        swags = swag.objects.filter(name__icontains=query)
        suggestions = [swag.name for swag in swags]
    else:
        suggestions = []
    return JsonResponse(suggestions, safe=False)
def search_view(request):
    query = request.GET.get('q')
    results=[]
    if query:
         results = swag.objects.filter(name__icontains=query) 
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'search_results.html', context)



def addtowishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])
    if product_id not in wishlist:
        wishlist.append(product_id)
    request.session['wishlist'] = wishlist
    return redirect('wishlist')
def buy_now(request, product_id):
    # Logic to add item to a temporary session and redirect to checkout
    request.session['buy_now'] = product_id
    return redirect('checkout')
#cart 
@login_required
def add_to_cart(request, product_id):
    """
    Add a product to the cart or update its quantity if it already exists.
    """
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1  # Increment quantity if already in cart
    cart_item.save()

    return redirect('view_cart')


@login_required
def view_cart(request):
    """
    Display the user's cart with items and totals.
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/view_cart.html', {'cart': cart})


@login_required
def update_cart_item(request, item_id):
    """
    Update the quantity of a specific cart item.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove if quantity is set to 0
    return redirect('view_cart')


@login_required
def remove_from_cart(request, item_id):
    """
    Remove an item from the cart.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')






