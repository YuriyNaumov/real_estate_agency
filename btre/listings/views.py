from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Listing, Contact 
from .choices import bedroom_choices, price_choices, state_choices
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from .forms import ContactForm
from datetime import datetime, timedelta
from django.conf import settings



# Create your views here.
def index(request):
    listings = Listing.objects.order_by('price').filter(is_published=True)

    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    
    context = {'listings': paged_listings}
    return render(request,'listings/listings.html', context)

def listing(request, listing_id): #listing_id is from url.py - path('<int:listing_id>',views.listing,name='listing'), 
  
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        realtor_email = request.POST.get('realtor_email','')

        if form.is_valid():
            if request.user.is_authenticated:
                today = datetime.now()
                tomorrow = today + timedelta(days=1)
                user_id = request.user.id 
                has_contracted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id, contact_date__lte=str(tomorrow))
                if has_contracted:
                    messages.error(request,'Вы уже оставляли заявку на этот объект за прошлые сутки')
                    return redirect('/listings/'+str(listing_id))
            
            form.save(commit=True)
            
            listing_post = request.POST.get('listing','')
            name = request.POST.get('name','')
            email = request.POST.get('email','')
            phone = request.POST.get('phone','')
            message = request.POST.get('message','')
            realtor_email = request.POST.get('realtor_email','')
            
            myemail = EmailMessage(
                subject = 'Запрос на выставленный объект',
                body = "Запрашивается объект" + listing_post + ' Клиент - ' + name +' Email-'+ email + ' Телефон-'+ phone +' Текст-'+ message,
                from_email = settings.EMAIL_HOST_USER, 
               
                to = [realtor_email,'yuriy.naumov@gmail.com'],
                reply_to=[realtor_email],
                )
            
            now = datetime.now()
            current_year = str(now.year)
            current_month = now.month
            if current_month < 10:
                current_month = str(0)+str(current_month)
            else:
                current_month = str(current_month)
            current_day = str(now.day)

            save_path = (settings.MEDIA_ROOT + '/'+'files/'+ current_year+'/'+current_month+'/'+current_day+'/'+request.FILES['file'].name).replace(' ','_')
            
            myemail.attach_file(save_path)
        
        # 
            myemail.send() 
            messages.success(request,'Письмо отправлено')

            # return HttpResponseRedirect(reverse('listing'))

            return redirect('/listings/'+str(listing_id))
            
    
    else:
        form= ContactForm() 

  

    listing = get_object_or_404(Listing, pk=listing_id)
    
    context = {
        'listing':listing,
        'form':form
    }

  
    return render(request,'listings/listing.html',context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
        # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
        
        # city 
    if 'city' in request.GET:
        keywords = request.GET['city']
        if keywords:
            queryset_list = queryset_list.filter(city__iexact=keywords)
        
        # State 
    if 'state' in request.GET:
        keywords= request.GET['state']
        if keywords:
            queryset_list = queryset_list.filter(state__iexact=keywords)
      
      # Bedrooms 
    if 'bedrooms' in request.GET:
        keywords= request.GET['bedrooms']
        if keywords:
            queryset_list = queryset_list.filter(bedrooms__iexact=keywords)
    
    # Price
    if 'price' in request.GET:
        keywords= request.GET['price']
        if keywords:
            queryset_list = queryset_list.filter(price__lte=keywords)



    context = {
         'state_choices':state_choices,
         'bedroom_choices':bedroom_choices,
         'price_choices':price_choices,
         'listings':queryset_list,
         'values':request.GET

    }
    return render(request,'listings/search.html',context)