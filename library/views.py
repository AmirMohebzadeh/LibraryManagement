from django.db.models import Q
from .models import Book, Category
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

@login_required
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

@login_required
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

@login_required
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


