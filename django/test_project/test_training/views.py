from django.shortcuts import render
from django.http import HttpResponse

from test_training.models import Trainingtype

def test(request):
    training = Trainingtype.objects.all()
    trainingtypes = {"trainingtypes":training}
    # return HttpResponse("<em> My second X-app!</em>")
    return render(request, "testpage.html", context=trainingtypes)

# Create your views here.
