from typing import Union
import tomli

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

# from .forms import TrainingForm, TrainingModelForm
import sys

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
        print("to get!")
        connection = PolarModel.objects.using("default")
        training = connection.filter(trainingtype={"roadrace": True})
        for val in training.values():
            try:
                print(val["trainingtype"])
            except TypeError:
                print("no")

        # xx
        # connection = PolarModel.objects.using("default")
        # dir(connection.first())
        # print(dir(connection))
        # print(connection.filter(sport="RUNNING"))

        # training = connection.filter(speed={"avg": 13.8})

        # training = connection.filter(
        #     trainingtype__contains={
        #         "interval": "no interval, crit. 3, under investigation."
        #     }
        # )
        # for val in training.values():
        #     print(val["speed"]["avg"])
        #     try:
        #         print(val["trainingtype"])
        #     except:
        #         print("no")
        # pass
        # xx
        # print(len(training))
        lenrunning = str(len(training))

        trainingen = [t for t in training.values()]
        # print(trainingen[0].keys())

        # print(training.values()[0]["speed"]["avg"])
        # print(training.values()[0]["alaps"][0])
        # for t in training.values():
        #     try:
        #         print(t["laps"][0]["distance"])
        #     except TypeError:
        #         print("probably None laps")

        ttypes = return_ttype()
        # print(ttypes)
        return render(
            request,
            "polar.html",
            context={
                "trainingen": trainingen,
                "lenrunning": lenrunning,
                "ttypes": ttypes,
            },
        )


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

        # print(training.values()[0]["speed"]["avg"])
        # print(training.values()[0]["alaps"][0])
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


# {% url 'test_training2:addttype' %}
