from typing import Union, Optional
import tomli

import json

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet

from test_polar.forms import locationForm, formType
from test_polar.models import PolarModel  # , PolarModel_test  # , Testpage

from nosql_adapter import MongoPolar


def return_configttype() -> list[str]:
    # config = tomli.load(open("../../config.toml", "rb"))
    config = tomli.load(open("config.toml", "rb"))
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


def _return_trainingdata(connection: QuerySet, fname: str) -> Union[dict, None]:
    trainingen = connection.filter(fname=fname)
    if trainingen.values()[0]["trainingdescription"] is not None:
        # return trainingen.values()[0]["trainingdescription"]
        return trainingen.values()[0]
    else:
        return None


def _return_lapdata(connection: QuerySet, fname: str) -> list[Optional[dict]]:
    trainingen = connection.filter(fname=fname)
    if trainingen.values()[0]["laps"] is not None:
        return trainingen.values()[0]["laps"]
    else:
        return trainingen.values()[0]["alaps"]


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
            "summary.html",
            context={
                "trainingen": trainingen,
                "ttypes": ttypes,
            },
        )


def _adapt_test(request: HttpRequest) -> HttpResponse:
    connection = PolarModel.objects.using("default")
    fname = "training-session-2022-01-12-6892575464-df5387b0-e271-48db-b0c2-4735c913b039.json"
    training = _return_trainingdata(connection, fname)
    if request.method == "GET":
        location = {
            # "trainingdescription": training.get("trainingdescription"),
            "location": training.get("location"),
        }
        # print(location)
        ttypeform = locationForm(
            initial=location,
        )
        if not ttypeform.is_valid():
            print(ttypeform.errors)
        else:
            print("yesss")
        return ttypeform
        # return render(request, "adapt.html", {"ttypeform": ttypeform})
    elif request.method == "POST":
        obj_id = training["_id"]
        ttypeform = locationForm(request.POST)
        if ttypeform.is_valid():
            new_location = request.POST["location"]
            mongpol = MongoPolar("polartest", "polar2022")
            mongpol.updateOne(
                obj_id,
                {"location": new_location},
            )
            return ttypeform  # redirect("/polar")
        else:
            print(ttypeform.errors)
            return None
            # return render(request, "add_ttype.html", {"ttypeform": ttypeform})


def show_adapt(request: HttpRequest) -> HttpResponse:
    connection = PolarModel.objects.using("default")
    if request.method == "GET":
        ttypeform = _adapt_test(request)

        if "ttypes" not in request.GET:
            trainingen = _return_trainrunning(connection)
        else:
            ttype = request.GET["ttypes"]
            print(len(ttype))

            trainingen = _return_trainttype(connection, ttype)
        ttypes = return_configttype()
        print(ttypes)
        print(ttypeform)

        return render(
            request,
            "adapt.html",
            context={
                "trainingen": trainingen,
                # "ttypes": ttypes,
                "ttypeform": ttypeform,
            },
        )
    elif request.method == "POST":
        ttypeform = _adapt_test(request)
        trainingen = _return_trainrunning(connection)
        ttypes = return_configttype()
        return render(
            request,
            "adapt.html",
            context={
                "trainingen": trainingen,
                "ttypes": ttypes,
                "ttypeform": ttypeform,
            },
        )


def show_lapdata(request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
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
                "summary.html",
                context={
                    "lapdata": lapdata,
                    "trainingen": trainingen,
                    "ttypes": ttypes,
                },
            )
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"})
    return JsonResponse({"status": "error", "message": "Invalid request method"})
