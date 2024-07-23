from cart.models import cart

def total(request):
    u=request.user
    count=0

    if request.user.is_authenticated:
        try:
            item=cart.objects.filter(user=u)
            count=item.count()
        except:
            count=0
    return {'count':count}