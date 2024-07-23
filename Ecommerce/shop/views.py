from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login ,logout
from shop.models import category
from shop.models import product
from django.contrib import messages


# Create your views here.


def allcategories(request):
    item= category.objects.all()
    return render(request, 'category.html', {'item':item})

def allproducts(request,pk):
    cate_obj=category.objects.get(id=pk)  #
    pro_obj=product.objects.filter(category=cate_obj)
    return render(request, 'product.html', {'cate_obj':cate_obj ,'pro_obj': pro_obj})

def product_details(request,pk):
    p = product.objects.get(id=pk)
    return render(request,'productdetails.html', {'p': p})


def register(request):
    if (request.method == "POST"):  # after form submition


        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        l = request.POST['l']
        f = request.POST['f']
        e = request.POST['e']
        if(cp==p):
            user=User.objects.create_user(username=u,password=p,first_name=f,last_name=l,email=e)  #so thath the password will be saved
            user.save()
            return redirect('shop:allcategories')


    return render(request,'register.html')



def userlogin(request):
    if (request.method == "POST"):  # after form submition

        u = request.POST['u']
        p = request.POST['p']
        print(u,p)
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:allcategories')
        else:
            messages.error(request,"invalid credetails")
    return render(request, 'login.html')

def userlogout(request):
    logout(request)
    return redirect('shop:userlogin')

