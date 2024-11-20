# ecom/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    print("Accessed login_view")

    # Check if the form is submitted
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = AuthenticationForm(request, data=request.POST)
        # Validate the form
        if form.is_valid():
            # Get the username and password from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            # If authentication is successful, log the user in
            if user is not None:
                login(request, user)  # Logs the user in
                return redirect('home')  # Redirect to a page, e.g., 'home'
    else:
        # Display an empty login form if GET request
        form = AuthenticationForm()
    # Render the login template with the form
    return render(request, 'login.html', {'form': form})
def home(request):
    return render(request, 'swag/home.html') 

