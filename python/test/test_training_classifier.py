import unittest
from training_classifier import MongoRunningClassifier as mrc
import nosql_adapter as mongodb
import tomli

class TestRunningClassifier(unittest.TestCase):
    @classmethod
    def setUp(cls):
        config = tomli.load(open("config.toml","rb"))

        cls.testyear = "polartest"
        cls.dbase = "polartest4"
        cls.adapter = mongodb.MongoPolar(cls.dbase, cls.testyear)
        path = config["polar_json"]["datapath"]
        filename = "training-session-2014-03-14-263911238-d1eefba4-26b5-4a68-9ed6-8571939ade8a.json"
        cls.adapter.put_jsonresume(path, filename)
        cls.session = mrc(cls.dbase, cls.testyear)

    def test_class_init(self):
        session = mrc(self.dbase, 2014)
        self.assertEqual(self.session.SPORT, "RUNNING")
