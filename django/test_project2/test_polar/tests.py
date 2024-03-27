# import settings
import os
import tomli
import glob
import json
import pprint

import unittest
from datetime import datetime, timedelta
from djongo import models as mongomod

# print(settings)
from django.conf import settings
from django.test import TestCase

from .models import (
    PolarModel,
)
from .forms import adaptForm

# from python.nosql_adapter import MongoPolar, MongoForerunner
from parsing.polar_parser import Parser
from analyzer import polar_analyzer as pol_an

# Create your tests here.
# print(settings.DATABASES)


# @unittest.skip
class TestPolarModel(unittest.TestCase):
    def setUp(self):

        config = tomli.load(open("config.toml", "rb"))
        path = config["polar_json"]["datapath"]
        year = 2013
        files = glob.glob(
            os.path.join(path, "training-session-" + str(year) + "-*.json")
        )
        print(path)
        fields = PolarModel._meta.fields
        PolarModel._meta.db_table = "dummy"
        field_names = [
            field.name
            for field in fields
            if not isinstance(field, mongomod.EmbeddedField)
            and not isinstance(field, mongomod.ArrayField)
        ]
        fi = files[3]
        filename = fi.split("\\")[-1]
        sess = pol_an.Trainses_json(filename)
        resume = sess.abstract
        resume.update({"laps": sess.laps, "alaps": sess.alaps})
        polar_data = Polargenerator().return_polardata(
            id_value=1, resume=resume, field_names=field_names
        )
        # Create test data for a PolarModel object
        # Create and save a PolarModel object
        self.polar_model = PolarModel.objects.create(**polar_data)

    def test_polar_model_creation(self):
        # Retrieve the PolarModel object from the database
        polar_model_from_db = PolarModel.objects.first()
        # Assert that the retrieved object matches the one created in setUp()
        self.assertEqual(polar_model_from_db.sport, "RUNNING")
        self.assertEqual(polar_model_from_db.fname, "test_session.json")
        # xx
        # Add more assertions for other fields as needed

    # Add more test methods as needed

    def tearDown(self):
        # Clean up after each test
        self.polar_model.delete()


# @unittest.skip
class DummyTest(TestCase):
    def setUp(self):
        print(os.getcwd())
        config = tomli.load(open("config.toml", "rb"))
        path = config["polar_json"]["datapath"]
        year = 2013
        self.files = glob.glob(
            os.path.join(path, "training-session-" + str(year) + "-*.json")
        )
        print(path)
        fields = PolarModel._meta.fields
        PolarModel._meta.db_table = "dummy"
        field_names = [
            field.name
            for field in fields
            if not isinstance(field, mongomod.EmbeddedField)
            and not isinstance(field, mongomod.ArrayField)
        ]

        print(self.files[0])
        polgen = Polargenerator()

        igen = id_generator()

        for i, fi in enumerate(self.files):
            id_value = next(igen)

            filename = fi.split("\\")[-1]
            sess = pol_an.Trainses_json(filename)
            resume = sess.abstract
            resume.update({"laps": sess.laps, "alaps": sess.alaps})

            polar_data = polgen.return_polardata(id_value, resume, field_names)
            pol = PolarModel(**polar_data)
            pol = PolarModel.objects.create()
            pol.speed = resume["speed"]
            pol.clean()

            pol.save()

    def test_one(self):
        pol = PolarModel.objects.all()
        for p in pol:
            print(p.fname)
        # print(pol[3].speed)
        self.assertEqual(PolarModel.objects.count(), 24)


class Polargenerator:
    polar_dummy_data = {
        "_id": 1,
        "sport": "RUNNING",
        "fname": "test_session.json",
        "location": "Test Location",
        "distance": 10000,
        "duration": 3600,
        "startTime": datetime.now().isoformat(),
        "stopTime": (datetime.now() + timedelta(hours=1)).isoformat(),
        "latitude": 51.94737,
        "longitude": 4.3703,
        "speed": {
            "_id": 1,
            "avg": 12.1,
            "max": 20.0,
            "avg_corr": None,
        },
        "maximumHeartRate": 180,
        "averageHeartRate": 140,
        "heartRate": {"_id": 1, "min": 60, "avg": 140, "max": 180},
        "alaps": [],
        "laps": [],
        "trainingdescription": {
            "_id": 1,
            "description": "Test description",
            "type": "interval",
        },
        # "trainingtype": {},
        "trainingtype": {
            "_id": 1,
            "interval": "",
            "easyrun": None,
            "roadrace": None,  # Add roadrace field with appropriate value
            "sprint": None,  # Add sprint field with appropriate value
            "climax": None,  # Add climax field with appropriate value
        },
    }

    def _set_speed(self, resume):
        if "speed" in resume:
            self.polar_dummy_data["speed"].update(resume["speed"])
        # pol["speed"].update(resume["speed"])
        # return pol
        # resume["speed"]

    def _set_heartrate(self, resume):
        if "heartRate" in resume:
            self.polar_dummy_data["heartRate"].update(resume["heartRate"])

    def return_polardata(self, id_value, resume, field_names):
        # id_gen = self.id_generator()
        # id_value = next(id_gen)

        for key, value in resume.items():
            if key in field_names:
                # try:
                self.polar_dummy_data[key] = value
                # except TypeError:
                # self.polar_dummy_data = value

        self.polar_dummy_data["laps"] = resume["laps"]
        self.polar_dummy_data["alaps"] = resume["alaps"]
        self._set_speed(resume)
        self._set_heartrate(resume)

        self.polar_dummy_data["_id"] = id_value
        self.polar_dummy_data["speed"]["_id"] = id_value
        self.polar_dummy_data["heartRate"]["_id"] = id_value
        self.polar_dummy_data["trainingdescription"]["_id"] = id_value
        self.polar_dummy_data["trainingtype"]["_id"] = id_value
        # spmol = SpeedModel(**resume["speed"])
        # lmol = Laps(resume["laps"])

        # self.polar_dummy_data["laps"]["_id"] = id_value
        # self.polar_dummy_data["alaps"]["_id"] = id_value
        return self.polar_dummy_data


def id_generator():
    x = 1
    while True:
        yield x
        x += 1


@unittest.skip
class TestForm(TestCase):
    def setUp(self):
        # print(self.files[0])
        polgen = Polargenerator()

        igen = id_generator()
        polar_data = polgen.return_polardata(igen, dict(), dict())

        self.polar_model = PolarModel.objects.create(**polar_data)

    def test_valid_form(self):
        #  TrainingDescription({"description": "dummy",
        #             "type": "dummy",
        #         })
        # Create form data
        fname = r"C:\Users\marcr\OneDrive\Documenten\logboek_looptracks\polarroutes\training-session-2023-12-28-7788129097-dec336e5-f1c8-405d-872d-0c73bc6cffe4.json"
        form_data = {
            "fname": "testfile",
            "sport": "RUNNING",
            "trainingdescription": {
                "description": "dummy",
                "type": "dummy",
            },
            "trainingtype": {  # Pass a dictionary here
                "easyrun": True,
                "interval": "no interval",
                "roadrace": False,
                "sprint": False,
                "climax": False,
            },
            "location": "value1",
        }
        initdict, hackdict = self.polar_model._return_training_adaptdata(fname)
        form = adaptForm(data=form_data)
        form = form.set_form_initial(initdict, hackdict)
        print(form.errors)
        # Check if the form is valid
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Create form data with invalid values
        form_data = {
            "location": 1,
            # "field2": "value2",
            # Add more fields as necessary
        }
        form = adaptForm(data=form_data)

        # Check if the form is invalid
        self.assertFalse(form.is_valid())

    def test_form_submission(self):
        # Create form data
        form_data = {
            "location": "value1",
            # "field2": "value2",
            # Add more fields as necessary
        }
        form = adaptForm(data=form_data)

        # Check if the form is valid and can be saved
        self.assertTrue(form.is_valid())
        instance = form.save(commit=False)
        instance.save()

        # Perform any additional assertions as needed
        # For example, you might want to check if the instance is saved correctly
