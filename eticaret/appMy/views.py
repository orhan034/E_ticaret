from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import *
# Create your views here.

def index(request):
   products = Product.objects.all()
   categorys = Category.objects.all()
   son_gelenler = Product.objects.all().order_by('-date_now')[:3]
   cok_satilanlar = Product.objects.all().order_by('?')[:3]
   context = {
      'title':'Anasayfa',
      'products':products,
      'categorys':categorys,
      'son_gelenler':son_gelenler,
      'cok_satilanlar':cok_satilanlar,
   }
   return render(request, 'index.html', context)


def loginUser(request):
   context = {
      'title':'Giriş Yap',
   }
   if request.method == 'POST':
      if request.POST['girisbutton'] == 'Giriş Yap':
         username = request.POST['username']
         password = request.POST['password']
         user = authenticate(username=username,password=password)
         if user is not None:
            login(request, user)
            return redirect('index')
         else:
            messages.success(request, 'Kullanıcı adı veya şifre hatalı!!')
            return redirect('loginUser')

      if request.POST['girisbutton'] == 'Kayit Ol':
         name = request.POST['name']
         surname = request.POST['surname']
         email = request.POST['email']
         username = request.POST['username']
         password1 = request.POST['password1']
         password2 = request.POST['password2']

         if password1== password2:
            if not User.objects.filter(username=username).exists():
               if not User.objects.filter(email=email).exists():
                  user = User.objects.create_user(email = email,
                                                username = username,
                                                password = password1,
                                                first_name = name,
                                                last_name = surname)
                  user.save()
                  userprofil = UserProfil(user=user)
                  userprofil.save()
                  return redirect('loginUser')
               else:
                  messages.warning(request, 'Bu email zaten kullanılıyor!!')
                  return redirect('loginUser')
            else:
               messages.warning(request, 'Bu username zaten kullanılıyor!!')
               return redirect('loginUser')   
         else:
            messages.warning(request, 'Şifreler aynı değil!!')
            return redirect('loginUser')

   return render(request, 'user/login.html', context)


def logoutUser(request):
   logout(request)
   return redirect('index')
    
def products(request):
   products = Product.objects.all()
   categorys = Category.objects.all()
   paginator = Paginator(products, 6)  # Show 25 contacts per page.
   page_number = request.GET.get('page')
   products = paginator.get_page(page_number)
   context = {
      'title':'Ürünler',
      'products':products,
      'categorys':categorys,
   }
   return render(request, 'products.html', context)

def marka(request,mid):
   marka = Category.objects.get(id = mid)
   markaurun = Product.objects.filter(category = mid)
   paginator = Paginator(markaurun, 4)  # Show 25 contacts per page.
   page_number = request.GET.get('page')
   markaurun = paginator.get_page(page_number)
   context = {
      'title':marka,
      'marka':marka,
      'markaurun':markaurun,
   }
   return render(request, 'marka.html',context)

def detail(request,id):
   product = Product.objects.get(id=id)
   comments = Comment.objects.filter(product=product)
   if request.method == 'POST':
      title = request.POST['title']
      text = request.POST['text']
      comment = Comment(title=title,text=text,product=product, user = request.user)
      comment.save()
        
      return HttpResponseRedirect("/detay/"+id+"/")
   context = {
      'title':"Detay",
      'product':product,
      'comments':comments,
   }
   return render(request, 'detail.html', context)


def profilUser(request):
   user = User.objects.get(username = request.user)
   profils = UserProfil.objects.get(user = user)

   if request.method == 'POST':
      if request.POST['formbutton'] == 'profilChange':
         job = request.POST.get('job')
         deneyim = request.POST.get('deneyim')
         email = request.POST.get('email') 
         website = request.POST.get('website') 
         tel = request.POST.get('tel') 
         address = request.POST.get('address') 
         profils.job = job
         profils.deneyim = deneyim
         user.email = email
         profils.web_site = website
         profils.phone = tel
         profils.address = address
         profils.save()
         user.save()
         return redirect('profilUser')

      if request.POST['formbutton'] == 'imageChange':
         image = request.FILES.get('image')
         profils.image = image
         profils.save()
         return redirect('profilUser')
      
      if request.POST['formbutton'] == 'sifreChange':
         password1 = request.POST['password1']
         password2 = request.POST['password2']
         password3 = request.POST['password3']
         user = User.objects.get(username = request.user)
         if user.check_password(password1):
            if password2==password3:
               user.set_password(password3)
               user.save()
               
               return redirect('loginUser')
   context = {
      'title':"Profil",
      "user":user,
      'profils':profils,
   }
   return render(request, 'user/profil.html',context)

