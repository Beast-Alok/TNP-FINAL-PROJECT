from django.shortcuts import render

# Create your views here.

def testlanding(request):
    return render(request, 'livetestlanding.html')

def livetestportalpage(request):
    return render(request, 'livetestportalpage.html')