from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Category, Product, Rating, Email
from .forms import LoginForm, RegisterForm, EmailForm
from django.contrib.auth import login, logout
from django.contrib import messages


# Create your views here.


class ProductList(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    extra_context = {
        'categories': Category.objects.filter(parent=None),
        'title': "Barcha Produclar",
        'all_products': Product.objects.all(),
        'form': EmailForm()
    }


class AllProductList(ProductList):
    template_name = 'shop/all_products.html'


def detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    context = {
        'categories': Category.objects.filter(parent=None),
        'product': product,
        'form': EmailForm()
    }
    rating = Rating.objects.filter(post=product, user=request.user.id).first()  # Requestdan foydalanish
    product.user_rating = rating.rating if rating else 0
    return render(request, 'shop/detail.html', context=context)


def product_by_category(request, pk):
    category = Category.objects.get(pk=pk)
    products = Product.objects.filter(category=category)
    context = {
        'categories': Category.objects.filter(parent=None),
        'products': products,
        'all_products': Product.objects.all()
    }
    return render(request, 'shop/all_products.html', context=context)


def rate(request: HttpRequest, post_id: int, rating: int) -> HttpResponse:
    post = Product.objects.get(id=post_id)
    Rating.objects.filter(post=post, user=request.user).delete()
    post.rating_set.create(user=request.user, rating=rating)
    return detail(request, post_id)


def user_logout(request):
    """This is for logout"""

    logout(request)
    return redirect('login')


def user_login(request):
    """This is for login"""

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successfully!")
            return redirect('index')

        if form.errors:
            messages.error(request, "Check that the fields are correct!")

    form = LoginForm()
    context = {
        'form': form,
        'title': 'Sign in'
    }
    return render(request, 'shop/login.html', context=context)


def user_register(request):
    """This is for sing up"""

    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "You can log in by entering your username and password.")
            return redirect('login')

        if form.errors:
            messages.error(request, "Check that the fields are correct!")

    form = RegisterForm()
    context = {
        'form': form,
        'title': 'Sign up'
    }
    return render(request, 'shop/register.html', context=context)


def user_email(request):
    form = EmailForm(data=request.POST)
    form.save()
    return redirect('index')
