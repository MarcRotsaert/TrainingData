from typing import Union, Optional
import tomli

import json

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
# from .forms import TrainingForm, TrainingModelForm
import sys

from test_polar.forms import formType

sys.path.append(r"C:\Users\marcr\Polar\Polar\python")
sys.path.append(r"C:\Users\marcr\Polar\Polar\python\analyzer")

# from nosql_adapter import MongoPolar

from test_polar.models import PolarModel  # , PolarModel_test  # , Testpage


def return_configttype() -> list[str]:
    config = tomli.load(open("../../config.toml", "rb"))
    return config["running"]["trainingtypes"]


def _return_trainttype(connection: QuerySet, ttype: str) -> list[Optional[dict]]:
    if ttype == "easy":
        ttype = "easyrun"
        comp = True
    elif ttype == "road":
        ttype = "roadrace"
        comp = True
    elif ttype == "interval":
        comp = "interval"
    else:
        print(ttype)
        return []
    
    training = connection.filter(trainingtype={ttype: comp})
    # FOR DEBUGGING
    # for val in training.values():
    #     try:
    #         print(val["trainingtype"])
    #     except TypeError:
    #         print("no")
    trainingen = [t for t in training.values()]
    return trainingen


def _return_trainrunning(connection: QuerySet) -> list[Optional[dict]]:
    training = connection.filter(sport="RUNNING")
    if len(training) > 0:
        return [t for t in training.values()]
    else:
        return []


def _return_lapdata(connection: QuerySet, fname: str) -> list[Optional[dict]]:
    trainingen = connection.filter(fname=fname)
    # print(trainingen.values()[0]["laps"])
    if len(trainingen.values()[0]["laps"]) > 0:
        return trainingen.values()[0]["laps"]
    else:
        return []


def show_polar(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        connection = PolarModel.objects.using("default")

        # print(request.POST) # print(request.body)
        if "ttypes" not in request.GET:
            trainingen = _return_trainrunning(connection)
            # training = connection.filter(sport="RUNNING")
        else:
            ttype = request.GET["ttypes"]
            print(len(ttype))

            trainingen = _return_trainttype(connection, ttype)
            # FOR DEBUG PURPOSES
            # trainingen = []
            # for t in range(200):
            #     try:
            #         print(training[t]["fname"])
            #         trainingen.append(training[t])
            #     except ValidationError:
            #         print("no")
            # xx
            # trainingen = [t for t in training.values()]
        
        ttypes = return_configttype()

        return render(
            request,
            "polar.html",
            context={
                "trainingen": trainingen,
                "ttypes": ttypes,
            },
        )




def show_lapdata(request: HttpRequest) -> Union[HttpResponse, JsonResponse] :
    connection = PolarModel.objects.using("default")
    if request.method == "POST":
        try:
            print(request.body)
            data = json.loads(request.body.decode("utf-8"))
            received_data = data.get("lapdata", "")
            lapdata = _return_lapdata(connection, received_data)

            trainingen = _return_trainrunning(connection)
            ttypes = return_configttype()

            return render(
                request,
                "polar.html",
                context={
                    "lapdata": lapdata,
                    "trainingen": trainingen,
                    "ttypes": ttypes,
                },
            )
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"})
    return JsonResponse({"status": "error", "message": "Invalid request method"})



