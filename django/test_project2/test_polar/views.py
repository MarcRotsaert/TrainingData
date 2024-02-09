from typing import Union
import json

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.core.exceptions import ValidationError

# from django.db.models.query import QuerySet
from test_polar.forms import adaptForm  # , formType
from test_polar.models import PolarModel  # , PolarModel_test  # , Testpage

# from nosql_adapter import MongoPolar

from .utils import (
    _return_configttype,
    _set_cache_trainingdata,
    get_collections_name,
)


def select_collections(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        collections = get_collections_name()
        return render(request, "home.html", context={"dbtables": collections})
    else:
        return request


def redirect_to_home(request: HttpRequest) -> HttpResponse:
    print(request)
    return redirect("home/")


def show_polar(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if "dtable" in request.GET:
            collection = request.GET["dtable"]
            print(collection)
            PolarModel.set_dtable(collection)
            print(PolarModel.check())

        if "ttypes" not in request.GET:
            trainingen = PolarModel._return_trainrunning()
        else:
            ttype = request.GET["ttypes"]
            trainingen = PolarModel._return_trainttype(ttype)

        _set_cache_trainingdata(trainingen, 360)

        ttypes = _return_configttype()
        return render(
            request,
            "summary.html",
            context={
                "trainingen": trainingen,
                "ttypes": ttypes,
            },
        )


def start_adapt(request: HttpRequest) -> HttpResponse:
    trainingen = PolarModel._return_trainrunning()

    if request.method == "GET":
        # TODO: add logging
        print("GET action_adapt")
    elif request.method == "POST":
        print(request.POST)
        PolarModel._set_database_adapt(request)
        trainingen = PolarModel._return_trainrunning()
    _set_cache_trainingdata(trainingen, 360)

    return render(
        request,
        "adapt.html",
        context={
            "trainingen": trainingen,
            "update_checked": True,
        },
    )


def show_adapt(request: HttpRequest, fname: str):
    # connection = PolarModel.objects.using("default")
    # print(__name__)
    if request.method == "GET":
        return request
    elif request.method == "DELETE":
        PolarModel.delete_training(request)
        trainingen = PolarModel._return_trainrunning()
        _set_cache_trainingdata(trainingen, 360)

        return render(
            request,
            "adapt.html",
            context={
                "trainingen": trainingen,
                "delete_checked": True,
                "update_checked": False,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        fname = data.pop("fname", None)
        lapdata = PolarModel.return_lapdata(fname)
        ldate = PolarModel._return_trainingdate(fname)
        initdict, hackdict = PolarModel._return_training_adaptdata(fname)
        # adaptform = _set_form_initial(adaptForm, initdict, hackdict)
        adaptform = adaptForm().set_form_initial(initdict, hackdict)

        return render(
            request,
            "adapt.html",
            context={
                "lapdate": ldate,
                "lapdata": lapdata,
                "adaptform": adaptform,
                "update_checked": True,
                "delete_checked": False,
            },
        )


def show_lapdata(request: HttpRequest, fname: str) -> Union[HttpResponse, JsonResponse]:
    if request.method == "GET":
        print(dir(PolarModel))
        lapdata = PolarModel.return_lapdata(fname)
        # print(lapdata)
        ttypes = _return_configttype()
        ldate = PolarModel._return_trainingdate(fname)

        return render(
            request,
            "summary.html",
            context={
                "lapdate": ldate,
                "lapdata": lapdata,
                "ttypes": ttypes,
                # "trainingen": trainingen,
            },
        )
    return JsonResponse(
        {"status": "error", "message": "Invalid request method in " + __name__}
    )
