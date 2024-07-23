from shop.models import category



def links(request):
    c=category.objects.all()
    return({'links':c})