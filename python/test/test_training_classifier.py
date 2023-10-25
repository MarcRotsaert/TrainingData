import unittest
import tomli
from training_classifier import MongoRunningClassifier as mrc
import nosql_adapter as mongodb


class TestRunningClassifierPolar(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.testyear = "polartest"
        cls.dbase = "unittest"
        cls.adapter = mongodb.MongoPolar(cls.dbase, cls.testyear)
        # config = tomli.load(open("config.toml", "rb"))
        # path = config["polar_json"]["datapath"]
        # filename_easyrun = ""
        # cls.adapter.put_jsonresume(path, filename_easyrun)
        # filename_interval = ""
        # cls.adapter.put_jsonresume(path, filename_interval)
        # cls.session = mrc(cls.dbase, cls.testyear)

    @unittest.skip("file not selected ")
    def test_return_easyrun(self):
        pass

    @unittest.skip("file not selected ")
    def test_return_interval(self):
        pass

    @unittest.skip("file not selected ")
    def test_set_easyrun(self):
        pass

    @unittest.skip("file not selected ")
    def test_set_interval(self):
        pass

    @classmethod
    def tearDown(cls):
        cls.adapter.deleteCollection()


class TestRunningClassifierGarmin(unittest.TestCase):
    @classmethod
    def setUp(cls):
        config = tomli.load(open("config.toml", "rb"))

        cls.testyear = "garmintest"
        cls.dbase = "unittest"
        cls.adapter = mongodb.MongoGarminfit(cls.dbase, cls.testyear)
        path = config["garmin_fit"]["datapath"]
        filename_easyrun = "marcrotsaert_162834949.fit"
        cls.adapter.put_jsonresume(path, filename_easyrun)
        filename_interval = "marcrotsaert_175152248.fit"
        cls.adapter.put_jsonresume(path, filename_interval)
        cls.session = mrc(cls.dbase, cls.testyear)

    def test_return_easyrun(self):
        easyrun, non_easyrun = self.session.return_easyrun()
        self.assertEqual(easyrun, ["marcrotsaert_162834949.fit"])
        self.assertEqual(non_easyrun, ["marcrotsaert_175152248.fit"])

    def test_return_interval(self):
        trainingen = self.session.return_interval()
        self.assertIsInstance(trainingen, dict)
        self.assertEqual(trainingen["marcrotsaert_175152248.fit"], "interval")

    def test_set_easyrun(self):
        self.session.set_easyrun()
        curs = self.adapter.simplequery("trainingtype.easyrun", True)
        res = list(curs)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["fname"], "marcrotsaert_162834949.fit")

    def test_set_interval(self):
        self.session.set_interval()
        curs = self.adapter.simplequery("trainingtype.interval", "interval")
        res = list(curs)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["fname"], "marcrotsaert_175152248.fit")

    @classmethod
    def tearDown(cls):
        cls.adapter.deleteCollection()
