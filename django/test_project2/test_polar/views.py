from typing import Union
import tomli

import json

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ValidationError

# from .forms import TrainingForm, TrainingModelForm
import sys

from test_polar.forms import formType

sys.path.append(r"C:\Users\marcr\Polar\Polar\python")
sys.path.append(r"C:\Users\marcr\Polar\Polar\python\analyzer")

from nosql_adapter import MongoPolar

from test_polar.models import PolarModel, PolarModel_test  # , Testpage


def show_polar(request: HttpRequest) -> HttpRequest:
    # config = tomli.load(open("../../config.toml", "rb"))
    # import os

    # curdir = os.getcwd()
    # os.chdir("../..")
    # curs = MongoPolar("polartest4", "polar2014").simplequery(
    #     "trainingtype.easyrun", True
    # )
    # os.chdir(curdir)

    if request.method == "GET":
        connection = PolarModel.objects.using("default")

        # print(request.POST) # print(request.body)
        if "ttypes" not in request.GET:
            training = connection.filter(sport="RUNNING")
        else:
            ttype = request.GET["ttypes"]
            print(len(ttype))
            if ttype == "easy":
                ttype = "easyrun"
                comp = True
                # xx
            elif ttype == "road":
                ttype = "roadrace"
                comp = True
            elif ttype == "interval":
                comp = "interval"
            else:
                print(ttype)

            training = connection.filter(trainingtype={ttype: comp})
            for val in training.values():
                try:
                    print(val["trainingtype"])
                except TypeError:
                    print("no")
        # training = training.order_by("startTime")

        trainingen = [t for t in training.values()]
        ttypes = return_ttype()
        return render(
            request,
            "polar.html",
            context={
                "trainingen": trainingen,
                "ttypes": ttypes,
            },
        )


def return_lapdata(request) -> HttpResponse:
    connection = PolarModel.objects.using("default")
    if request.method == "POST":
        try:
            print(dir(request))
            print(request.body)
            data = json.loads(request.body.decode("utf-8"))
            received_data = data.get("lapdata", "")
            trainingen = connection.filter(fname=received_data)
            print(trainingen.values()[0]["laps"])
            x = trainingen.values()[0]["laps"]
            print(trainingen.values()[0]["alaps"])
            # x = trainingen.values()[0]["alaps"]
            lapdata = trainingen.values()[0]["laps"]
            # Process the received_data as needed
            training = connection.filter(sport="RUNNING")
            trainingen = [t for t in training.values()]
            ttypes = return_ttype()

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


def return_ttype() -> HttpRequest:
    config = tomli.load(open("../../config.toml", "rb"))

    return config["running"]["trainingtypes"]


# as a test
def return_easy(ttype: str) -> HttpRequest:
    if request.method == "GET":
        connection = PolarModel.objects.using("default")
        training = connection.filter(sport="RUNNING")
        print(len(training))
        lenrunning = str(len(training))

        trainingen = [t for t in training.values()]
        print(trainingen[0].keys())

        for t in training.values():
            try:
                print(t["laps"][0]["distance"])
            except TypeError:
                print("probably None laps")

        ttypes = return_ttype()
        print(ttypes)
        return render(
            request,
            "polar.html",
            context={
                "trainingen": trainingen,
                "lenrunning": lenrunning,
                "ttypes": ttypes,
            },
        )
