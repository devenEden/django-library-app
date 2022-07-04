from django.shortcuts import render, redirect
from .forms import SignUpForm, UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.
def home(request):
    return render(request, "home.html")

def signup(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")
                form.save()
                new_user = authenticate(username = username, password = password)
                if new_user is not None:
                    login(request, new_user)
                    return redirect("home")
    
    
    
    form = SignUpForm()

    context = {
        "form" : form
    }
    return render(request, "signup.html", context)