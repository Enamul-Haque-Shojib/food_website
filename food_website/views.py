from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from food.models import Food, Category

# class HomeView(TemplateView):
#     template_name = 'home.html'

class AboutUsView(TemplateView):
    template_name = 'about_us.html'


def home(request, category_slug = None):
    data = Food.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        data = Food.objects.filter(category = category)
    category = Category.objects.all()
    return render(request, 'home.html', {'data': data, 'category': category, 'type': 'Home Page'})



def search(request):
    query = request.GET['query']
    data = Food.objects.filter(name__icontains=query) | Food.objects.filter(price__icontains=query)
    category = Category.objects.all()
    return render(request, 'home.html', {'data': data, 'category': category, 'type': 'Home Page'})
    