from typing import Union, List
from datetime import timedelta
import numpy as np

import tomli


class LapAnalyzer:
    def __init__(self, laps: list, params: list):
        self.laps_an = self._reshapelaps(laps, params)

    def _reshapelaps(self, laps: list, params: list) -> dict:
        result = {}
        for par in params:
            try:
                temp = {par: [la[par] for la in laps]}
            except KeyError:
                temp = {par: None}
            except TypeError:
                continue
            result.update(temp)
        return result

    def _check_allempty_data(self, param: str):
        empty = []
        for i, data in enumerate(self.laps_an[param]):
            if len(data) == 0:
                empty.append(i)
        if len(empty) == len(self.laps_an[param]):
            return True
        else:
            return False

    def return_distance(self, lapidx: list[int] = []) -> list[float]:
        distance = []
        if len(lapidx) == 0:
            distance = self.laps_an["distance"]
        else:
            for i in lapidx:
                distance.append(self.laps_an["distance"][i])
        return distance

    def return_duration(self, lapidx: list = []) -> list[float]:
        duration = []
        if len(lapidx) == 0:
            duration = self.laps_an["duration"]
        else:
            for i in lapidx:
                duration.append(self.laps_an["duration"][i])
        return duration

    def return_paraslist(self, par: str, *arg: str) -> list[float]:
        temp = self.laps_an[par]
        values = []
        if len(arg) == 0:
            values = temp
        else:
            for la in temp:
                try:
                    values.append(la[arg[0]])
                except KeyError:
                    values.append(-999)

        return values

    def print_nrlaps(self) -> None:
        print(len(self.laps_an["speed"]))

    def compare_hr_sp(self) -> Union[None, np.ndarray[float, float]]:
        if self.laps_an["heartRate"] is None or self.laps_an["speed"] is None:
            print("no heartrate or speed")
            return None
        else:
            avgheartr = self.return_paraslist("heartRate", "avg")
            avgspeed = self.return_paraslist("speed", "avg")
            return np.corrcoef(avgspeed, avgheartr)[0, 1]

    def determine_speedvariability(
        self, ignorelaps: list[int] = []
    ) -> (float, float, float):
        speed = np.array(self.return_paraslist("speed", "avg"))
        speed = np.delete(speed, ignorelaps)
        stdspeed = np.std(speed)
        maxspeed = np.max(speed)
        minspeed = np.max(speed)
        return stdspeed, maxspeed, minspeed

    def _determine_accelaration(self, ignorelaps: list[int] = []) -> np.array:
        speed = np.array(self.return_paraslist("speed", "avg"))
        speed = np.delete(speed, ignorelaps)
        dspeed = speed[1:] - speed[0:-1]
        return dspeed

    def determine_heartratevariability(
        self, ignorelaps: list[int] = []
    ) -> (float, float, float):
        hrt = np.array(self.return_paraslist("heartRate"))
        hrt = np.delete(hrt, ignorelaps)
        stdhrt = np.std(hrt)
        maxhrt = np.max(hrt)
        minhrt = np.max(hrt)
        return stdhrt, maxhrt, minhrt


class RLapAnalyzerBasic(LapAnalyzer):
    """
    basic class for analyzing manual/automatic laps
    """

    def __init__(self, laps: dict):
        config = tomli.load(open("config.toml", "rb"))
        self.param = config["running"]["lap_param"]
        self.paces = config["running"]["lap_paces"]
        super().__init__(laps, self.param)

    def identify_roadrace(
        self, ignorelaps: list = [], min_speed: float or None = None
    ) -> bool:
        if min_speed is None:
            min_speed = self.paces["minroadrace"]

        speedarr = np.array(self.return_paraslist("speed", "avg"))
        speedarr = np.delete(speedarr, ignorelaps)
        if len(speedarr) == 0:
            result = False
        else:
            result = all(speedarr > min_speed)
        return result

    def identify_easyrun(self, max_speed: float or None = None) -> bool:
        if self._check_allempty_data("speed"):
            return False

        if max_speed is None:
            max_speed = self.paces["maxeasy"]

        speed = []
        for sp in self.laps_an["speed"]:
            if len(sp) != 0:
                speed.append(sp["avg"])
        speed = np.array(speed)

        result = all(speed <= max_speed)

        return result


class RAutoLapAnalyzer(RLapAnalyzerBasic):
    def __init__(self, alaps: dict):
        # TODO: check on Alaps
        super().__init__(alaps)


class RManualLapAnalyzer(RLapAnalyzerBasic):
    def __init__(self, laps: dict):
        # TODO: check on laps
        super().__init__(laps)

    def determine_startuprunoutlaps(
        self, su_speed=None
    ) -> (Union[List[int], None], Union[List[int], None]):
        nodata = self._check_allempty_data("speed")
        if nodata:
            return None, None
        if su_speed is None:
            su_speed = self.paces["maxruninout"]
        idx_su = []
        i1 = 0

        # code hieronder kan niet omgaan met een lege dictionaryin laps["speed"]
        for speed in self.laps_an["speed"]:
            if len(speed) == 0:
                idx_su.append(i1)
                i1 += 1
            else:
                if speed["avg"] > su_speed:
                    break
                else:
                    idx_su.append(i1)
                    i1 += 1
        if len(idx_su) == 0:
            idx_su = []

        idx_ro = []
        i2 = len(self.laps_an["speed"]) - 1
        while self.laps_an["speed"][i2]["avg"] < su_speed and i2 > i1:
            idx_ro.append(i2)
            i2 -= 1
        if len(idx_ro) == len(self.laps_an["speed"]) + 1:
            idx_ro = []
        elif len(idx_ro) == 0:
            idx_ro = []
        return idx_su, idx_ro

    def determine_lapswithoutsu(self) -> Union[dict, None]:
        su, ro = self.determine_startuprunoutlaps()
        if su == (None, None):
            return None

        removerounds = []
        if su != [-1]:
            removerounds.extend(su)
        if ro != [99999]:
            removerounds.extend(ro)
        removerounds.sort()
        removerounds.reverse()

        laps = self.laps_an.copy()
        for k in laps:
            for i_la in removerounds:
                if laps[k] is None:
                    break
                laps[k].pop(i_la)
        return laps

    @staticmethod
    def _rounded_distance(distance: float, rounding_distance: int = 100) -> int:
        return rounding_distance * round(distance / rounding_distance)

    @staticmethod
    def _rounded_duration(duration: float, rounding_time: int = 30) -> int:
        if isinstance(duration, str):
            duration = float(duration.lstrip("PT").rstrip("S"))
        return rounding_time * round(duration / rounding_time)

    def _classify_timedistance(self, duration: list, distance: list) -> str:
        """determine if lapinterval is based upon distance or time"""
        rounded_distance = []
        rounded_duration = []
        for dur in duration:
            rounded_duration.append(self._rounded_duration(dur))
        for dis in distance:
            rounded_distance.append(self._rounded_distance(dis))
        rounded_distance = np.array(rounded_distance)
        rounded_duration = np.array(rounded_duration)

        dif_dis = np.abs(distance - rounded_distance)
        dif_dur = np.abs(duration - rounded_duration)

        if dif_dur.mean() < 4:
            classification = ["time", rounded_duration]
        elif dif_dis.std() < 15 and dif_dur.mean() >= 4:
            classification = ["distance", rounded_distance]
        else:
            classification = ["undetermined", None]

        return classification

    @staticmethod
    def _return_lap_length(distance, duration, clas_timedis):
        if clas_timedis == "time":
            return duration
        elif clas_timedis == "distance":
            return distance
        elif clas_timedis == "undetermined":
            return None

    def determine_intervals(self):
        """determine lapinterval size in distance or time"""
        idx_su, idx_ru = self.determine_startuprunoutlaps()

        classif = self._classifylap_speedupspeeddown(self.laps_an)
        for i in idx_su + idx_ru:
            classif[i] = 0

        idx = np.where(classif == 1)[0]
        distance_interval = self.return_distance(idx)
        duration_interval = self.return_duration(idx)

        idx = np.where(classif == -1)[0]
        distance_recovery = self.return_distance(idx)
        duration_recovery = self.return_duration(idx)

        regis_interval = self._classify_timedistance(
            duration_interval, distance_interval
        )
        regis_recovery = self._classify_timedistance(
            duration_recovery, distance_recovery
        )
        if regis_recovery[0] != "undetermined" and regis_interval[0] != "undetermined":
            trainingstr = self.convertor_length2str(regis_interval, regis_recovery)
        else:
            trainingstr = "undetermined"

        return trainingstr

    def convertor_length2str(self, regis_interval, regis_recovery):
        # conversion2str
        interval_strtype = regis_interval[0]
        intervals = regis_interval[1]
        recovery_strtype = regis_recovery[0]
        recoveries = regis_recovery[1]

        trainingstr = ""
        for i in range(len(recoveries)):
            if interval_strtype == "time":
                trainingstr += self._convertor_lapduration2str(intervals[i]) + ","
            elif interval_strtype == "distance":
                trainingstr += self._convertor_lapdistance2str(intervals[i]) + ","

            trainingstr += "P"
            if recovery_strtype == "time":
                trainingstr += self._convertor_lapduration2str(recoveries[i]) + ","
            elif recovery_strtype == "distance":
                trainingstr += self._convertor_lapdistance2str(recoveries[i]) + ","

        if interval_strtype == "time":
            trainingstr += self._convertor_lapduration2str(intervals[i]) + ","
        elif interval_strtype == "distance":
            trainingstr += self._convertor_lapdistance2str(intervals[i]) + ","

        return trainingstr

    @staticmethod
    def _convertor_lapduration2str(duration: int) -> str:
        td = timedelta(0, int(duration), 0)
        minutes, seconds = divmod(td.seconds, 60)
        if minutes <= 1:
            duration_str = str(duration) + "s"
        else:
            duration_str = str(minutes) + ":" + "{:>02}".format(seconds)
        return duration_str

    @staticmethod
    def _convertor_lapdistance2str(distance: int) -> str:
        if distance >= 1000:
            distance_str = str(round(distance / 1000, 1)) + "km"
        else:
            distance_str = str(distance) + "m"
        return distance_str

    def _classifylap_speedupspeeddown(self, laps):
        """
        element in de
        -1 = recovery
        1 = interval

        """
        dspeed_int = self.paces["dspeedinterval"]
        speed = np.array([sp["avg"] for sp in laps["speed"]])
        dspeed = speed[1:] - speed[0:-1]
        dspeed[(dspeed < dspeed_int) & (dspeed > -dspeed_int)] = 0
        dspeed[dspeed > dspeed_int] = 1
        dspeed[dspeed < -dspeed_int] = -1

        if dspeed[0] == 1:
            result = np.hstack([-1, dspeed])
        elif dspeed[0] == -1:
            result = np.hstack([1, dspeed])
        else:
            result = np.hstack([0, dspeed])

        return result

    def identify_interval(self) -> str:
        if self._check_allempty_data("speed"):
            return "undetermined"

        laps = self.determine_lapswithoutsu()

        if laps is None:
            return "undetermined"

        speed = np.array([sp["avg"] for sp in laps["speed"]])
        sprint = self.identify_sprints()
        easyrun = self.identify_easyrun()

        if speed.shape[0] < 5:
            # Not enough laps
            return "no interval, crit. 1"
        elif sprint or easyrun:
            # Training is sprint or easy_run
            return "no interval, crit. 2"

        recovspeed = self._classifylap_speedupspeeddown(laps)

        if np.count_nonzero(recovspeed == 0) / len(recovspeed) > 0.25:
            return "no interval, crit. 3, under investigation."

        deriv = recovspeed[1:] + recovspeed[0:-1]
        if sum(deriv) == 0:
            return "interval"

        if (
            len(speed) > 8
            and len(recovspeed[recovspeed == -1]) / len(recovspeed) > 1 / 3
        ):
            # Almost certain
            return "interval, check1"

        if len(speed) == 5 and len(recovspeed[recovspeed == -1]) == 2:
            return "interval, check2"
        else:
            return "no interval, crit. 4, under investigation"

    def identify_sprints(self, max_time: float = 20.0) -> bool:
        sprints = []
        for lnr in range(len(self.laps_an["duration"])):
            lapdur = self.laps_an["duration"][lnr]
            if isinstance(lapdur, str):
                lapdur = float(lapdur.lstrip("PT").rstrip("S"))
            if lapdur < max_time:
                sprints.append(lnr)
        result = len(sprints) > 3
        return result
