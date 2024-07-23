from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login ,logout
from shop.models import product
from cart.models import cart
from cart.models import Payment
from cart.models import ordertable
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import razorpay

def add_to_cart(request,pk):
    p = product.objects.get(id=pk)
    u = request.user
    try:
        Cart= cart.objects.get(user=u, Product=p)
        if (p.stock > 0):
            Cart.quantity += 1
            Cart.save()
            p.stock -= 1
            p.save()

    except:
        if(p.stock):
            Cart= cart.objects.create(Product=p, user=u, quantity=1)
            Cart.save()
            p.stock -= 1
            p.save()

    return redirect('cart:cart_view')

def cart_view(request):
    u=request.user
    c = cart.objects.filter(user=u)

    total=0
    for i in c:
        total=total+i.quantity*i.Product.price

    return render(request,'cart.html',{'cart':c,'total':total})


def cart_decrement(request,pk):
    print(pk)
    p = product.objects.get(id=pk)
    u = request.user
    try:
        c=cart.objects.get(user=u,Product=p)

        if(c.quantity>1):
                c.quantity -= 1
                c.save()
                p.stock += 1
                p.save()
        else:
                c.delete()
                p.stock +=1
                p.save()
    except:
        pass
    return cart_view(request)

def remove(request,pk):
    p = product.objects.get(id=pk)
    u = request.user
    c = cart.objects.get(user=u, Product=p)
    c.delete()
    p.stock += c.quantity
    p.save()
    return redirect('cart:cart_view')


def orderform(request):
    if (request.method == "POST"):
         phone= request.POST['phone']
         a = request.POST['a']
         n= request.POST['n']
         u = request.user
         c = cart.objects.filter(user=u)


         total=0
         for i in c:
             total = total + i.quantity * i.Product.price
         total=int(total*100)

         client=razorpay.Client(auth=('rzp_test_nJ2SFOGdAl2pLI','sIyEjbVqgepfJnx90AOO5IFq'))
         response_payment=client.order.create(dict(amount=total,currency='INR'))

         print( response_payment)
         order_id=response_payment['id']
         order_status=response_payment['status']
         if order_status=="created":
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=ordertable.objects.create(user=u,Product=i.Product,address=a,phone=phone,pin=n,no_of_items=i.quantity,order_id=order_id)
                o.save()

         response_payment['name']=u.username
         return render(request, 'payment.html',{'payment':response_payment})

    return render(request,'orderform.html')


@csrf_exempt
def status(request,u):
    print(request.user.is_authenticated)                    #false
    if not request.user.is_authenticated:
        user = User.objects.get(username=u)
        login(request,user)
        print(request.user.is_authenticated)

    if (request.method == "POST"):
        username=request.user
        print(username)
        response=request.POST
        print(response)      #razorpay response after completion of payment
        print(u)

        param_dict={
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature'],
        }
        client = razorpay.Client(auth=('rzp_test_nJ2SFOGdAl2pLI', 'sIyEjbVqgepfJnx90AOO5IFq'))
        try:
            status=client.utility.verify_payment_signature(param_dict)
            print(status)

             #after succesfull payment

            ord = Payment.objects.get(order_id=response['razorpay_order_id'])
            ord.razorpay_payment_id = response['razorpay_payment_id']              #edits payment id response
            ord.paid = True                       #edits paid to true
            ord.save()

            u=User.objects.get(username=u)
            c=cart.objects.filter(user=u)

            #filter the order table details with order id
            o=ordertable.objects.filter(user=u,order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status="paid"            #edits payment status paid
                i.save()
            c.delete()
            return render(request, 'paymentstatus.html',{})

        except:
            pass



    return render(request, 'paymentstatus.html')

@login_required
def orderview(request):
    u=request.user
    orders=ordertable.objects.filter(user=u,payment_status="paid")

    return render(request, 'orderview.html',{'orders':orders,'u':u.username})