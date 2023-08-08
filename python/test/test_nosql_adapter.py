import unittest
import nosql_adapter as mongodb


class TestMongoAdapter(unittest.TestCase):
    def setUp(self):
        self.dbase = "polartest4"
        self.collections = range(2012, 2021)
        self.testyear = "2014"

    def test_connection(self):
        adapter = mongodb.MongoAdapter(self.dbase, self.testyear)
        self.assertEqual(adapter.client(), 0)

    def test_returndocs(self):
        adapter = mongodb.MongoAdapter(self.dbase, self.testyear)
        cursor = adapter.returnDocs()
        self.assertEqual(docs, 10)


class TestMongoQuery(unittest.TestCase):
    def setUp(self):
        self.dbase = "polartest4"
        self.collections = range(2012, 2021)
        self.testyear = "2014"
