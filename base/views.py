from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from .forms import BookForm, RoleForm, SignUpForm, UserCreationForm
from .models import Book, Role, Borrowed
from django.db.models import Q
from django.template import loader
from django.http import HttpResponse

# Create your views here.
# SIGNUP


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            form.save()
            new_user = authenticate(username=username, password=password)
            role = RoleForm({'user': new_user.id, 'role': 'Student'})
            role.save()
            if new_user is not None:
                login(request, new_user)
                return redirect("home")

    form = SignUpForm()

    context = {
        "form": form
    }
    return render(request, "auth/signup.html", context)


# login views

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    total_students = Role.objects.filter(role='Student').count()
    total_books = Book.objects.count()
    books = Book.objects.filter(Q(title__icontains=q) | Q(author__icontains=q))
    user_role = Role.objects.get(user=request.user.id)

    context = {
        'books': books,
        'total_books': total_books,
        'total_students': total_students,
        'user_role': user_role,
        'q': q
    }
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

# edit book view


@login_required(login_url='/login')
def editBook(request, pk):
    book = Book.objects.get(id=pk)
    context = {
        'book': book
    }

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'books/edit_book_form.html', context)


@login_required(login_url='/login')
def deleteBook(request, pk):
    book = Book.objects.get(id=pk)
    context = {
        'book': book
    }
    if request.method == 'POST':
        book.delete()
        return redirect('home')
    return render(request, 'books/delete_book.html', context)
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

#Book_requests
def borrow_book(request, pk):
    book = Book.objects.get(id=pk)
    context = {
        'book': book
    }
    if request.method == 'POST':
        book.save(Borrowed)
        return redirect('book_requests')
    return render(request, 'books/borrow_book.html', context)

def bookRequests(request):
    borrowed = Borrowed.objects.all()
    role = Role.objects.all()

    total_students = role.count()

    total_borrowed = borrowed.count()
    accepted = borrowed.filter("Accepted").count()
    deny = borrowed.filter("Deny").count()
    
    context = {
        'borrowed': borrowed, 'role': role, 'accepted' : accepted, 'deny' : deny 
    }
    if request.method == 'POST':
        form = BorrowedForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'books/book_requests.html', context)

    
#@login_required(login_url='/login')