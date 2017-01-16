from django.http import HttpResponse
from django.shortcuts import render
from awsomeProject.models import Product

def index(request):
    #data = Product(title="Panda")
    #data.save()
    return render(request, "index.html", {"title" : Product.objects.values('title').filter(pk=1)[0]['title']})
