from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from .forms import BookForm, SignUpForm, UserCreationForm
from .models import Book
from django.shortcuts import render, redirect 

# Create your views here.
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


# login views

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login')
def home(request):
    total_books = Book.objects.count()
    books = Book.objects.all()
    context = {'books': books, 'total_books': total_books}
    return render(request, 'dashboard.html', context)


@login_required(login_url='/login')
def createBook(request):
    form = BookForm
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'books/books_form.html')

# login views


def loginPage(request):
    context = {
        'username': '',
        'password': ''
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        context['username'] = username
        context['password'] = password

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Invalid Credentials')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong credentials')

    return render(request, 'auth/login.html', context)
