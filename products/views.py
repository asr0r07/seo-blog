from django.shortcuts import render, redirect, get_object_or_404
from .models import Color, Product, Brand, Category, Review


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
    ctx = {'products': products, 'categories': categories}
    return render(request, 'index.html', ctx)


def product_list(request):
    selected_brands = None
    products = Product.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()
    colors = Color.objects.all()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    brand_idx = [int(x) for x in request.GET.getlist('brand')]
    color = request.GET.get('color')
    sort = request.GET.get('sort')
    error_message = None

    try:
        if min_price:
            products = products.filter(price__gte=float(min_price))
        if max_price:
            products = products.filter(price__lte=float(max_price))
    except ValueError:
        error_message = "Invalid price range. Please enter valid numbers."

    if brand_idx:
        products = products.filter(brand__id__in=brand_idx)
        selected_brands = brands.filter(id__in=brand_idx)
        brands = brands.exclude(id__in=brand_idx)
    if color:
        products = products.filter(color__id=color)

    if sort == 'low_to_high':
        products = products.order_by('price')
    elif sort == 'high_to_low':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')



    ctx = {
        'products': products,
        'brands': brands,
        'categories': categories,
        'colors': colors,
        'error_message': error_message,
        'selected_brands': selected_brands
    }
    return render(request, 'products/product-by-category.html', ctx)


def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('category')
        color_id = request.POST.get('color')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        try:
            price = float(price)
        except (ValueError, TypeError):
            return render(request, 'products/product-create.html', {
                'error': 'Price must be a valid number.'
            })

        if name and price and brand_id and category_id and color_id and description and image:
            brand = get_object_or_404(Brand, id=brand_id)
            category = get_object_or_404(Category, id=category_id)
            color = get_object_or_404(Color, id=color_id)

            Product.objects.create(
                name=name,
                price=price,
                brand=brand,
                category=category,
                color=color,
                description=description,
                image=image,
            )
            return redirect('products:list')
        else:
            return render(request, 'products/product-create.html', {
                'error': 'All fields are required.'
            })

    brands = Brand.objects.all()
    categories = Category.objects.all()
    colors = Color.objects.all()
    ctx = {
        'brands': brands,
        'categories': categories,
        'colors': colors,
    }
    return render(request, 'products/product-create.html', ctx)


def product_detail(request, year, month, day, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        created_at__year=year,
        created_at__month=month,
        created_at__day=day
    )
    if request.method == "POST":
        name = request.POST.get('name')
        rating = request.POST.get('rating')
        content = request.POST.get('content')
        if name and rating and content:
            Review.objects.create(
                product=product,
                rating=int(rating),
                name=name,
                review=content
            )
    reviews = Review.objects.filter(product=product)
    ctx = {'product': product, 'reviews': reviews}
    return render(request, 'products/product-detail.html', ctx)


def success_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/success-commented.html', {'product': product})
