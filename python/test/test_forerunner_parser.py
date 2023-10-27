import unittest
import time
import tomli

import forerunner_parser as for_par


class ForerunnerParser(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.startime = time.time()

    def test_lapparser_multilap(self):
        file = "20041227-191950.xml"
        laps = for_par.Lapparser(file).xml2laps()
        with self.subTest():
            self.assertEqual(len(laps), 13)
        
    def test_lapparser_singlelap(self):
        file = "20041222-171003.xml"
        laps = for_par.Lapparser(file).xml2laps()
        with self.subTest():
            self.assertEqual(len(laps), 1)

    def test_sampleparser(self):
        file = "20041227-191950.xml"
        samples = for_par.Sampleparser( file).xml2samples()
        with self.subTest():
            self.assertEqual(len(samples), 544)

    def test_xml2json_multiplelaps(self):
        file = "20041227-191950.xml"
        json = for_par.Parser(file).xml2json()
        with self.subTest():
            self.assertIn("exercises", json)
        with self.subTest():
            self.assertEqual(len(json["exercises"]),1)
        with self.subTest():
            self.assertTrue('laps' in json["exercises"][0])
        with self.subTest():
            self.assertTrue('samples' in json["exercises"][0])
        with self.subTest():
            self.assertTrue('recordedRoute' in json["exercises"][0]['samples'])
     
    def test_xml2json_singlelaps(self):
        file = "20041222-171003.xml"
        json = for_par.Parser(file).xml2json()
        with self.subTest():
            self.assertIn("exercises", json)
        with self.subTest():
            self.assertEqual(len(json["exercises"]),1)
        with self.subTest():
            self.assertTrue('laps' not in json["exercises"][0])
        with self.subTest():
            self.assertTrue('samples' in json["exercises"][0])
        with self.subTest():
            self.assertTrue('recordedRoute' in json["exercises"][0]['samples'])