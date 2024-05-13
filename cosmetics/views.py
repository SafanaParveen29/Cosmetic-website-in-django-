from django.shortcuts import render, redirect
from django.contrib import messages
from CosmeticAdmin.models import *
from .models import *
from django.db.models import Q
from datetime import date,timedelta
from django.shortcuts import get_object_or_404

def header(request):    
    return render(request, 'header.html')

def footer(request):
    return render(request, 'footer.html')

def body(request):
    data = Product.objects.all()
    Name=request.POST.get('q')
    if Name!='' and Name is not None:
        data = data.filter(ProductName__icontains=Name) or data.filter(category__icontains=Name) or data.filter(Subcategory__icontains=Name)
    context = {
        'data':data
    }
    return render(request, 'homebody.html',context)

def product(request):
    data = Product.objects.all()
    Name=request.POST.get('q')
    if Name!='' and Name is not None:
        data = data.filter(ProductName__icontains=Name) or data.filter(category__icontains=Name) or data.filter(Subcategory__icontains=Name)
    context = {
        'data':data
    }
    return render(request, 'product.html',context)

def viewProduct(request,id):
    viewproduct = Product.objects.get(id=id)
    today_date = date.today()
    deliveryDate = today_date + timedelta(weeks=1)
    offer = 0
    offerpercentage = 0
    i = int(viewproduct.offerPrice)
    if (i > 0):
        offer = int(viewproduct.ActualPrice) - int(viewproduct.offerPrice)
        offerpercentage = (offer*100)/int(viewproduct.ActualPrice)

    context1 = {
        'viewproduct' : viewproduct,
        'today_date': today_date,
        'deliveryDate' : deliveryDate,
        'offer' : offer,
        'offerpercentage' : round(offerpercentage)
    }  
    return render(request, 'short-description.html',context1)

def products_by_category(request, category):
    data = Product.objects.filter(category=category)
    data1 = Product.objects.filter(Subcategory=category)
    context = {
        'data':data,
        'data1':data1,
        'category' : category,
        'Subcategory':category
    }  
    return render(request, 'Product.html',context)

def register(request):
    if request.method == "POST":
        CustomerPassword = request.POST.get("CustomerPassword")
        ConfirmPassword = request.POST.get("ConfirmPassword")
        if CustomerPassword == ConfirmPassword:
            FirstName = request.POST.get('FirstName')
            LastName = request.POST.get("LastName")
            username = request.POST.get("username")
            PhoneNumber = request.POST.get("PhoneNumber")
            CustomerEmail = request.POST.get("CustomerEmail")            
            customer = Customer.objects.create(FirstName=FirstName, LastName=LastName, username=username, PhoneNumber=PhoneNumber, CustomerEmail=CustomerEmail, CustomerPassword=CustomerPassword, ConfirmPassword=ConfirmPassword)
            messages.success(request,"User profile has been registered successfully! Please login to continue")
            return redirect('user_login')
        else:
            messages.error(request,"Passwords do not match! Please try again")
            

    return render(request, 'register.html')

def user_login(request):
    if request.session.has_key('username'):
        return redirect('body')
    else:
        if request.method=='POST':
            Username=request.POST.get("username_or_email")
            Email = request.POST.get("username_or_email")
            Password=request.POST.get("CustomerPassword")
            session = Customer.objects.filter((Q(username=Username)|Q(CustomerEmail=Email)),CustomerPassword=Password)
            if session.exists():  
                user = session.first()  
                request.session['username'] = user.username 
                request.session['user_id'] = user.id 
                return redirect('body') 
            else:
                messages.warning(request,'Invalid Username or Password! Please Try Again')

    return render(request, 'login.html')

def user_logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('user_login')

def edit_users(request, id):
    useredit = Customer.objects.get(id=id)
    password = useredit.ConfirmPassword
    if request.method == 'POST':
        OldPassword = request.POST.get("OldPassword")
        
        if OldPassword != password:
            messages.error(request, 'Invalid old Password! Please Try Again')
        else:
            FirstName = request.POST.get("FirstName")
            LastName = request.POST.get("LastName")
            username = request.POST.get("username")
            PhoneNumber = request.POST.get("PhoneNumber")
            CustomerEmail = request.POST.get("CustomerEmail")
            CustomerPassword = request.POST.get("CustomerPassword")
            ConfirmPassword = request.POST.get("ConfirmPassword")
            
            if CustomerPassword == ConfirmPassword:
                # Update user fields and save
                useredit.FirstName = FirstName
                useredit.LastName = LastName
                useredit.username = username
                useredit.PhoneNumber = PhoneNumber
                useredit.CustomerEmail = CustomerEmail
                useredit.CustomerPassword = CustomerPassword
                useredit.ConfirmPassword = ConfirmPassword
                useredit.save()
                
                messages.success(request, "User profile has been updated successfully! Please to continue shopping")
                return redirect('body')
            else:
                messages.error(request, "The password and confirmation do not match")

    return render(request, 'profile.html', {'useredit': useredit})

def wishlist(request):
    return render(request, 'wishlist.html')

def cart(request):
    if 'username' in request.session:
        user_id = request.session['user_id']
        cart_items = Cart.objects.filter(customer=int(user_id))
        total_price = 0
        for i in cart_items:    
            total_price = total_price + i.cart_price + 100

        context={
            'cart_items':cart_items,
            'total_price':total_price,        
        }
        return render(request, 'cart.html',context)
    else:        
        messages.error(request,"Please login to continue!!!")
        return redirect('user_login')

def add_to_cart(request, product_id):
    try:
        user_id=request.session['user_id']
        customer = Customer.objects.get(id=int(user_id))    
        filtered_products = Product.objects.filter(id=product_id).get(id=product_id)
        j = int(filtered_products.offerPrice)
        k = int(filtered_products.ActualPrice)
        if j <= 0:
            price = k
        else:
            price = j
        if filtered_products:
            cart_item, created = Cart.objects.get_or_create(Product=filtered_products,customer=customer)
            cart_item.quantity += 1
            cart_item.cart_price=((cart_item.quantity)*(price))
            cart_item.save()
            return redirect('cart')
    except:
        return redirect('user_login')
        messages.error(request,"Please login to continue!!!")

def remove_from_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart')

def checkout(request):    
    user_id = request.session['user_id']
    cart_items = Cart.objects.filter(customer=int(user_id))
    total_price = 0
    for item in cart_items:    
        total_price = total_price + item.cart_price + 100
    
    context={
        "cart_items":cart_items,
        "total_price":total_price
    }   

    return render(request, 'checkout.html',context)

def place_order(request):
    user_id = request.session.get('user_id')
    customer = Customer.objects.get(id=int(user_id))
    user_cart = Cart.objects.filter(customer=user_id)
    c_pro_li = []   
    qua=[]
    pri=[]
    for i in user_cart:
        c_pro_li.append(i.Product)
        qua.append(i.quantity)
        pri.append(i.cart_price) 
    for quantity, price, pro in zip(qua, pri, c_pro_li):           
        order = Orders.objects.create(customer=customer, product=pro,retailer=pro.subadmin,quantity=quantity,cart_price=price)
    
    if order:
        messages.success(request, 'Order placed successfully.')
        return redirect('order_confirmation') 
    else:
        messages.error(request, 'Failed to place order.')
        return redirect('cart')

def order_confirmation(request):
    if 'username' in request.session:
            user_id = request.session.get('user_id')
            cart_items = Cart.objects.filter(customer=int(user_id))
            cart_items.delete()
            o = Orders.objects.filter(customer=user_id).order_by('-id')
            context={
                "o":o
            }
            return render(request,'order_confirmation.html',context)
    else:
       
        messages.error(request,"Please login to continue!!!")
        return redirect('user_login')




 










