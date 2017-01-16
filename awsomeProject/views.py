from django.http import HttpResponse
from django.shortcuts import render
from .models import Product


def index(request):
    if Product.objects.filter(pk=1).exists():
        data = Product(title="Panda")
        data.save()
    return render(request, "index.html", {"title" : Product.objects.values('title').filter(pk=1)[0]['title']})
