from typing import Union
# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect
from .forms import TrainingForm, TrainingModelForm

from test_training2.models import Trainingtype# , PolarModel#, Testpage, PolarModel


# def show_polar(request: HttpRequest) -> HttpRequest:
#     if request.method == "GET":
#         print(request.body)
#     training = PolarModel.using_mongo().all()
#     # print(len(training))
#     return render(request, "polar.html")

def select_ttype(request: HttpRequest) -> HttpRequest:
    if request.method == "GET":
        print(request.body)
    training = Trainingtype.using_sqlite().all()
    trainingtypes = {"trainingtypes": training}
    # # return HttpResponse("<em> My second X-app!</em>")
    return render(request, "testpage.html", context=trainingtypes)


def _get_typenames() -> list:
    trainings = Trainingtype.using_sqlite().all()
    type_names = [t.type_name for t in trainings ]
    print(type_names)
    return  type_names


def select_ttype2(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        type_names = _get_typenames()
        return render(request,"get_ttype.html",  context={"trainingtypes": type_names})

    elif request.method == "POST":
        # print(request.POST)
        trainingtypes = _get_typenames()
        print(request.POST["type_name"])
        trainsel = Trainingtype.using_sqlite().filter(type_name=request.POST["type_name"])
        print(trainsel[0])
        return render(request, "get_ttype.html", context={"datapath": trainsel[0].datapath, "trainingtypes": trainingtypes})

    else:
        print("xx")
        return render(request, "get_ttype.html")

def add_ttype(request) -> Union[HttpResponse, HttpResponseRedirect]:
    form  = TrainingModelForm()
    # print(dir(form))
    if request.method == "POST":
        print(request.POST)
        form = TrainingModelForm(request.POST,  request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save(commit=True)
        return redirect("select_ttype")
            
    return render(request, "add_ttype.html", {"form": form})

