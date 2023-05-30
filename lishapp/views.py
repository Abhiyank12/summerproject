from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth import authenticate,login,logout
from django. contrib import messages
from django.http.response import JsonResponse
import json

# Create your views here.
def home(request):
    return render(request,"home.html")

def index(request):
    data = Carousel.objects.all()
    dic = {'data':data}
    return render(request, "index.html",dic)

def contact(request):
    return render(request, "contact.html")

def main(request):
    data = Carousel.objects.all()
    dic = {'data':data}
    return render(request, "index.html",dic)

def about(request):
    return render(request,"about.html")

def adminlog(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                msg="user login sucessfull"
                return redirect('dashboard')
               
            else:
                msg = "Invalid Credentials"
        except:
            msg = "Invalid Credentials"
    dic = {'msg': msg}
    
    return render(request, 'admin_login.html', dic)


 
def adminbase(request):
    if not request.user.is_staff:
        return redirect('adminlog')
    return render(request,"admin-base.html")

def dashboard(request):
    if not request.user.is_staff:
        return redirect('adminlog')
    return render(request,"dashboard.html")
#category
def addcat(request):
    if request.method == 'POST':
        lname = request.POST['name']
        if category.objects.filter(name=lname).exists():
           messages.error(request,"category must be different")
        else:
           category.objects.create(name=lname)
           messages.success(request,"category added")
           return redirect('vcat')
         
    return render(request,"addcat.html",locals())

def vcat(request):
    if not request.user.is_staff:
        return redirect('adminlog')
    Category = category.objects.all()
    return render(request,"vcat.html", locals())

def ecat(request, pid):
    if not request.user.is_staff:
        return redirect('adminlog')
    Category = category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        Category.name = name
        message ="produxt added"
        Category.save()
        return redirect('vcat')
    return render(request, 'ecat.html', locals())

def dcat(request,pid):
    if not request.user.is_staff:
        return redirect('adminlog')
    Category = category.objects.get(id=pid)
    Category.delete()
    messages.success(request,"Category deleted")
    return redirect('vcat')
#product

def addproduct(request):
    if not request.user.is_staff:
        return redirect('adminlog')
    Category = category.objects.all()
    if request.method == "POST":
       name = request.POST['name']
       description = request.POST['description']
       image= request.FILES['image']
       quantity = request.POST['quantity']
       price = request.POST['price']
       cat= request.POST['category']
       mfgdate = request.POST['mfgdate']
       expdate = request.POST['expdate']
       catobj = category.objects.get(id=cat)
       Product.objects.create(name=name,description=description,category=catobj,image=image,quantity=quantity,price=price,mfgdate=mfgdate,expdate=expdate)
    
       messages.success(request,"product added")
       return redirect('dashboard-vproduct')
    return render(request,"addproduct.html",locals())

def vproduct(request):
    if not request.user.is_staff:
        return redirect('adminlog')
    product =Product.objects.all()
    return render(request,"vproduct.html", locals())

def epro(request, pid):
    if not request.user.is_staff:
        return redirect('adminlog')
    product = Product.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        product.name = name
        product.save()
        msg = "product Updated"
        return redirect('dashboard-vproduct')
    return render(request, 'epro.html', locals())

def dpro(request,pid):
    if not request.user.is_staff:
        return redirect('adminlog')
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request,"product deleted")
    return redirect('dashboard-vproduct')

def adminlogout(request):
    logout(request)
    messages.success(request,"logout sucessfully")
    return redirect('main')

#userregis
def userregis(request):
    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['phone_no'] 
        if UserProfile.objects.filter(phoneno=mobile).exists():
           messages.error(request,"phone number must be different")
     
        else:
         user =User.objects.create_user(username=email,last_name=lname,first_name=fname,password=password,email=email)
         UserProfile.objects.create(user=user,address=address,phoneno=mobile)
         user.save()
         messages.success(request,"user registered sucessfully")
    return render(request,'userregist.html',locals())

def ulogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            messages.success(request,"login sucessful")
            return redirect('main')
        else:
            messages.error(request,"invalid user")
    return render(request, 'login.html', locals())

def logoutuser(request):
    logout(request)
    messages.success(request,"logout sucessfully")
    return redirect('main')

def userprofile(request):
    data = UserProfile.objects.get(user = request.user)
    if request.method =="POST":
        lname = request.POST['lname']
        fname = request.POST['fname']
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['phone_no']
        data.save()
        user = User.objects.filter(id= request.user.id).update(first_name=fname,last_name=lname)
        UserProfile.objects.filter(id=data.id).update(address=address,phoneno =mobile)
        msg="Successfully updated"
        return redirect('userprofile')
    return render(request, 'profile.html', locals())

def changepass(request):
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        user = authenticate(name= request.user.username,password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('main')
           
            else:
                messages.success(request, "Password mnot matched")
                return redirect('change_password')
        else:
            mag="Invalid Password"
            return redirect('change_password')
    return render(request, 'change_password.html')

def user_product(request,pid):
    if pid==0:
        product = Product.objects.all()
    else:
        Category= category.objects.get(id=pid)
        product = Product.objects.filter(category=category)
    allCategory = category.objects.all()
    return render(request, "user_product.html", locals())

# add to cart
def addToCart(request, pid):
    if not request.user.is_authenticated:
        return redirect('ulogin')
    myli = {"objects":[]}
    try:
        cart = Cart.objects.get(user=request.user)
        myli = json.loads((str(cart.product)).replace("'", '"'))
        try:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
        except:
            myli['objects'].append({str(pid):1})
        cart.product = myli
        cart.save()
    except:
        myli['objects'].append({str(pid): 1})
        cart = Cart.objects.create(user=request.user, product=myli)
    return redirect('cart')

def incredecre(request, pid):
    cart = Cart.objects.get(user=request.user)
    if request.GET.get('action') == "incre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
    if request.GET.get('action') == "decre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        if myli['objects'][0][str(pid)] == 1:
            del myli['objects'][0][str(pid)]
        else:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) - 1
    cart.product = myli
    cart.save()
    return redirect('cart')

def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        product = (cart.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
    except:
        product = []
    lengthpro = len(product)
    return render(request, 'cart.html', locals())

def deletecart(request, pid):
    cart = Cart.objects.get(user=request.user)
    product = (cart.product).replace("'", '"')
    myli = json.loads(str(product))
    del myli['objects'][0][str(pid)]
    cart.product = myli
    cart.save()
    messages.success(request, "Delete Successfully")
    return redirect('cart')
   
#manage user
def vuser(request):
    User =UserProfile.objects.all()
    return render(request,"manage_user.html", locals())

def duser(request,pid):
    profile = UserProfile.objects.get(id=pid)
    profile.user.delete()
    messages.success(request,"deleted sucessfully")
    return redirect('dashboard-vuser')

def product_detail(request, pid):
    product = Product.objects.get(id=pid)

    return render(request, "product_detail.html", locals())

def booking(request):
    if not request.user.is_authenticated:
        return redirect('ulogin')
    user = UserProfile.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)
    total = 0
    productid = (cart.product).replace("'", '"')
    productid = json.loads(str(productid))
    try:
        productid = productid['objects'][0]
    except:
        messages.success(request, "Cart is empty, Please add product in cart.")
        return redirect('cart')
    for i,j in productid.items():
        product = Product.objects.get(id=i)
        total += int(j) * int(product.price)
    if request.method == "POST":
        book = Booking.objects.create(user=request.user, product=cart.product, total=total)
        cart.product = {'objects':[]}
        cart.save()
        messages.success(request, "Book Order Successfully")
        return redirect('payment')
    return render(request, "booking.html", locals())
def myOrder(request):
    order = Booking.objects.filter(user=request.user)
    return render(request, "order.html", locals())

def change_order_status(request, pid):
    order = Booking.objects.get(id=pid)
    status = request.GET.get('status')
    if status:
        order.status = status
        order.save()
        messages.success(request, "Order status changed.")
    return redirect('myorder')

def admin_changepass(request):
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('dashboard')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_changepass')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_changepass')
    return render(request, 'adminpass.html')

def manage_order(request):
    action = request.GET.get('action', 0)
    order = Booking.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        order_status = 'All'
    return render(request, 'manage_order.html', locals()) 
    
def delete_order(request, pid):
    order = Booking.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('delete_order')


def payment(request):
    total = request.GET.get('total')
    cart = Cart.objects.get(user=request.user)
    if request.method == "POST":
        book = Booking.objects.create(user=request.user, product=cart.product, total=total)
        cart.product = {'objects': []}
        cart.save()
        messages.success(request, "Book Order Successfully")
        return redirect('myorder')
    return render(request, 'payment.html', locals())











 

