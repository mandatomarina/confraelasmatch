from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def page(request, page_name):
    return render(request, 'pages/'+page_name+'.html')
   