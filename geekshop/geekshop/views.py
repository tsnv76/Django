from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product


def main(request):
    title = 'Магазин'
    basket = Basket.objects.filter(user=request.user)

    products = Product.objects.all()[:4]

    context = {
        'title': title,
        'products': products,
        'basket': basket,
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    title = 'Контакты'

    context = {
        'title': title,
    }
    return render(request, 'geekshop/contact.html', context)
