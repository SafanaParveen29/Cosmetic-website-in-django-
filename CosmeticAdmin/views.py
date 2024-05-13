from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import *
from cosmetics.models import *
from django.db.models import Q

def Admin_dashboard(request):
    if request.session.has_key('admin_username'):
        return render(request, 'index.html',{'user_type':'Admin'})
    else:
        messages.error(request,"Please login to continue!!!")
        return redirect('admin_login')  

def Subadmin_dashboard(request):
    if request.session.has_key('subadmin_username'):
        return render(request, 'index.html',{'user_type':'SubAdmin'})
    else:
        messages.error(request,"Please login to continue!!!")
        return redirect('subadmin_login') 

def admin_register(request):
    if request.method == "POST":
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")
        admin_username = request.POST.get("admin_username")
        if Administator.objects.filter(admin_username=admin_username).exists() == True:
            messages.error(request,"Username already exists! Please choose a different one")
        else:
            if password == password_confirmation:
                admin_email = request.POST.get("admin_email") 
                ContactNumber = request.POST.get("ContactNumber")           
                administator = Administator.objects.create(admin_username=admin_username,admin_email=admin_email,ContactNumber=ContactNumber,password=password,password_confirmation=password_confirmation)
                messages.success(request,"User profile has been registered successfully! Please login to continue")
                return redirect('admin_login')
            else:
                messages.error(request,"Passwords do not match! Please try again later")
    return render(request, 'auth/admin_register.html')

def admin_login(request):
    if request.session.has_key('admin_username'):
        return redirect('Admin_dashboard')
    else:
        if request.method=='POST':
            a=request.POST.get('admin_username')
            b=request.POST.get('password')
            row_records=Administator.objects.filter(admin_username=a,password=b)
            if row_records:
                row = Administator.objects.only('id').get(admin_username=a).id
                request.session['admin_username'] = a
                request.session['user_id'] = row
                return redirect('Admin_dashboard')
            else:
                messages.error(request,'Invalid username or Password')
    return render(request, 'auth/admin_login.html',{'user_type':'Admin'})

def admin_logout(request):
    if 'admin_username' in request.session:
        del request.session['admin_username']
    return redirect('admin_login')

def admin_edit(request,id):
    adminedit = Administator.objects.get(id=id)
    password1 = adminedit.password_confirmation
    context={
        'adminedit' : adminedit,
        'user_type' : 'Admin'
    }
    if request.method == 'POST':
        oldPassword = request.POST.get("oldPassword")
        
        if oldPassword != password1:
            messages.error(request, 'Invalid Password! Please Try Again')
        else:
            admin_username = request.POST.get("admin_username")
            admin_email = request.POST.get("admin_email")
            ContactNumber = request.POST.get("ContactNumber")    
            password = request.POST.get("password")
            password_confirmation = request.POST.get("password_confirmation")
            
            if password == password_confirmation:
                # Update user fields and save
                adminedit = Administator.objects.filter(id=id).update(admin_username=admin_username,admin_email=admin_email,ContactNumber=ContactNumber,password=password,password_confirmation=password_confirmation)
                messages.success(request, "User profile has been updated successfully! Please to continue shopping")
                return redirect('Admin_dashboard')
            else:
                messages.error(request, "The password and confirmation do not match")    
    return render(request, 'auth/admin_edit.html',context)

def subadmin_edit(request,id):
    subadminedit = Subadmin.objects.get(id=id)
    password1 = subadminedit.subadmin_password1
    context = {
        'subadminedit': subadminedit,
        'user_type': 'SubAdmin'
    }
    if request.method == 'POST':
        oldPassword = request.POST.get("oldPassword")
        
        if oldPassword != password1:
            messages.error(request, 'Invalid Password! Please Try Again')
        else:
            subadmin_username = request.POST.get("subadmin_username")
            subadmin_email = request.POST.get("subadmin_email")
            subadmin_Number = request.POST.get("subadmin_Number")    
            subadmin_password = request.POST.get("subadmin_password")
            subadmin_password1 = request.POST.get("subadmin_password1")
            
            if subadmin_password == subadmin_password1:
                # Update user fields and save
                subadminedit = Subadmin.objects.filter(id=id).update(subadmin_username=subadmin_username, subadmin_email=subadmin_email,subadmin_Number=subadmin_Number, subadmin_password=subadmin_password, subadmin_password1=subadmin_password1)
                messages.success(request, "User profile has been updated successfully! Please to continue shopping")
                return redirect('Subadmin_dashboard')
            else:
                messages.error(request, "The password and confirmation do not match")    
    return render(request, 'auth/admin_edit.html',context)

def register_subuser(request):
    if request.session.has_key('admin_username'):        
        if request.method == 'POST':
            subadmin_username = request.POST.get('subadmin_username')
            subadmin_email = request.POST.get('subadmin_email')
            subadmin_Number = request.POST.get('subadmin_Number')
            subadmin_password = request.POST.get('subadmin_password')
            subadmin_password1 = request.POST.get('subadmin_password1')
            admin_username = request.POST.get("admin_username")
            password = request.POST.get("password")
            try:
                administator = Administator.objects.get(admin_username=admin_username,password=password)
            except Administator.DoesNotExist:
                messages.error(request,"Invalid admin credentials!!!")        
            subadmin = Subadmin(administator=administator,subadmin_username=subadmin_username,subadmin_email=subadmin_email,subadmin_Number=subadmin_Number,subadmin_password=subadmin_password,subadmin_password1=subadmin_password1)
            subadmin.save()
            messages.success(request,"User profile has been registered successfully! Please login to continue")
            return redirect('admin_login')
                                        
        return render(request,'auth/subuser_register.html')
    else:
        messages.error(request,"Please contect your admin to register your 'retailer' account")
        return redirect('admin_login')

def subadmin_login(request):
    if request.session.has_key('subadmin_username'):
        return redirect('Subadmin_dashboard')
    else:
        if request.method=='POST':
            a=request.POST.get('subadmin_username')
            b=request.POST.get('subadmin_password')
            row_record=Subadmin.objects.filter(subadmin_username=a,subadmin_password=b)
            if row_record:
                row1 = Subadmin.objects.only('id').get(subadmin_username=a).id
                request.session['subadmin_username'] = a
                request.session['user_id'] = row1
                return redirect('Subadmin_dashboard')
            else:
                messages.error(request,'Invalid username or Password')
    return render(request, 'auth/admin_login.html',{'user_type':'SubAdmin'})

def subadmin_logout(request):
    if 'subadmin_username' in request.session:
        del request.session['subadmin_username']
    return redirect('admin_login')

def AddProduct(request):
    if request.session.has_key('subadmin_username'):        
        if request.method == 'POST':
            category = request.POST.get('category')
            Subcategory = request.POST.get('Subcategory')
            ProductName = request.POST.get('ProductName')
            ActualPrice = request.POST.get('ActualPrice')
            offerPrice = request.POST.get('offerPrice')
            ProductColour = request.POST.get('ProductColour')
            StackQuantity = request.POST.get('StackQuantity')
            DeliveryCost = request.POST.get('DeliveryCost')
            ProductDetails = request.POST.get('ProductDetails')
            ProductInformation = request.POST.get('ProductInformation')
            HowToUse = request.POST.get('HowToUse')
            img1 = request.FILES['img1']
            img2 = request.FILES['img2']
            img3 = request.FILES['img3']
            img4 = request.FILES['img4']
            img5 = request.FILES['img5']
            userid=request.session['user_id'] 
            userId = Subadmin.objects.get(id=int(userid))
            product = Product.objects.create(subadmin=userId,category=category,Subcategory=Subcategory,ProductName=ProductName,
                            ActualPrice=int(ActualPrice),offerPrice=int(offerPrice),ProductColour=ProductColour,
                            StackQuantity=int(StackQuantity),DeliveryCost=float(DeliveryCost),
                            ProductDetails=ProductDetails,ProductInformation=ProductInformation,
                            HowToUse=HowToUse,img1=img1,img2=img2,img3=img3,img4=img4,img5=img5)
            if product:
                messages.success(request,"Product added Successfully!!!")
                return redirect('viewProducts')
            else:
                messages.warning(request,"Something went wrong please try again later!!!")
        return render(request, 'AddProduct.html')
    else:
        messages.error(request,"Please login to continue!!!")
        return redirect('subadmin_login')

def viewProducts(request):
    if request.session.has_key("subadmin_username"):
        userID = request.session["subadmin_username"]
        sub = Subadmin.objects.get(subadmin_username=userID)
        subid=sub.id
    data = Product.objects.filter(subadmin=subid).order_by('-id')
    context = {
        'data':data
    }
    return render(request, 'viewProduct.html',context)

def delete_subuser(request,sid):
    sub = Subadmin.objects.get(id = sid)
    sub.delete()
    messages.success(request,'The retailer hasbeen deleted successfully!')
    return redirect("view_subuser")

def view_subuser(request):
    if request.session.has_key('admin_username'):
        userId = request.session['admin_username']
        adm = Administator.objects.get(admin_username=userId)
        admid = adm.id
    subusers = Subadmin.objects.filter(administator=admid)
    context = {
        'subusers':subusers
    }
    return render(request, 'view_subuser.html',context)    

def update_product(request, pid):
    update  = Product.objects.get(id=pid)
    context = {'update': update}
    if request.method == 'POST':        
        ProductName = request.POST.get("ProductName")
        ActualPrice = request.POST.get("ActualPrice")
        offerPrice = request.POST.get("offerPrice")
        ProductColour = request.POST.get("ProductColour")
        StackQuantity = request.POST.get("StackQuantity")
        DeliveryCost = request.POST.get("DeliveryCost")
        ProductDetails = request.POST.get("ProductDetails")
        ProductInformation = request.POST.get("ProductInformation")
        HowToUse = request.POST.get("HowToUse")

        update = Product.objects.filter(id=pid).update( ProductName=ProductName,ActualPrice=ActualPrice, 
        offerPrice=offerPrice,ProductColour=ProductColour,StackQuantity=StackQuantity,DeliveryCost=DeliveryCost,
        ProductDetails=ProductDetails,ProductInformation=ProductInformation,HowToUse=HowToUse)
        
        if update:
            messages.success(request,"product is updated successfully")
            return redirect("viewProducts")
        else:
            messages.success(request,"you cannot able to update this product")

    return render(request, 'auth/update_product.html', context)
  
def delete_product(request, pid):
    products = Product.objects.get(id=pid)
    products.delete()
    messages.success(request,'The selected product has been deleted')
    return redirect('viewProducts')

def myorders(request):
    rid = request.session.get('subadmin_username')
    retailer_user = Subadmin.objects.get(subadmin_username=rid)
    retailer = retailer_user.id
    order = Orders.objects.filter(retailer=retailer).order_by('-id')
    context={
        'order':order,
        'STATUS_CHOICES' : Orders.STATUS_CHOICES
    }
    
    return render(request,'orders.html', context)

def status(request,id):
    if request.method == "POST":
        status = request.POST.get('status')
        clg = Orders.objects.filter(id=id).update(delivery_status=status)
        if clg:
            messages.success(request,"Order Updated Successfully")
            return redirect("myorders")
        else:
            messages.warning(request,"Error Updating Order")
        
    