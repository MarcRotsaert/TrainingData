import unittest
import time
import tomli

import garmin_analyzer as gar_an

class GarminAnalyzer(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.startime = time.time()
        config = tomli.load(open("config.toml", "rb"))
        cls.path = config["forerunner_xml"]["datapath"]

    def test_read_data_general(self):
        file = "marcrotsaert_217112806.fit"
        session = gar_an.Trainses_fit(self.path, file)
        with self.subTest():
            self.assertTrue(hasattr(session, 'abstract'))
            self.assertTrue(hasattr(session, 'laps'))
            self.assertTrue(hasattr(session, 'alaps'))
            self.assertTrue(hasattr(session, 'samples'))
        with self.subTest():
            self.assertIn("fname", session.abstract)

    def test_read_data_manuallap(self):
        file = "marcrotsaert_217112806.fit"
        session = gar_an.Trainses_fit(self.path, file)
        with self.subTest():
            self.assertTrue(hasattr(session, 'abstract'))
            self.assertTrue(hasattr(session, 'laps'))
            self.assertTrue(hasattr(session, 'alaps'))
            self.assertTrue(hasattr(session, 'samples'))
        with self.subTest():
            self.assertEqual(len(session.laps), 19)

    def test_read_data_autolap(self):
        file = "marcrotsaert_651691100.fit"
        session = gar_an.Trainses_fit(self.path, file)
        with self.subTest():
            self.assertEqual(len(session.alaps), 8)
        with self.subTest():
            self.assertIn('heartRate', session.alaps[0])
            self.assertIn('speed', session.alaps[0])
            self.assertIn('duration', session.alaps[0])
            self.assertIn('distance', session.alaps[0])
            self.assertIn('avg', session.alaps[0]['speed'])

    def test_read_data_samples(self):
        file = "marcrotsaert_651691100.fit"
        session = gar_an.Trainses_fit(self.path, file)
        with self.subTest():
            self.assertIn( 'recordedRoute', session.samples)
        with self.subTest():
            self.assertEqual(len(session.samples['recordedRoute']), 568)
        with self.subTest():
            self.assertIn('heartRate', session.samples)
            self.assertIn('speed', session.samples)
            self.assertIn('latitude', session.samples['recordedRoute'][0])
            self.assertIn('longitude', session.samples['recordedRoute'][0])
            self.assertIn('dateTime', session.samples['recordedRoute'][0])
