import unittest
from pymongo import MongoClient
import nosql_adapter as mongodb


class TestMongoAdapter(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.dbase = "polartest4"
        self.collections = range(2012, 2021)
        self.testyear = "polar2014"
        self.adapter = mongodb.MongoAdapter(self.dbase, self.testyear)

    def test_connection(self):
        self.assertIsInstance(adapter.client, MongoClient)

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

    @unittest.skip("first database adaptation.")
    def test_simplequery(self):
        cursor = self.adapter.simplequery("trainingtype.easyrun", True)
        training = [res for res in cursor]
        self.assertEqual(len(training), 100)

    def test_morecomplexquery(self):
        cursor = self.adapter.morecomplexquery({"trainingtype": {"$exists": False}})
        training = [res for res in cursor]
        self.assertEqual(len(training), 596)

        # for res in result:
        #     session = pj.Trainses_mongo(res)
        #     # print(res)
        #     if "trainingtype" in session.abstract:
        #         print(session.abstract["trainingtype"])
        #     else:
        #         print("no type")
        #     # continue
        #     laps = session.return_laps()
        #     if laps != None:
        #         lapses = pj.RManualLapAnalyzer(laps)
        #         su = lapses.return_startuprunoutlaps()
        #         result = lapses.return_accelartion(ignorelaps=su[0] + su[1])
        #         print(result)
        #         print(sum(result))
        #         fname = session.abstract["fname"]
        #         ses = pj.Trainses(path, fname)
        #         samses = pj.SamAnalExtra(ses.samples)
        #         samses.plot("speed")
        #         time.sleep(1)
