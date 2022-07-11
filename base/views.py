from django.shortcuts import render, redirect 
from .forms import SignUpForm, UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.
def home(request):
    return render(request, "home.html")

# SIGNUP
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


# LOGIN  
def user_login(request):
    if request.method == "POST":
        username = request.POST.get["username"]
        password = request.POST.get["password"]
        user = authenticate(request, username= username, password= password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("home")
            else:
                return HttpResponse("<h1> Disable Account </h1>")
        else:
            return HttpResponse("<h1> Invalid Login </h1>")
    else:
        pass
    return render(request, "login.html")

        

