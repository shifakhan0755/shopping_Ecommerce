from django.shortcuts import render,redirect
from django.views import View
from .models import Cart,Customer,Product,OrderPlaced
from .forms import CustomerRegistrationForm,LoginForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#def home(request):
# return render(request, 'app/home.html')

class ProductView(View):
 def get(self,request):
  totalitem = 0
  topwears =Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  laptops = Product.objects.filter(category='L')
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops,'totalitem':totalitem})

class ProductDetailView(View):
 def get(self,request,pk):
  totalitem = 0
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart ':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
 user = request.user
 product = request.GET.get('prod_id')
 product1 = Product.objects.get(id=product)
 Cart(user=user,product=product1).save()
 return redirect('/cart/')

@login_required
def show_cart(request):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
  user=request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    totalamount = amount + shipping_amount
    print(totalamount)
   return render(request,'app/addtocart.html',{'cart':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
  else:
   return render(request,'app/emptycart.html',{'totalitem':totalitem})

def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount

  data = {
    'quantity' : c.quantity,
    'amount':amount,
    'totalamount': amount + shipping_amount
  }
  return JsonResponse(data)


def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount

  data = {
    'quantity' : c.quantity,
    'amount':amount,
    'totalamount': amount + shipping_amount
  }
  return JsonResponse(data)


@login_required
def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount

  data = {
    'amount':amount,
    'totalamount': amount + shipping_amount
  }
  return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
 totalitem = 0
 add=Customer.objects.filter(user=request.user)
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary','totalitem':totalitem})

@login_required
def orders(request):
 totalitem = 0
 op = OrderPlaced.objects.filter(user=request.user)
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/orders.html',{'placed':op,'totalitem':totalitem})



def mobile(request,data=None):
 totalitem = 0
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'apple' or data == 'samsung' or data == 'oppo':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def laptop(request,data=None):
 totalitem = 0
 if data == None:
  laptops = Product.objects.filter(category='L')
 elif data == 'macbook' or data == 'hp' or data == 'asus':
  laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'below':
  laptops = Product.objects.filter(category='L').filter(discounted_price__lt=30000)
 elif data == 'above':
  laptops = Product.objects.filter(category='L').filter(discounted_price__gt=30000)
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/laptop.html',{'laptops':laptops,'totalitem':totalitem})

def topwear(request,data=None):
 if data == None:
  topwears = Product.objects.filter(category='TW')
 elif data == 'only' or data == 'levis' or data == 'lee':
  topwears = Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'below':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=1000)
 elif data == 'above':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=1000)
 return render(request, 'app/topwear.html',{'topwears':topwears})

def bottomwear(request,data=None):
 if data == None:
  bottomwears = Product.objects.filter(category='BW')
 elif data == 'only' or data == 'lee' or data == 'levis':
  bottomwears = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'below':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=30000)
 elif data == 'above':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=30000)
 return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears})


class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 def post(self,request):
  form=CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'Congratulations!! Registered Successfully')
   form.save()
  return render(request,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
 totalitem = 0
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70.0
 total_amount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
  totalamount = amount+shipping_amount
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})

@login_required
def payment_done(request):
  totalitem = 0
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
   OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
   c.delete()
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  return redirect("orders",{'totalitem':totalitem})

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
 def get(self,request):
  form=CustomerProfileForm()
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

 def post(self,request):
  form=CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
   reg.save()
   messages.success(request,'Congratulation!! profile updated successfully')
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})


