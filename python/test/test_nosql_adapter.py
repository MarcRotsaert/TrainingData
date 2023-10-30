import unittest
from pymongo import MongoClient
import tomli
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
        self.assertEqual(len(docs), 298)


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
        self.assertTrue(80 < len(training) < 90)

    def test_morecomplexquery(self):
        cursor = self.adapter.morecomplexquery({"trainingtype": {"$exists": False}})
        training = [res for res in cursor]
        self.assertEqual(len(training), 35)

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
        self.assertTrue(125 < len(training) < 130)


class TestMongoPolar_adddata(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.dbase = "polartest4"
        cls.testyear = "polartest"
        cls.adapter = mongodb.MongoPolar(cls.dbase, cls.testyear)

    def test_addjson2db(self):
        config = tomli.load(open("config.toml", "rb"))
        path = config["polar_json"]["datapath"]
        filename = "training-session-2014-03-14-263911238-d1eefba4-26b5-4a68-9ed6-8571939ade8a.json"

        docs_voor = self.adapter.returnDocs()
        self.adapter.put_jsonresume(filename)

        docs_na = self.adapter.returnDocs()
        self.assertEqual(len(docs_na) - len(docs_voor), 1)

    @classmethod
    def tearDown(cls):
        cls.adapter.deleteCollection()


class TestMongoPolar_deletedata(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.dbase = "polartest4"
        cls.testyear = "polartest"
        cls.adapter = mongodb.MongoPolar(cls.dbase, cls.testyear)

    def test_delete_duplicates(self):
        config = tomli.load(open("config.toml", "rb"))
        path = config["polar_json"]["datapath"]
        filename = "training-session-2014-01-07-263914646-19f7d47a-6fd0-4a4b-bdf5-56df34741458.json"

        self.adapter.put_jsonresume(filename)
        self.adapter.put_jsonresume(filename)

        self.adapter.delete_duplicates()
        docs_na = self.adapter.returnDocs()

        self.assertEqual(len(docs_na), 1)

    @classmethod
    def tearDown(cls):
        cls.adapter.deleteCollection()


class TestMongoForerunner_adddata(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.dbase = "polartest4"
        cls.testyear = "polartest"
        cls.adapter = mongodb.MongoForerunner(cls.dbase, cls.testyear)

    def test_addjson2db(self):
        config = tomli.load(open("config.toml", "rb"))
        path = config["forerunner_xml"]["datapath"]
        filename = "20040922-132041.xml"

        docs_voor = self.adapter.returnDocs()
        self.adapter.put_jsonresume(filename)

        docs_na = self.adapter.returnDocs()
        self.assertEqual(len(docs_na) - len(docs_voor), 1)

    @classmethod
    def tearDown(cls):
        cls.adapter.deleteCollection()


class TestMongoForerunner_deletedata(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.dbase = "polartest4"
        cls.testyear = "polartest"
        cls.adapter = mongodb.MongoForerunner(cls.dbase, cls.testyear)

    def test_delete_duplicates(self):
        config = tomli.load(open("config.toml", "rb"))
        path = config["forerunner_xml"]["datapath"]
        filename = "20040922-132041.xml"

        self.adapter.put_jsonresume(filename)
        self.adapter.put_jsonresume(filename)

        self.adapter.delete_duplicates()
        docs_na = self.adapter.returnDocs()

        self.assertEqual(len(docs_na), 1)
