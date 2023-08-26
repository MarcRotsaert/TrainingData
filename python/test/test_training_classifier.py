import unittest
from training_classifier import MongoRunningClassifier as mrc


class TestRunningClassifier(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.dbase = "polartest4"
        cls.collections = range(2011, 2013)
        # cls.adapter = mongodb.MongoAdapter(self.dbase, self.testyear)

    def test_class_init(self):
        for year in self.collections:
            session = mrc(self.dbase, year)
            self.assertEqual(session.sport, "RUNNING")
