import unittest
import polar_analyzer as pol_an
import nosql_adapter as mongodb
import tomli
import time


class PolarAnalyzerJson(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.startime = time.time()
        config = tomli.load(open("config.toml", "rb"))
        cls.path = config["polar_json"]["datapath"]

    def test_read_data1(self):
        file = "training-session-2019-07-04-3666956261-8c8d9764-332d-42d1-bed3-f502dbc4c273.json"
        session = pol_an.Trainses_json(self.path, file)
        with self.subTest():
            self.assertEqual(len(session.alaps), 7)
        with self.subTest():
            self.assertIsNone(session.laps)
        with self.subTest():
            self.assertIn("fname", session.abstract)

    def test_read_data2(self):
        file = "training-session-2017-09-21-1766006650-5ffee761-22e6-4c0b-9590-ae130c929649.json"
        session = pol_an.Trainses_json(self.path, file)
        with self.subTest():
            self.assertEqual(len(session.alaps), 15)
        with self.subTest():
            self.assertEqual(len(session.laps), 17)
        with self.subTest():
            self.assertIn("fname", session.abstract)
        print(time.time() - self.startime)


class PolarAnalyzerMongo(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.startime = time.time()
        cls.dbase = "polartest4"
        cls.testyear = "polar2017"
        cls.adapter = mongodb.MongoPolar(cls.dbase, cls.testyear)
        cursor = cls.adapter.simplequery(
            "fname",
            "training-session-2017-09-21-1766006650-5ffee761-22e6-4c0b-9590-ae130c929649.json",
        )
        cls.record = cursor.next()

    def test_read_data1(self):
        session = pol_an.Trainses_mongo(self.record)
        with self.subTest():
            self.assertEqual(len(session.alaps), 15)
        with self.subTest():
            self.assertEqual(len(session.laps), 17)
        with self.subTest():
            self.assertIn("fname", session.abstract)
        print(time.time() - self.startime)
