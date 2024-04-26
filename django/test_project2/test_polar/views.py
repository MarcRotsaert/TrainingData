from typing import Union
import json

# from urllib.parse import urlencode


# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse
from django.core.exceptions import ValidationError

# from django.db.models.query import QuerySet
from test_polar.forms import adaptForm, adaptFormLaps  # , formType
from test_polar.models import PolarModel  # , PolarModel_test  # , Testpage

from django.conf import settings
from nosql_adapter import MongoPolar

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
    return redirect("/home/")


def show_polar(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if "dtable" in request.GET:
            collection = request.GET["dtable"]
            print(collection)
            PolarModel.set_dtable(collection)

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


def adapt_distance(request: HttpRequest) -> HttpResponse:
    print(request.POST)
    PolarModel._set_database_adaptlap(request)
    fname = request.POST.get("fname")
    lapdata = PolarModel.return_lapdata(fname)
    ldate = PolarModel._return_trainingdate(fname)
    initdict, hackdict = PolarModel._return_training_adaptdata(fname)
    adaptform = adaptForm().set_form_initial(initdict, hackdict)

    # Simulate a POST request to show_adapt view
    # post_request = HttpRequest()
    # post_request.method = "POST"
    # post_request._body = request.body
    # post_request.content_type = request.content_type
    # post_request._encoding = request.encoding
    # post_request.POST = request.POST
    # return show_adapt(request, fname=fname)

    # redirect_url = "/adapt/?" + urlencode(request.POST)
    # return redirect(redirect_url)

    return render(
        request,
        "adapt.html",
        context={
            "fname": fname,
            "lapdate": ldate,
            "lapdata": lapdata,
            "adaptform": adaptform,
            "update_checked": True,
            "delete_checked": False,
        },
    )


def start_analyze(request: HttpRequest) -> HttpResponse:

    ttypes = _return_configttype()
    if "ttypes" not in request.GET:
        trainingen = PolarModel._return_trainrunning()
    else:
        ttype = request.GET["ttypes"]
        trainingen = PolarModel._return_trainttype(ttype)
    _set_cache_trainingdata(trainingen, 360)

    context = {
        "trainingen": trainingen,
        "ttypes": ttypes,
    }
    return render(request, "analyze.html", context)


def plot_analyze(request, fname):
    if request.method == "GET":
        if fname is not None:
            lapdata = PolarModel.return_lapdata(fname)
            ldate = PolarModel._return_trainingdate(fname)
            print(JsonResponse({"lapdata": lapdata, "ldate": ldate}, safe=False))
            return JsonResponse({"lapdata": lapdata, "ldate": ldate}, safe=False)
        else:
            return HttpResponseBadRequest("No 'fname' parameter provided.")
    else:
        return HttpResponseBadRequest(
            "Invalid request method. This view only accepts GET requests."
        )


def show_adapt(request: HttpRequest, fname: str):
    # connection = PolarModel.objects.using("default")
    if request.method == "GET":
        return request

    if request.method == "DELETE":
        PolarModel.delete_training(request)
        trainingen = PolarModel._return_trainrunning()
        _set_cache_trainingdata(trainingen, 360)
        return redirect(
            request,
            "adapt.html",
            context={
                "trainingen": trainingen,
                "delete_checked": True,
                "update_checked": False,
            },
        )

    if request.method == "POST":
        # try:
        # data = json.loads(request.body.decode("utf-8"))
        # fname = data.pop("fname", None)
        lapdata = PolarModel.return_lapdata(fname)
        ldate = PolarModel._return_trainingdate(fname)
        initdict, hackdict = PolarModel._return_training_adaptdata(fname)
        adaptform = adaptForm().set_form_initial(initdict, hackdict)
        return render(
            request,
            "adapt.html",
            context={
                "fname": fname,
                "lapdate": ldate,
                "lapdata": lapdata,
                "adaptform": adaptform,
                "update_checked": True,
                "delete_checked": False,
            },
        )


def show_adaptlap(request: HttpRequest, fname: str):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        # fname = data.pop("fname", None)
        lapnr = data.get("lapnr", None)
        if lapnr:
            lapnr = int(lapnr)
        lapdata = PolarModel.return_lapdata(fname)
        ldate = PolarModel._return_trainingdate(fname)
        data = {"distance": 1, "lapNumber": lapnr, "fname": fname}
        # form = adaptFormLaps(
        #     data=data, initial={"distance": 0, "lapNumber": 0, "fname": "no"}
        # )
        form = adaptFormLaps(
            data=data,
        )

        if not form.is_valid():  # Validate the form
            print(form.fields["distance"].error_messages)
        return render(
            request,
            "adapt.html",
            context={
                "fname": fname,
                "lapdate": ldate,
                "lapdata": lapdata,
                "adaptform": None,
                "adaptlapform": form,
                "update_checked": True,
                "delete_checked": False,
            },
        )


def show_lapdata(request: HttpRequest, fname: str) -> Union[HttpResponse, JsonResponse]:
    if request.method == "GET":
        # print(dir(PolarModel))
        lapdata = PolarModel.return_lapdata(fname)
        # print(lapdata)
        ttypes = _return_configttype()
        ldate = PolarModel._return_trainingdate(fname)

        return render(
            request,
            "summary.html",
            context={
                "fname": fname,
                "lapdate": ldate,
                "lapdata": lapdata,
                "ttypes": ttypes,
            },
        )
    return JsonResponse(
        {"status": "error", "message": "Invalid request method in " + __name__}
    )
