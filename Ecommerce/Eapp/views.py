from django.shortcuts import render,redirect # type: ignore
from django.http import HttpResponse # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth import authenticate,login,logout # type: ignore
from .models import Product,Cart,Order
from django.db.models import Q # type: ignore
import razorpay # type: ignore
# Create your views here.


def index(request):
    context={}
    p=Product.objects.all()
    print(p)
    context["Product"]=p

    return render(request,'index.html',context)

# Register view
def register(request):
    context={}
    if request.method=='POST':
        un=request.POST['uname']
        p=request.POST['pass']
        cp=request.POST['cpass']

        if un=="" or p=="" or cp=="":
            context["errmsg"]="Fields can not be empty"
            return render(request,'register.html',context)
        
        elif p !=cp:
            context["errmsg"]="Passwords do not match"
            return render(request,'register.html',context)
        
        else:
            try:

            
                u=User.objects.create(username=un,email=cp)
                u.set_password(p)  # use to encrtypt password
                u.save()
                context["success"]="Registration Successful !!"
                return render(request,'register.html',context)
            except:
                context['errmsg']="User Already Exist"
                return render(request,'register.html',context)
        
            


    else:
        return render(request,'register.html')
    
# login view

def ulogin(request):
    context={}
    if request.method=="POST":
        nm=request.POST['lname']
        p=request.POST['lpass']
        

        if nm=="" or p=="":
            context["errmsg"]="Fields can not be empty"
            return render(request,'login.html',context)
        
        else:
            u=authenticate(username=nm,password=p)
            
            print(u)
            if u is not None:
                login(request,u)
                return redirect('/index')

            
            else:
                context["errmsg"]="Invalid Credentials"
                return render(request,'login.html',context)



    else:
        return render(request,'login.html')
    
#logout view
def ulogout(request):
    logout(request)
    return redirect('/index')

def catfilter(request,cv):
    p=Product.objects.filter(category=cv)
    context={}
    context["Product"]=p
    return render(request,'index.html',context)


# use for price sorting(high to low and low to high)
def sortbyprice(request,pv):
    if pv=="0":
      p=Product.objects.all().order_by('-price').filter(is_active=True)
    else:
      p=Product.objects.all().order_by('price').filter(is_active=True)
    context={}
    context["Product"]=p
    return render(request,'index.html',context)


# use for filtering price

def filterbyprice(request):
    mn=request.GET["min"]
    mx=request.GET["max"]
    q1=Q(price__gte=mn)
    q2=Q(price__lte=mx)
    p=Product.objects.filter(q1&q2)
    context={}
    context["Product"]=p
    return render(request,'index.html',context)


def productdetails(request,rid):
    context={}
    p=Product.objects.filter(id=rid)
    context["data"]=p
    return render(request,'product_details.html',context)

def viewcart(request):
    cobj2=Cart.objects.filter(userid=request.user.id)
    context={}
    context["carts"]=cobj2
    return render(request,"viewcart.html",context)

def addtocart(request,pid):
    context={}
    if request.user.is_authenticated:
        p=Product.objects.filter(id=pid)
        u=User.objects.filter(id=request.user.id)
        print(u)
        print(p)
        q1=Q(pid=p[0])
        q2=Q(userid=u[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        if n==1:
            context["msg"]="Product already exist in cart"
            return render(request,"product_details.html",context)
        else:
            cart=Cart.objects.create(pid=p[0],userid=u[0])
            cart.save()
            context["msg"]="Product added to cart"
            return render(request,"product_details.html",context)

        
    else:
        return redirect('/login')

# use to add quantity
def updatequantity(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    print(q)
    if x=="1":
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    return redirect("/vcart")

import random
def placeorder(request):
    c=Cart.objects.filter(userid=request.user.id)
    orderid=random.randrange(1000,9999)
    for x in c:
        amount=x.qty* x.pid.price
        o=Order.objects.create(order_id=orderid,amt=amount,p_id=x.pid,user_id=x.userid)
        o.save()
        #x.delete()
    return redirect('/fetchorder')

def fetchorder(request):
    orders=Order.objects.filter(user_id=request.user.id)
    context={}
    context["orders"]=orders
    sum=0
    for x in orders:
        sum=sum+x.amt
    context["totalamount"]=sum
    context['n']=len(orders)
    return render(request,"placeorder.html",context)

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_SXYCZR7Ug8RjAu", "glLeXQlXAx5p0Y40evd5SAOy"))
    orders=Order.objects.filter(user_id=request.user.id)
    context={}
    context["orders"]=orders
    sum=0

    for x in orders:
        sum=sum+x.amt  
        orderid=x.order_id

        
    data = { "amount": sum, "currency": "INR", "receipt": "orderid" }
    payment = client.order.create(data=data)
    print(payment)
    context["payment"]=payment
    return render(request,"pay.html",context)

#for payment success
def paymentsuccess(request):
    return HttpResponse("Payment Success")