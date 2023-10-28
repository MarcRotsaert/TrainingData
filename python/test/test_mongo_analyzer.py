import time
import unittest

import nosql_adapter as mongodb
from trainsession import Trainsession_mongo


class MongoAnalyzer(unittest.TestCase):
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

    # @unittest.skip("not yet implemented")
    def test_read_data1(self):
        session = Trainsession_mongo(self.record)
        with self.subTest():
            self.assertEqual(len(session.alaps), 15)
        with self.subTest():
            self.assertEqual(len(session.laps), 17)
        with self.subTest():
            self.assertIn("fname", session.abstract)
        print(time.time() - self.startime)
