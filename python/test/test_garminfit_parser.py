import unittest
import time
import tomli

import parsing.garminfit_parser as gar_par


class GarminfitParser(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.startime = time.time()

    def test_lapparser_example1(self):
        file = "marcrotsaert_158946109.fit"
        alaps = gar_par.Lapparser(file).fit2laps("alaps")
        laps = gar_par.Lapparser(file).fit2laps("laps")
        with self.subTest():
            self.assertEqual(len(alaps), 2)
        with self.subTest():
            self.assertEqual(len(laps), 0)

    def test_lapparser_example2(self):
        file = "marcrotsaert_401780441.fit"
        alaps = gar_par.Lapparser(file).fit2laps("alaps")
        laps = gar_par.Lapparser(file).fit2laps("laps")
        with self.subTest():
            self.assertEqual(len(alaps), 18)
        with self.subTest():
            self.assertEqual(alaps[0]["distance"], 5000)
            self.assertEqual(alaps[-1]["distance"], 1857.0)
        with self.subTest():
            self.assertEqual(len(laps), 1)

    def test_sampleparser(self):
        file = "marcrotsaert_158946109.fit"
        samples = gar_par.Sampleparser(file).fit2samples()
        with self.subTest():
            self.assertEqual(len(samples), 4)
        with self.subTest():
            for par in samples:
                self.assertEqual(len(samples[par]), 360)

    def test_fit2json_example1(self):
        file = file = "marcrotsaert_401780441.fit"
        json = gar_par.Parser(file).fit2json()
        with self.subTest():
            self.assertNotIn("laps", json)
        with self.subTest():
            self.assertIn("alaps", json)
        with self.subTest():
            self.assertIn("exercises", json)
        with self.subTest():
            self.assertEqual(len(json["exercises"]), 1)
        with self.subTest():
            self.assertTrue("samples" in json["exercises"][0])
        with self.subTest():
            self.assertTrue("recordedRoute" in json["exercises"][0]["samples"])

    def test_fit2json_example1(self):
        file = file = "marcrotsaert_158946109.fit"
        json = gar_par.Parser(file).fit2json()
        with self.subTest():
            self.assertIn("laps", json["exercises"][0])
        with self.subTest():
            self.assertIn("alaps", json["exercises"][0])
        with self.subTest():
            self.assertIn("laps", json["exercises"][0])
        with self.subTest():
            self.assertEqual(len(json["exercises"][0]["laps"]), 0)
        with self.subTest():
            self.assertIn("exercises", json)
        with self.subTest():
            self.assertEqual(len(json["exercises"]), 1)
        with self.subTest():
            self.assertTrue("samples" in json["exercises"][0])
        with self.subTest():
            self.assertTrue("recordedRoute" in json["exercises"][0]["samples"])

    def test_fit2json_example2(self):
        file = file = "marcrotsaert_401780441.fit"
        json = gar_par.Parser(file).fit2json()
        with self.subTest():
            self.assertIn("laps", json["exercises"][0])
        with self.subTest():
            self.assertIn("alaps", json["exercises"][0])
        with self.subTest():
            self.assertEqual(len(json["exercises"][0]["laps"]), 1)
        with self.subTest():
            self.assertIn("exercises", json)
        with self.subTest():
            self.assertEqual(len(json["exercises"]), 1)
        with self.subTest():
            self.assertTrue("samples" in json["exercises"][0])
        with self.subTest():
            self.assertTrue("recordedRoute" in json["exercises"][0]["samples"])

    def test_abstract_parsing(self):
        file = "marcrotsaert_158946109.fit"
        abstract = gar_par.Parser(file).extract_abstract()
        self.assertEqual(abstract["sport"], "CYCLING")
        self.assertEqual(abstract["maximumHeartRate"], 150)
