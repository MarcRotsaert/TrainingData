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

    def _classifylap_speedupspeeddown(self, speedlist: list) -> np.array:
        """
        element in de
        -1 = recovery
        1 = interval

        """
        dspeed_int = self.paces["dspeedinterval"]

        speed = np.array(speedlist)
        dspeed = speed[1:] - speed[0:-1]

        dspeed[(dspeed < dspeed_int) & (dspeed > -dspeed_int)] = 0
        dspeed[dspeed >= dspeed_int] = 1
        dspeed[dspeed < -dspeed_int] = -1

        if dspeed[0] == 1:
            result = np.hstack([-1, dspeed])
        elif dspeed[0] == -1:
            result = np.hstack([1, dspeed])
        else:
            result = np.hstack([0, dspeed])

        return result

    @staticmethod
    def _difference2rounded(
        values: list, rounding_value: float
    ) -> [np.array, np.array]:
        """determine difference between recorded and rounded lap values"""
        rounded_values = []
        for val in values:
            rounded_val = rounding_value * round(val / rounding_value)
            rounded_values.append(rounded_val)
        rounded_values = np.array(rounded_values)
        dif = np.abs(values - rounded_values)
        return dif, rounded_values

    def _classify_timedistance(
        self, distance: list, duration: list
    ) -> list[str, Union[float, None]]:
        """determine if lapinterval is based upon distance or time"""
        # criteria for classification
        dif_dur_mean = 4  # sec
        dif_dis_std = 15  # m

        rounding_time = 30  # sec
        rounding_distance = 100  # m

        dif_dis, rounded_distance = self._difference2rounded(
            distance, rounding_distance
        )
        dif_dur, rounded_duration = self._difference2rounded(duration, rounding_time)

        if dif_dur.mean() < dif_dur_mean:
            classification = ["time", rounded_duration]
        elif dif_dis.std() < dif_dis_std and dif_dur.mean() >= dif_dur_mean:
            classification = ["distance", rounded_distance]
        else:
            classification = ["undetermined", None]

        return classification

    def _group_intervalorrecovery(
        self, classif, intervalrecovery
    ) -> [np.array, np.array]:
        if intervalrecovery == "interval":
            cl_index = 1
        elif intervalrecovery == "recovery":
            cl_index = -1
        idx = np.where(classif == cl_index)[0]
        duration_values = self.return_duration(idx)

        idx = np.where(classif == cl_index)[0]
        distance_values = self.return_distance(idx)
        return distance_values, duration_values

    def determine_intervals(self) -> str:
        """determine lapinterval size in distance or time"""
        idx_su, idx_ru = self.determine_startuprunoutlaps()

        speedlist = self.return_paraslist("speed", "avg")
        classif = self._classifylap_speedupspeeddown(speedlist)
        for i in idx_su + idx_ru:
            classif[i] = 0

        distance_interval, duration_interval = self._group_intervalorrecovery(
            classif, "interval"
        )
        distance_recovery, duration_recovery = self._group_intervalorrecovery(
            classif, "recovery"
        )

        regis_interval = self._classify_timedistance(
            distance_interval, duration_interval
        )
        regis_recovery = self._classify_timedistance(
            distance_recovery, duration_recovery
        )

        if regis_recovery[0] != "undetermined" and regis_interval[0] != "undetermined":
            if len(regis_interval[1]) - len(regis_recovery[1]) == 1:
                regis_laps = self._prepare_convertorl2str(
                    regis_interval, regis_recovery
                )
                trainingstr = self.convertor_length2str(regis_laps)
            else:
                trainingstr = "error: nr. interval laps equals nr recovery laps"

        else:
            trainingstr = "undetermined"

        return trainingstr

    def _prepare_convertorl2str(self, regis_interval, regis_recovery):
        # Special preparation for interval training 2 string, combine interval and recover
        interval_strtype = regis_interval[0]
        intervals = regis_interval[1]
        recovery_strtype = regis_recovery[0]
        recoveries = regis_recovery[1]

        convertlist = []
        for i in range(len(recoveries)):
            convertlist.append([intervals[i], interval_strtype])
            convertlist.append([recoveries[i], "P" + recovery_strtype])

        convertlist.append([intervals[i + 1], interval_strtype])
        return convertlist

    def convertor_length2str(self, regis_laps: list) -> str:
        """ """
        trainingstr = ""
        for r_lap in regis_laps:
            if r_lap[1] == "time":
                trainingstr += self._convertor_lapduration2str(r_lap[0]) + ","
            elif r_lap[1] == "distance":
                trainingstr += self._convertor_lapdistance2str(r_lap[0]) + ","
            elif r_lap[1] == "Ptime":
                trainingstr += "P" + self._convertor_lapduration2str(r_lap[0]) + ","
            elif r_lap[1] == "Pdistance":
                trainingstr += "P" + self._convertor_lapdistance2str(r_lap[0]) + ","

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
        speedlist = self.return_paraslist("speed", "avg")
        recovspeed = self._classifylap_speedupspeeddown(speedlist)

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
