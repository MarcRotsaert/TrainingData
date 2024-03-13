from typing import Union

import tomli

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from .forms import TrainingForm, TrainingModelForm

from test_training2.models import Trainingtype  # , PolarModel#, Testpage, PolarModel


def select_ttype(request: HttpRequest) -> HttpRequest:
    config = tomli.load(open("config.toml", "rb"))

    if request.method == "GET":
        print(request.body)
    # training = Trainingtype.using_sqlite().all()
    trainingtypes = config["running"]["trainingtypes"]

    ttypes = []
    for ind, t in enumerate(trainingtypes):
        ttypes.append({"type_name": t, "datapath": str(ind)})

    # trainingtypes = {"trainingtypes": trainingtypes}
    return render(request, "testpage.html", context={"ttypes": ttypes})


def add_ttype(request) -> Union[HttpResponse, HttpResponseRedirect]:
    form = TrainingModelForm()
    # print(dir(form))
    if request.method == "POST":
        print(request.POST)
        form = TrainingModelForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save(commit=True)
        return redirect("select_ttype")

    return render(request, "add_ttype.html", {"form": form})
