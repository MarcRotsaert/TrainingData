# import settings

# print(settings)
from django.conf import settings
from django.test import TestCase

from .models import PolarModel

# from python.nosql_adapter import MongoPolar, MongoForerunner
# from parsing.polar_parser import Parser
# from analyzer import polar_analyzer as pol_an

# Create your tests here.
print(settings.DATABASES)


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
        field_names = [field.name for field in fields]

        for i, fi in enumerate(self.files):
            filename = fi.split("\\")[-1]
            sess = pol_an.Trainses_json(filename)
            resume = sess.abstract
            resume.update({"laps": sess.laps, "alaps": sess.alaps})
            valid_resume_keys = {
                key: value for key, value in resume.items() if key in field_names
            }
            PolarModel.objects.create(**valid_resume_keys)
        print(valid_resume_keys)
        print(field_names)

    def test_one(self):
        self.assertEqual(PolarModel.objects.count(), 24)
