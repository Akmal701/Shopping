from django.contrib import messages
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, HttpResponse

from product.models import Category, Product
from .forms import SearchForm
from .models import Setting, ContactForm, ContactMessage


# Create your views here.
def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:4]
    products_latest = Product.objects.all().order_by('-id')[:4]
    products_picked = Product.objects.all().order_by('?')[:4]
    page = "home"
    context ={'setting': setting,
              'page': page,
              'category':category,
              'products_slider':products_slider,
              'products_latest': products_latest,
              'products_picked':products_picked,
              }
    return render(request, 'index.html', context)


def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Sizning xabaringiz qabul qilindi!Rahmat')
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context = {'setting': setting, 'form': form, }
    return render(request, 'contact.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting':setting,}
    return render(request, 'about.html', context)


def category_products(request, id, slug):
    category = Category.objects.all()
    catdata = Category.objects.get(pk=1)
    products = Product.objects.filter(category_id=id)
    context = {
        'category': category,
        'catdata': catdata,
        'products': products,
    }
    return render(request, 'category_products.html', context)

def search(request):
    if request.method=='POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()
            context = {
                'products': products,
                'query': query,
                'category': category,
            }
            return render(request, 'search.html', context)
    return HttpResponseRedirect('/')