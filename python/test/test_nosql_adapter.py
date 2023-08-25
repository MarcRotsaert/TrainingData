import unittest
from pymongo import MongoClient
import nosql_adapter as mongodb


class TestMongoAdapter(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.dbase = "polartest4"
        cls.collections = range(2012, 2021)
        cls.testyear = "polar2014"
        cls.adapter = mongodb.MongoAdapter(cls.dbase, cls.testyear)

    def test_connection(self):
        self.assertIsInstance(self.adapter.client, MongoClient)

    def test_returndocs(self):
        docs = self.adapter.returnDocs()
        self.assertEqual(len(docs), 596)


class TestMongoQuery(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.dbase = "polartest4"
        cls.collections = range(2012, 2021)
        cls.testyear = "polar2014"
        cls.adapter = mongodb.MongoQuery(cls.dbase, cls.testyear)

    # @unittest.skip("first fill database with training info.")
    def test_simplequery(self):
        cursor = self.adapter.simplequery("trainingtype.easyrun", True)
        training = [res for res in cursor]
        self.assertEqual(len(training), 178)

    def test_morecomplexquery(self):
        cursor = self.adapter.morecomplexquery({"trainingtype": {"$exists": False}})
        training = [res for res in cursor]
        self.assertEqual(len(training), 182)

    def test_morecomplexquery2(self):
        cursor = self.adapter.morecomplexquery(
            {
                "$and": [
                    {"trainingtype": {"$exists": True}},
                    {"trainingtype.interval": {"$ne": "interval"}},
                    {"trainingtype.interval": {"$ne": "interval, check"}},
                    {"trainingtype.interval": {"$ne": "interval, check2"}},
                    {"trainingtype.easyrun": {"$ne": True}},
                    {"trainingtype.sprint": {"$ne": True}},
                ]
            }
        )
        training = [res for res in cursor]
        self.assertEqual(len(training), 154)
