from django.shortcuts import render, redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

# from contacts.models import Contact

from listings.models import Contact

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Юзер уже существует')
                return render(request,'accounts/register.html')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Емэйл уже используется')
                    return render(request,'accounts/register.html')
                else:
                    user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                    user.save();
                    messages.success(request,'Вы зарегестрированы')
                    return redirect('accounts:login')

        else:
            messages.error(request,'Пароли не совпадают')
            return redirect('accounts:register')
    else:
        return render(request,'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password) 
        if user is not None:
            auth.login(request, user)
            messages.success(request,'Вы успешно зарегестрированы')
            return redirect('accounts:dashboard')
        else:
            messages.error(request,'Неправильный логин или пароль')
            return redirect('accounts:login')

    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'Вы уже не авторизованны')
        return redirect('index')
    
    return redirect('index')

def dashboard(request):
    

    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts':user_contacts,
        

    }
    return render(request,'accounts/dashboard.html',context)


def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['Sellers']).exists()


@login_required
@user_passes_test(is_in_multiple_groups) 
def vse_zayavki(request):
    vse_zayavki = Contact.objects.order_by('-contact_date')
    paginator = Paginator(vse_zayavki, 10)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    
    context = {
            'contacts':paged_listings,
          
                }
    return render(request,'accounts/vse_zayvki.html',context)
    