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
            self.assertEqual(len(laps), 12)
        
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
