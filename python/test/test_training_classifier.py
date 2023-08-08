import unittest
from training_classifier import MongoRunningClassifier as mrc


class TestRunningClassifier(unittest.TestCase):
    def setUp(self):
        self.dbase = "polartest4"
        self.collections = range(2011, 2013)

    def test_class_init(self):
        for year in self.collections:
            self.assertIsEqual(session.sport, "RUNNING")
            session = mrc(self.dbase, year)
