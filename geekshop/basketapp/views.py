from django.db.models import F, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product
from django.contrib.auth.decorators import login_required


@login_required
def basket(request):
    basket = Basket.objects.filter(user=request.user)
    context = {
        'basket': basket,
    }
    return render(request, 'basketapp/basket.html', context)


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:detail', args=[pk]))
    product = get_object_or_404(Product, pk=pk)

    old_basket_items = Basket.objects.filter(user=request.user, product=product).first()

    if not old_basket_items:
        old_basket_items[0].quantity += 1
        old_basket_items[0].save()
    else:
        old_basket_items[0].quantity = F('quantity') + 1

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        context = {
            'basket': basket_items
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', context)

        return JsonResponse({'result': result})