from django.db.models import Q
from .models import Book, Category, Profile
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm
from django.core.paginator import Paginator
from django.contrib.auth import login
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.http import HttpResponseForbidden
from functools import wraps

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return HttpResponseForbidden("ابتدا وارد حساب کاربری شوید.")

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            try:
                user_role = request.user.profile.role
            except Profile.DoesNotExist:
                return HttpResponseForbidden("برای حساب شما نقشی تعیین نشده است.")

            if user_role not in roles:
                return HttpResponseForbidden("شما اجازه انجام این کار را ندارید.")

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator



def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    if category_id:
        books = books.filter(category_id=category_id)

    categories = Category.objects.all()
    paginator = Paginator(books, 6)  # هر صفحه ۶ کتاب
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    return render (request, 'home.html', {
        'books': books,
        'categories': categories,
    })

@role_required("librarian", "admin")
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST , request.FILES)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = BookForm()

    return render(request, 'add_book.html', {
        'form': form
    })

@role_required("librarian", "admin")
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES,  instance=book)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {
        'form': form
    })

@role_required("admin")
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    book.delete()

    return redirect('home')

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)

    return render(request, 'detail_book.html', {
        'book': book
    })

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})

    class CustomLoginView(LoginView):
     template_name = "registration/login.html"
    authentication_form = LoginForm


