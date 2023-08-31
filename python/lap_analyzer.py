from typing import Tuple, Union
import numpy as np
from polar_base import Base_polar


class RLapAnalyzerBasic:
    """
    basic class for analyzing manual/automatic laps
    """

    def __init__(self, laps: dict):
        self.param = Base_polar.run_classattr["lap_param"]
        self.paces = Base_polar.run_classattr["lap_paces"]
        self.laps = self._reshapelaps(laps)

    def _reshapelaps(self, laps) -> dict:
        result = {}
        for par in self.param:
            try:
                temp = {par: [la[par] for la in laps]}
            except KeyError:
                temp = {par: None}
            except TypeError:
                continue
            result.update(temp)
        return result

    def _check_allempty_data(self, param: str):
        self.laps[param]

        empty = []
        for i, data in enumerate(self.laps[param]):
            if len(data) == 0:
                empty.append(i)
        if len(empty) == len(self.laps[param]):
            return True
        else:
            return False

    def return_paraslist(self, par: str, *arg: str) -> list[float]:
        temp = self.laps[par]
        values = []
        if len(arg) == 0:
            # values = [la for la in temp]
            values = temp
        else:
            for la in temp:
                try:
                    values.append(la[arg[0]])
                except KeyError:
                    values.append(-999)

        return values

    def print_nrlaps(self) -> None:
        print(len(self.laps["speed"]))

    def compare_hr_sp(self) -> np.array([float, float]) | None:
        if self.laps["heartRate"] is None or self.laps["speed"] is None:
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

    def _determine_accelaration(
        self, ignorelaps: list[int] = []
    ) -> np.array:  # , mindspeed=0.400):
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
            # print(speedarr)
            result = all(speedarr > min_speed)
        return result

    def identify_easyrun(self, max_speed: float or None = None) -> bool:
        if self._check_allempty_data("speed"):
            return False

        if max_speed is None:
            max_speed = self.paces["maxeasy"]

        speed = []
        for sp in self.laps["speed"]:
            if len(sp) != 0:
                speed.append(sp["avg"])
        speed = np.array(speed)

        result = all(speed <= max_speed)

        return result


class RAutoLapAnalyzer(RLapAnalyzerBasic):
    def __init__(self, alaps: dict):
        # super(RAutoLapAnalyzer, self).__init__(alaps)
        super().__init__(alaps)


class RManualLapAnalyzer(RLapAnalyzerBasic):
    def __init__(self, laps: dict):
        # super(RManualLapAnalyzer, self).__init__(laps)
        super().__init__(laps)

    def return_distance(self) -> list[float]:
        return self.laps["distance"]

    def return_duration(self) -> list[str]:
        return self.laps["duration"]

    def determine_startuprunoutlaps(self, su_speed=None) -> list[list, list]:
        nodata = self._check_allempty_data("speed")
        if nodata:
            return [], []
        if su_speed is None:
            su_speed = self.paces["maxruninout"]
        idx_su = []
        i1 = 0

        # if not self.laps["speed"]:
        #     # empty self.laps
        #     return [], []
        # code hieronder kan niet omgaan met een lege dictionaryin laps["speed"]
        for speed in self.laps["speed"]:
            if len(speed) == 0:
                idx_su.append(i1)
                i1 += 1
            else:
                if speed["avg"] > su_speed:
                    break
                else:
                    idx_su.append(i1)
                    i1 += 1

        idx_ro = []
        i2 = len(self.laps["speed"]) - 1
        while self.laps["speed"][i2]["avg"] < su_speed and i2 > i1:
            idx_ro.append(i2)
            i2 -= 1
        return idx_su, idx_ro

    def determine_lapswithoutsu(self) -> Union[dict, None]:
        su = self.determine_startuprunoutlaps()
        if su == ([], []):
            return None

        su = su[0] + su[1]
        su.sort()
        su.reverse()
        laps = self.laps.copy()
        for k in laps:
            for i_la in su:
                if laps[k] is None:
                    break
                laps[k].pop(i_la)
        return laps

    def identify_interval(self) -> str:
        if self._check_allempty_data("speed"):
            return "undetermined"

        dspeed_int = self.paces["dspeedinterval"]
        laps = self.determine_lapswithoutsu()
        if not laps:
            return "undetermined"

        speed = np.array([sp["avg"] for sp in laps["speed"]])
        sprint = self.identify_sprints()
        easyrun = self.identify_easyrun()

        if speed.shape[0] < 5:
            return "no interval, crit. 1"
        elif sprint or easyrun:
            return "no interval, crit. 2"

        dspeed = speed[1:] - speed[0:-1]
        dspeed[(dspeed < dspeed_int) & (dspeed > -dspeed_int)] = 0
        dspeed[dspeed > dspeed_int] = 1
        dspeed[dspeed < -dspeed_int] = -1
        if np.count_nonzero(dspeed == 0) / len(dspeed) > 0.25:
            return "no interval, crit. 3, under investigation."

        deriv = dspeed[1:] + dspeed[0:-1]
        if sum(deriv) == 0:
            return "interval"

        if len(speed) > 8 and len(dspeed[dspeed == -1]) / len(dspeed) > 1 / 3:
            return "interval, check1"

        if len(speed) == 5 and len(dspeed[dspeed == -1]) == 2:
            return "interval, check2"
        else:
            return "no interval, crit. 4, under investigation"

    def identify_sprints(self, max_time: float = 20.0, min_cadence: int = 98) -> bool:
        sprints = []
        for lnr in range(len(self.laps["duration"])):
            lapdur_str = self.laps["duration"][lnr]
            lapdur = float(lapdur_str.lstrip("PT").rstrip("S"))
            if lapdur < max_time:  # and lapcadence_max > min_cadence:
                sprints.append(lnr)
        result = len(sprints) > 3
        return result