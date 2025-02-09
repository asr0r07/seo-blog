from django.shortcuts import render, redirect
from catalogs.models import Category


def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name and description:
            Category.objects.create(
                name=name,
                description=description,
            )
            return redirect('home')
        else:
            return render(request, 'products/category-create.html', {
                'error': 'All fields are required.'
            })
    return render(request, 'category/category-create.html')

