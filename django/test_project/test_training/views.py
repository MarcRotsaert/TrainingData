from django.shortcuts import render

from django.http import HttpResponse

def test(request):
    # return HttpResponse("<em> My second X-app!</em>")
    return render(request, "testpage.html", {})

# Create your views here.
