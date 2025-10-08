from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about_me(request):
    return render(request, 'about_me.html')

def projects(request):
    return render(request, 'projects.html')

def skills(request):
    return render(request, 'skills.html')

def contact_me(request):
    return render(request, 'contact_me.html')