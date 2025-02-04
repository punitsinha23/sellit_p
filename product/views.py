from django.shortcuts import render, redirect, get_object_or_404
from .models import Product , Cart
from .forms import Productform
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def create_product(request, username):
    if request.user.username != username:
        return redirect('user_home', kwargs={'username': username})

    if request.method == 'POST':
        form = Productform(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # Assign logged-in user to product
            product.save()
            return redirect(reverse('product_list', kwargs={'username': request.user.username}))
    else:
        form = Productform()

    return render(request, 'create_product.html', {'form': form, 'username': username})


@login_required
def product_list(request, username):
    if request.user.username != username:
        return redirect(reverse('user_home', kwargs={'username': request.user.username}))

    products = Product.objects.filter(user=request.user)  # Filter products by user
    return render(request, 'product_list.html', {'products': products, 'username': username})


@login_required
def update_product(request, pk, username):
    if request.user.username != username:
        return redirect(reverse('user_home', kwargs={'username': request.user.username}))

    product = get_object_or_404(Product, pk=pk, user=request.user)  # Ensure product belongs to user

    if request.method == 'POST':
        form = Productform(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('product_list', kwargs={'username': username}))
    else:
        form = Productform(instance=product)

    return render(request, 'update_product.html', {'form': form, 'username': username})


@login_required
def delete_product(request, pk, username):
    if request.user.username != username:
        return redirect(reverse('user_home', kwargs={'username': request.user.username}))

    product = get_object_or_404(Product, pk=pk, user=request.user) 
    product.delete()
    return redirect(reverse('product_list', kwargs={'username': username}))


@login_required
def detail_product(request, pk, username):
    if request.user.username != username:
        return redirect(reverse('user_home', kwargs={'username': request.user.username}))

    product = get_object_or_404(Product, pk=pk, user=request.user) 
    return render(request, 'detail_product.html', {'product': product, 'username': username})

@login_required
def cart_product(request, pk, username):
    if request.user.username != username:
        return redirect(reverse('user_home', kwargs={'username': request.user.username}))

    # Get the product (Fix: Correct query filter)
    product = get_object_or_404(Product, pk=pk)

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Add product to cart
    if product not in cart.products.all():
        cart.products.add(product)

    return redirect(reverse('view_cart', kwargs={'username': username}))  

@login_required
def view_cart(request, username):
    if request.user.username != username:
        return redirect(reverse('user_home', kwargs={'username': request.user.username}))

    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'view_cart.html', {'cart': cart})

@login_required
def navbar_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    product_count = cart.products.count()
    total_price = sum([Product.price for Product in Cart.Products.all()])
    
    return render(request, 'navbar.html', {
        'cart': cart,
        'product_count': product_count,
        'total_price': total_price,
    })