from django.shortcuts import redirect, render
from .models import Book, IssuedItem
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import date
from django.core.paginator import Paginator
from django.http import HttpResponse

# Home view
def home(request):
    try:
        books = Book.objects.all()
        return render(request, "home.html",{"books":books})
    except Exception as e:
        messages.error(request, str(e))
        return redirect("/")

# Login view to login user
def login(request):
    try:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("/")
            else:
                messages.info(request, "Invalid Credential")
                return redirect("login")
        else:
            return render(request, "login.html")
    except Exception as e:
        messages.error(request, str(e))
        return redirect("login")

# Register view to register user
def register(request):
    try:
        if request.method == "POST":
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            username = request.POST["username"]
            email = request.POST["email"]
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]
            
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username already exist")
                    return redirect("register")
                elif User.objects.filter(email=email).exists():
                    messages.info(request, "Email already registered")
                    return redirect("register")
                else:
                    user = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        email=email,
                        password=password1,
                    )
                    user.save()
                    return redirect("login")
            else:
                messages.info(request, "Password not matches")
                return redirect("register")
        else:
            return render(request, "register.html")
    except Exception as e:
        messages.error(request, str(e))
        return redirect("register")

# Logout view to logout user
def logout(request):
    try:
        auth.logout(request)
        return redirect("/")
    except Exception as e:
        messages.error(request, str(e))
        return redirect("/")

# Issue view to issue book to user
@login_required(login_url="login")
def issue(request):
    try:
        if request.method == "POST":
            book_id = request.POST["book_id"]
            current_book = Book.objects.get(id=book_id)
            book = Book.objects.filter(id=book_id)
            issue_item = IssuedItem.objects.create(
                user_id=request.user, book_id=current_book
            )
            issue_item.save()
            book.update(quantity=book[0].quantity - 1)
            messages.success(request, "Book issued successfully, added into record. Check your 'Issue History' for more information")
        
        my_items = IssuedItem.objects.filter(
            user_id=request.user, return_date__isnull=True
        ).values_list("book_id")
        books = Book.objects.exclude(id__in=my_items).filter(quantity__gt=0)
        return render(request, "issue_item.html", {"books": books})
    except Exception as e:
        messages.error(request, str(e))
        return redirect("/")

# History view to show history of issued books to user
@login_required(login_url="login")
def history(request):
    try:
        my_items = IssuedItem.objects.filter(user_id=request.user).order_by("-issue_date")
        paginator = Paginator(my_items, 10)
        page_number = request.GET.get("page")
        show_data_final = paginator.get_page(page_number)
        return render(request, "history.html", {"books": show_data_final})
    except Exception as e:
        messages.error(request, str(e))
        return redirect("/")

# Return view to return book to library
@login_required(login_url="login")
def return_item(request):
    try:
        if request.method == "POST":
            book_id = request.POST["book_id"]
            current_book = Book.objects.get(id=book_id)
            
            # Update book quantity
            current_book.quantity += 1
            current_book.save()
            
            # Update issued item return date
            issued_item = IssuedItem.objects.filter(
                user_id=request.user, book_id=current_book, return_date__isnull=True
            ).first()
            
            if issued_item:
                issued_item.return_date = date.today()
                issued_item.save()
                messages.success(request, "Book returned successfully. Please check your 'Issue history' for more information")
            else:
                messages.error(request, "Error returning book. Please try again.")
        
        # Retrieve books that the user has issued but not returned
        issued_items = IssuedItem.objects.filter(
            user_id=request.user, return_date__isnull=True
        )
        book_ids = issued_items.values_list("book_id", flat=True)
        books = Book.objects.filter(id__in=book_ids)
        
        # Pagination
        paginator = Paginator(books, 10)
        page_number = request.GET.get("page")
        books_paginated = paginator.get_page(page_number)
        
        params = {"books": books_paginated}
        return render(request, "return_item.html", params)
    except Exception as e:
        messages.error(request, str(e))
        return redirect("/")
