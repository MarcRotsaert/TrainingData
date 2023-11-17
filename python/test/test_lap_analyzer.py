import unittest
import tomli
import numpy as np

import analyzer.polar_analyzer as pol_an
import analyzer.lap_analyzer as lap_an


class TestRMLapAnalyzer_timeint(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        config = tomli.load(open("config.toml", "rb"))
        cls.path = config["polar_json"]["datapath"]
        session = pol_an.Trainses_json(
            "training-session-2015-01-25-263888810-887b73d8-5599-4534-833c-521322b8c28b.json"
        )
        cls.laps = session.return_laps()
        cls.lap_an = lap_an.RManualLapAnalyzer(cls.laps)
        cls.paces = config["running"]["lap_paces"]

    def test_return_param(self):
        with self.subTest():
            distance = self.lap_an.return_distance()
            self.assertEqual(len(distance), 37)
        with self.subTest():
            duration = self.lap_an.return_duration()
            self.assertEqual(len(duration), 37)
        with self.subTest():
            speed = self.lap_an.return_paraslist("speed", "avg")
            self.assertEqual(len(speed), 37)

        with self.subTest():
            speed = self.lap_an.return_paraslist("speed", "avg", ind=[0, 1, 4, 7])
            self.assertListEqual(speed, [5.4, 15.8, 7.0, 16.2])

        with self.subTest():
            hr = self.lap_an.return_paraslist("heartRate", "avg")
            self.assertEqual(len(hr), 37)

        with self.subTest():
            asc = self.lap_an.return_paraslist("ascent", ind=[0, 1, 4, 20])
            self.assertListEqual(asc, [15, 5, 0, 0])
            self.assertEqual(len(asc), 4)

        with self.subTest():
            distance = self.lap_an.return_distance([2, 4, 6])
            self.assertEqual(len(distance), 3)

    def test_startuprunoutlaps(self):
        idx_su, idx_ru = self.lap_an.determine_startuprunoutlaps()
        self.assertEqual(idx_su, [0])
        self.assertEqual(idx_ru, [36])

    def test_speedupspeeddown(self):
        testresult = 18 * [-1.0, 1.0] + [-1.0]
        speedlist = self.lap_an.return_paraslist("speed", "avg")
        dspeed_int = self.paces["dspeedinterval"]
        speedup_speeddown = self.lap_an._classify_speedupdown(speedlist, dspeed_int)
        self.assertListEqual(testresult, speedup_speeddown.tolist())

    def test_convertdur2str(self):
        t_list = [
            [301, "5:01"],
            [60, "60s"],
            [90, "90s"],
            [32, "32s"],
        ]

        for t in t_list:
            t_str = self.lap_an._convertor_lapduration2str(t[0])
            self.assertEqual(t_str, t[1])

    def test_convertdist2str(self):
        d_list = [
            [20, "20m"],
            [340, "340m"],
            [2000, "2.0km"],
            [2500, "2.5km"],
        ]
        for d in d_list:
            d_str = self.lap_an._convertor_lapdistance2str(d[0])
            self.assertEqual(d_str, d[1])

    def test_check_allemptydata(self):
        # TODO: select appropriate data for this test
        self.assertFalse(self.lap_an._check_allempty_data("heartRate"))
        self.assertFalse(self.lap_an._check_allempty_data("speed"))

    def test_classify_timedistance(self):
        idx_int, idx_rec = self.lap_an.return_idx_intrec()

        distance_recovery = self.lap_an.return_distance(idx_rec)
        duration_recovery = self.lap_an.return_duration(idx_rec)

        result = self.lap_an._classify_timedistance(
            distance_recovery, duration_recovery
        )
        self.assertEqual(result[0], "time")

        distance_interval = self.lap_an.return_distance(idx_int)
        duration_interval = self.lap_an.return_duration(idx_int)

        result = self.lap_an._classify_timedistance(
            distance_interval, duration_interval
        )
        self.assertEqual(result[0], "time")

    def test_determine_corrspeed_int(self):
        res = self.lap_an.determine_corrspeed_int()
        self.assertEqual(res, None)


class TestRMLapAnalyzer_distint(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        config = tomli.load(open("config.toml", "rb"))
        cls.path = config["polar_json"]["datapath"]
        session = pol_an.Trainses_json(
            "training-session-2014-06-27-263907116-7cb098dc-3364-47b5-9d68-94ec381b08f7.json"
        )
        cls.laps = session.return_laps()
        cls.lap_an = lap_an.RManualLapAnalyzer(cls.laps)

    def test_determine_corrspeed_int(self):
        res = self.lap_an.determine_corrspeed_int()
        self.assertIsInstance(res, np.ndarray)
        self.assertListEqual(res.tolist(), [18.3, 18.1, 15.7])

    def test_determine_intervals(self):
        res = self.lap_an.determine_intervals()
        with self.subTest():
            self.assertEqual(res[0], "distance")
        with self.subTest():
            self.assertEqual(res[1], "time")
        with self.subTest():
            self.assertListEqual(res[2].tolist(), [1000, 1000, 1000])
        with self.subTest():
            self.assertListEqual(res[3].tolist(), [360, 330])
