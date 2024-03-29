import unittest
import time
import analyzer.forerunner_analyzer as for_an

class ForerunnerAnalyzer(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.startime = time.time()

    def test_read_data_multilap(self):
        file = "20050725-190632.xml"
        session = for_an.Trainses_xml(file)
        with self.subTest():
            self.assertEqual(len(session.laps), 11)
        with self.subTest():
            self.assertIn("fname", session.abstract)

    def test_read_data_onelap(self):
        file = "20041008-170457.xml"
        session = for_an.Trainses_xml(file)
        with self.subTest():
            self.assertIsNone(session.laps)
        with self.subTest():
            self.assertEqual(session.abstract["distance"], 5724.523)
        with self.subTest():
            self.assertIn("fname", session.abstract)
        print(time.time() - self.startime)
