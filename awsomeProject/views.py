from django.http import HttpResponse
from django.shortcuts import render
from .models import Product

effing = True

def index(request):
    if effing == True:
        data = Product(title="Panda")
        data.save()
        effing = False
    return render(request, "index.html", {"title" : Product.objects.values('title').filter(pk=1)[0]['title']})
