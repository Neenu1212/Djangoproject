from django.shortcuts import render
from shop.models import product
from django.db.models import Q



def search_products(request):
        p = None  # to initialize
        query = ""
        if (request.method == "POST"):
                query = request.POST['q']
                if query:
                        p =product.objects.filter(Q(title__icontains=query) | Q(price__icontains=query))
        return render(request, 'search_products.html', {'p': p, 'query': query})