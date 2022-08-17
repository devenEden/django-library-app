from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from .forms import BookForm, OrderForm, RoleForm, SignUpForm, UserCreationForm
from .models import Book, Role, Order
from django.db.models import Q
from django.template import loader
from django.http import HttpResponse

# Create your views here.
# SIGNUP


def signup(request):
    form = SignUpForm()
    context = {
        'username': '',
        'password1': '',
        'password2': '',
        'email': '',
        'form': form
    }
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        context['username'] = request.POST.get('username')
        context['password1'] = request.POST.get('password1')
        context['password2'] = request.POST.get('password2')
        context['email'] = request.POST.get('email')
        context['form'] = form
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
        else:
            messages.error(request, form.errors)

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

# Book_requests


@login_required(login_url='/login')
def borrowBook(request, pk):
    book = Book.objects.get(id=pk)
    borrowed_book = True
    orders = Order.objects.filter(
        Q(status="Accepted") | Q(status="Pending"),
        book_name=book.id
    ).count()

    if orders >= 1:
        borrowed_book = False

    context = {
        'book': book,
        "borrowed_book": borrowed_book
    }

    print(borrowed_book, orders)
    if request.method == 'POST':
        return redirect('book_requests')
    return render(request, 'books/borrow_book.html', context)


@login_required(login_url='/login')
def createOrder(request):
    form = OrderForm()
    book_name = request.POST.get("book_name")
    if request.method == 'POST':
        form = OrderForm(
            {
                "status": "Pending",
                "date_borrowed": datetime.now(),
                "book_name": book_name,
                "return_date": datetime.now(),
                "student_name": request.user
            })
        if form.is_valid():
            form.save()
            return redirect('book_requests')
        else:
            print(form.errors)

    return redirect('book_requests')


@login_required(login_url='/login')
def bookRequests(request):

    total_order_count = Order.objects.filter(status='Pending').count()
    total_orders = Order.objects.filter(status='Pending', student_name=request.user)
    total_orders_admin = Order.objects.filter(status='Pending')
    total_borrowed = Order.objects.filter(status='Accepted').count()
    borrowed_books = Order.objects.filter(status="Accepted")
    user_role = Role.objects.get(user=request.user.id)
    total_books = Book.objects.count()
    student_name = User.objects.get(username=request.user)
    current_book_borrowed = Order.objects.filter(student_name=request.user).order_by("-id")[:1]
    current = {}

    if len(current_book_borrowed) > 0: 
        current = current_book_borrowed[0]
    

    context = {
        'total_order_count': total_order_count,
        'total_orders': total_orders,
        'total_borrowed': total_borrowed,
        'user_role': user_role,
        'borrowed_books': borrowed_books,
        'total_books': total_books,
        'student_name': student_name,
        "total_orders_admin": total_orders_admin,
        "current_book_borrowed": current,
    }

    return render(request, "books/book_requests.html", context)


def confirmBook(request, pk):
    order = Order.objects.get(id=pk)
    inputs = {"return_date": "", "date_borrowed": ""}
    if request.method == 'POST':
        form = OrderForm({
            "status": "Accepted",
            "date_borrowed": request.POST.get("date_borrowed"),
            "book_name": order.book_name,
            "return_date": request.POST.get("return_date"),
            "student_name": order.student_name,
        }, instance=order)
        inputs["return_date"] = request.POST.get("return_date")
        inputs["date_borrowed"] = request.POST.get("date_borrowed")
        print(request.POST.get('book_name'))
        if form.is_valid():
            form.save()
            return redirect('book_requests')
        else:
            print(form.errors)

    context = {
        "order": order,
        "form": inputs
    }
    return render(request, 'books/confirm_book_form.html', context)


def denyBook(request, pk):
    order = Order.objects.get(id=pk)
    context = {}
    if request.method == 'POST':
        order.delete()
        return redirect('book_requests')
    return render(request, 'books/deny_book.html', context)

def returnBook(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        form = OrderForm({
            "status": "Returned",
            "date_borrowed": request.POST.get("date_borrowed"),
            "book_name": order.book_name,
            "return_date": request.POST.get("return_date"),
            "student_name": order.student_name,
        }, instance=order) 
        if form.is_valid():
            order.delete()
            return redirect('book_fines')
        else:
            print(form.errors)

    context = {
        "order" : order
    }
    return render(request, 'dashboard.html', context)

def bookFines(request):
    return render(request, 'books/book_fines.html')
