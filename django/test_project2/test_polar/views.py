from typing import Union, Optional
import json
import tomli

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.core.cache import cache

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
    trainingen = [t for t in training.values()]
    return trainingen


def _return_trainrunning(connection: QuerySet) -> list[Optional[dict]]:
    training = connection.filter(sport="RUNNING")
    if len(training) > 0:
        return [t for t in training.values()]
    else:
        return []


def _return_trainingdata(connection: QuerySet, fname: str) -> dict:
    trainingen = connection.filter(fname=fname)
    return trainingen.values()[0]


def _return_lapdata(connection: QuerySet, fname: str) -> list[Optional[dict]]:
    trainingen = connection.filter(fname=fname)
    if trainingen.values()[0]["laps"] is not None:
        return trainingen.values()[0]["laps"]
    else:
        return trainingen.values()[0]["alaps"]


def _set_cache_trainingdata(trainingen: list, cachetime: float):
    cache_key = "training_data"
    cache.clear()
    cache.set(cache_key, trainingen, cachetime)


def show_polar(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        connection = PolarModel.objects.using("default")

        if "ttypes" not in request.GET:
            trainingen = _return_trainrunning(connection)
            # training = connection.filter(sport="RUNNING")
        else:
            ttype = request.GET["ttypes"]
            print(len(ttype))
            print(ttype)

            trainingen = _return_trainttype(connection, ttype)
            print(len(trainingen))

        _set_cache_trainingdata(trainingen, 60)

        ttypes = return_configttype()
        return render(
            request,
            "summary.html",
            context={
                "trainingen": trainingen,
                "ttypes": ttypes,
            },
        )
    else:
        return HttpResponse()


def _set_database(request: HttpRequest, connection):
    new_description = request.POST["trainingdescription-description"]
    new_location = request.POST["location"]
    print(new_description)
    new_location = request.POST["location"]
    new_description = request.POST["trainingdescription-description"]
    # fname = "training-session-2022-01-12-6892575464-df5387b0-e271-48db-b0c2-4735c913b039.json"
    fname = request.POST["fname"]
    training = _return_trainingdata(connection, fname)
    obj_id = training["_id"]
    print(fname)
    db_table = PolarModel._meta.db_table
    config = tomli.load(open("config.toml", "rb"))
    database = config["mongodb"]["database"]

    mongpol = MongoPolar(database, db_table)
    mongpol.updateOne(
        obj_id,
        {
            "location": new_location,
            "trainingdescription": {"description": new_description},
        },
    )


def _get_adapt_form(
    request: HttpRequest,
) -> HttpResponse:
    connection = PolarModel.objects.using("default")
    if request.method == "GET":
        locationform = locationForm()
        print("nonono")
        return locationform

    elif request.method == "POST":
        locationform = locationForm(request.POST)
        return locationform
        # else:
        #     print(locationform.errors)
        #     return None
        #     # return render(request, "add_ttype.html", {"ttypeform": ttypeform})


def action_adapt(request: HttpRequest) -> HttpResponse:
    connection = PolarModel.objects.using("default")
    trainingen = _return_trainrunning(connection)
    print(request.method)

    if request.method == "GET":
        _set_cache_trainingdata(trainingen, 60)
    elif request.method == "POST":
        _set_database(request, connection)
        trainingen = _return_trainrunning(connection)
        _set_cache_trainingdata(trainingen, 60)

    return render(
        request,
        "adapt.html",
        context={
            "trainingen": trainingen,
        },
    )


def show_form(request: HttpRequest, fname: str):
    print(__name__)
    connection = PolarModel.objects.using("default")
    if request.method == "GET":
        return request
    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        fname = data.pop("fname", None)
        if not fname:
            fname = data.get("lapdata", None)
        print(fname)
        lapdata = _return_lapdata(connection, fname)

        training = _return_trainingdata(connection, fname)
        location = training["location"]
        try:
            description = training["trainingdescription"]["description"]
        except:
            description = "unknown"
        print(description)

        locationform = locationForm(
            use_required_attribute=True,
            initial={
                "location": location,
                "fname": fname,
                # TODO: onderstaande werkt allemaal niet.
                #  Waarschijnlijk op te lossen met apart model maken voor form ipv polarmodel
                # "trainingdescription": {"description": description, "type": ""},
                # "trainingdescription-description": "random",
                # "trainingdescription-type": "",
                # "dummy": "tralala",
            },
        )

        # lf_trainingdesc = locationform["trainingdescription-description"]
        # print(dir(lf_trainingdesc))
        print(locationform.fields)
        print(locationform.is_valid())
        print(locationform.errors)

        return render(
            request,
            "adapt.html",
            context={
                "lapdata": lapdata,
                "locationform": locationform,
            },
        )


def show_lapdata(request: HttpRequest, fname: str) -> Union[HttpResponse, JsonResponse]:
    if request.method == "GET":
        print(fname)

        connection = PolarModel.objects.using("default")
        # try:
        #     print(request.GET.keys())
        #     print(request.GET.get("value"))
        #     data = request.GET
        #     # print(request.body)
        #     # data = json.loads(request.body.decode("utf-8"))
        # except json.JSONDecodeError:
        #     return JsonResponse(
        #         {"status": "error", "message": "Invalid JSON in" + __name__}
        #     )
        # received_data = data.get("lapdata", "")
        lapdata = _return_lapdata(connection, fname)

        # trainingen = _return_trainrunning(connection)
        # print(trainingen)
        ttypes = return_configttype()

        return render(
            request,
            "summary.html",
            context={
                "lapdata": lapdata,
                # "trainingen": trainingen,
                "ttypes": ttypes,
            },
        )
    return JsonResponse(
        {"status": "error", "message": "Invalid request method in " + __name__}
    )
