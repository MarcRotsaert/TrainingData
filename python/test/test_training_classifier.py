import unittest
import tomli
from training_classifier import MongoRunningClassifier as mrc
from training_classifier import MongoIntervalTraining as mit
import nosql_adapter as mongodb


class TestRunningClassifierPolar(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.testyear = "polartest"
        cls.dbase = "unittest"
        cls.adapter = mongodb.MongoPolar(cls.dbase, cls.testyear)
        config = tomli.load(open("config.toml", "rb"))
        path = config["polar_json"]["datapath"]
        filename_easyrun = "training-session-2014-01-09-263914844-2b6b0088-52f9-4eb0-8434-f8837be097f4.json"
        cls.adapter.put_jsonresume(filename_easyrun)
        filename_interval = "training-session-2014-01-15-263914982-9576f971-b7fd-41f2-a257-436ffaa5aa3c.json"
        cls.adapter.put_jsonresume(filename_interval)
        filename_roadrace1 = "training-session-2014-05-14-263907872-a33e2e53-ef48-4763-9205-027a466396d9.json"
        cls.adapter.put_jsonresume(filename_roadrace1)
        filename_roadrace2 = "training-session-2014-06-29-263907128-d8753bea-9939-4993-8f88-e11ad7ff3202.json"
        cls.adapter.put_jsonresume(filename_roadrace2)
        filename_roadrace3 = "training-session-2014-07-05-263905442-d3ae528e-b7e2-4484-86ab-19ce51299025.json"

        cls.adapter.put_jsonresume(filename_roadrace3)
        cls.session = mrc(cls.dbase, cls.testyear)

    def test_return_easyrun(self):
        easyrun, non_easyrun = self.session.return_easyrun()

        self.assertIn(
            "training-session-2014-01-09-263914844-2b6b0088-52f9-4eb0-8434-f8837be097f4.json",
            easyrun,
        )
        self.assertIn(
            "training-session-2014-01-15-263914982-9576f971-b7fd-41f2-a257-436ffaa5aa3c.json",
            non_easyrun,
        )
        self.assertIn(
            "training-session-2014-05-14-263907872-a33e2e53-ef48-4763-9205-027a466396d9.json",
            non_easyrun,
        )
        self.assertIn(
            "training-session-2014-06-29-263907128-d8753bea-9939-4993-8f88-e11ad7ff3202.json",
            non_easyrun,
        )
        self.assertIn(
            "training-session-2014-07-05-263905442-d3ae528e-b7e2-4484-86ab-19ce51299025.json",
            non_easyrun,
        )

    def test_return_interval(self):
        trainingen = self.session.return_interval()

        self.assertIsInstance(trainingen, dict)
        self.assertEqual(
            trainingen[
                "training-session-2014-01-15-263914982-9576f971-b7fd-41f2-a257-436ffaa5aa3c.json"
            ],
            "interval",
        )

    def test_set_easyrun(self):
        self.session.set_easyrun()

        curs = self.adapter.simplequery("trainingtype.easyrun", True)
        res = list(curs)
        self.assertEqual(len(res), 1)

        self.assertEqual(
            res[0]["fname"],
            "training-session-2014-01-09-263914844-2b6b0088-52f9-4eb0-8434-f8837be097f4.json",
        )

    def test_set_interval(self):
        self.session.set_interval()

        curs = self.adapter.simplequery("trainingtype.interval", "interval")
        res = list(curs)
        self.assertEqual(len(res), 1)
        self.assertEqual(
            res[0]["fname"],
            "training-session-2014-01-15-263914982-9576f971-b7fd-41f2-a257-436ffaa5aa3c.json",
        )

    def test_return_roadrace(self):
        trainingen = self.session.return_roadrace()
        self.assertIsInstance(trainingen, set)
        self.assertIn(
            "training-session-2014-05-14-263907872-a33e2e53-ef48-4763-9205-027a466396d9.json",
            trainingen,
        )
        self.assertIn(
            "training-session-2014-06-29-263907128-d8753bea-9939-4993-8f88-e11ad7ff3202.json",
            trainingen,
        )
        self.assertIn(
            "training-session-2014-07-05-263905442-d3ae528e-b7e2-4484-86ab-19ce51299025.json",
            trainingen,
        )

        # ["marcrotsaert_175152248.fit"], "interval")

    def test_set_roadrace(self):
        self.session.set_roadrace()
        curs = self.adapter.simplequery("trainingtype.roadrace", True)
        res = list(curs)
        self.assertEqual(len(res), 3)
        fnames = [res[0]["fname"], res[1]["fname"], res[2]["fname"]]
        self.assertIn(
            "training-session-2014-05-14-263907872-a33e2e53-ef48-4763-9205-027a466396d9.json",
            fnames,
        )
        self.assertIn(
            "training-session-2014-06-29-263907128-d8753bea-9939-4993-8f88-e11ad7ff3202.json",
            fnames,
        )
        self.assertIn(
            "training-session-2014-07-05-263905442-d3ae528e-b7e2-4484-86ab-19ce51299025.json",
            fnames,
        )

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
        cls.adapter.put_jsonresume(filename_easyrun)
        filename_interval = "marcrotsaert_175152248.fit"
        cls.adapter.put_jsonresume(filename_interval)

        filename_roadrace1 = "marcrotsaert_164141202.fit"
        cls.adapter.put_jsonresume(filename_roadrace1)
        filename_roadrace2 = "marcrotsaert_252658603.fit"
        cls.adapter.put_jsonresume(filename_roadrace2)
        cls.session = mrc(cls.dbase, cls.testyear)

    def test_return_easyrun(self):
        easyrun, non_easyrun = self.session.return_easyrun()
        self.assertIn("marcrotsaert_162834949.fit", easyrun)
        self.assertIn("marcrotsaert_175152248.fit", non_easyrun)
        self.assertIn("marcrotsaert_164141202.fit", non_easyrun)
        self.assertIn("marcrotsaert_252658603.fit", non_easyrun)

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

    def test_return_roadrace(self):
        trainingen = self.session.return_roadrace()
        self.assertIsInstance(trainingen, set)
        self.assertIn("marcrotsaert_252658603.fit", trainingen)
        self.assertIn("marcrotsaert_164141202.fit", trainingen)

        # ["marcrotsaert_175152248.fit"], "interval")

    def test_set_roadrace(self):
        self.session.set_roadrace()
        curs = self.adapter.simplequery("trainingtype.roadrace", True)
        res = list(curs)
        self.assertEqual(len(res), 2)
        fnames = [res[0]["fname"], res[1]["fname"]]
        self.assertIn("marcrotsaert_252658603.fit", fnames)
        self.assertIn("marcrotsaert_164141202.fit", fnames)

    @classmethod
    def tearDown(cls):
        cls.adapter.deleteCollection()


class TestRunningClassifierInterval(unittest.TestCase):
    @classmethod
    def setUp(cls):
        config = tomli.load(open("config.toml", "rb"))
        cls.testyear = "polartest"
        cls.dbase = "unittest"

        cls.adapter = mongodb.MongoPolar(cls.dbase, cls.testyear)
        config = tomli.load(open("config.toml", "rb"))
        path = config["polar_json"]["datapath"]
        filename_easyrun = "training-session-2014-01-09-263914844-2b6b0088-52f9-4eb0-8434-f8837be097f4.json"
        cls.adapter.put_jsonresume(filename_easyrun)
        filename_interval = "training-session-2014-01-15-263914982-9576f971-b7fd-41f2-a257-436ffaa5aa3c.json"
        cls.adapter.put_jsonresume(filename_interval)
        cls.session = mrc(cls.dbase, cls.testyear)
        cls.session_i = mit(cls.dbase, cls.testyear)

    def test_set_intervaldescription(self):
        self.session.set_interval()
        self.session_i.set_intervaldescription()

        curs = self.adapter.simplequery(
            "trainingdescription.type",
            "interval",
        )
        res = list(curs)
        descrstring = res[0]["trainingdescription"]["description"]
        reslist = descrstring.replace(" ", "").strip(",").split(",")
        self.assertEqual(len(reslist), 27)
        self.assertEqual(reslist[1], "500m")
        self.assertEqual(reslist[-1], "P300m")

        # self.assertEqual(
        #     res[0]["fname"],
        #     "training-session-2014-01-15-263914982-9576f971-b7fd-41f2-a257-436ffaa5aa3c.json",
        # )
