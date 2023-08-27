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

    def return_paraslist(self, par: str, *arg: str) -> list[float]:
        temp = self.laps[par]
        values = []
        if len(arg) == 0:
            values = [la for la in temp]
        else:
            for la in temp:
                try:
                    values.append(la[arg[0]])
                except KeyError:
                    values.append(-999)
            # values = [la[arg[0]] for la in temp]

        return values

    def print_nrlaps(self) -> None:
        print(len(self.laps["speed"]))

    def compare_hr_sp(self) -> Tuple[float, float] | str:
        if self.laps["heartRate"] is None or self.laps["speed"] is None:
            print("no heartrate or speed")
            # return
        else:
            avgheartr = self.return_paraslist("heartRate", "avg")
            avgspeed = self.return_paraslist("speed", "avg")
            # heartr = self.laps["heartRate"]
            # speed = self.laps["speed"]
            # avgspeed = [sp["avg"] for sp in speed]
            # avgheartr = [hr["avg"] for hr in heartr]
            # xx
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
        # dspeed[(dspeed > -mindspeed) & (dspeed < mindspeed)] = 0
        # dspeed[dspeed > mindspeed] = 1
        # dspeed[dspeed < -mindspeed] = -1
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
            print(speedarr)
            if all(speedarr > min_speed):
                all(speedarr)
                result = True
            else:
                result = False
        return result

    def identify_easyrun(self, max_speed: float or None = None) -> bool:
        if max_speed is None:
            max_speed = self.paces["maxeasy"]

        # laps = self.return_lapswithoutsu()
        speed = np.array([sp["avg"] for sp in self.laps["speed"]])
        if any(speed > max_speed):
            result = False
        else:
            result = True

        return result


class RAutoLapAnalyzer(RLapAnalyzerBasic):
    def __init__(self, alaps):
        super(RAutoLapAnalyzer, self).__init__(alaps)


class RManualLapAnalyzer(RLapAnalyzerBasic):
    def __init__(self, laps):
        super(RManualLapAnalyzer, self).__init__(laps)

    def return_distance(self) -> list[float]:
        return self.laps["distance"]

    def return_duration(self) -> list[str]:
        return self.laps["duration"]

    def determine_startuprunoutlaps(self, su_speed=None) -> list[list, list]:
        if su_speed is None:
            su_speed = self.paces["maxruninout"]
        idx_su = []
        i1 = 0

        if not self.laps["speed"]:
            # empty self.laps
            return None
        # code hieronder kan niet omgaan met een lege dictionaryin laps["speed"]
        for speed in self.laps["speed"]:
            # [i1]["avg"] < su_speed
            # and i1 < len(self.laps["speed"]) - 1
            # ):
            if len(speed) == 0:
                idx_su.append(i1)
                i1 += 1
                continue
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
        if not su:
            return None
        su = su[0] + su[1]
        su.sort()
        su.reverse()
        laps = self.laps.copy()
        for k in laps:
            for i_la in su:
                try:
                    laps[k].pop(i_la)
                except AttributeError:  # None values
                    break
        return laps

    def identify_interval(self) -> Union[str, None]:
        dspeed_int = self.paces["dspeedinterval"]
        laps = self.determine_lapswithoutsu()
        if not laps:
            return None

        speed = np.array([sp["avg"] for sp in laps["speed"]])
        sprint = self.identify_sprints()
        easyrun = self.identify_easyrun()

        if speed.shape[0] < 5:
            result = "no interval, crit. 1"
        elif sprint or easyrun:
            result = "no interval, crit. 2"
        else:
            dspeed = speed[1:] - speed[0:-1]
            dspeed[(dspeed < dspeed_int) & (dspeed > -dspeed_int)] = 0
            dspeed[dspeed > dspeed_int] = 1
            dspeed[dspeed < -dspeed_int] = -1
            if np.count_nonzero(dspeed == 0) / len(dspeed) > 0.25:
                result = "no interval, crit. 3, under investigation."
            else:
                deriv = dspeed[1:] + dspeed[0:-1]
                if sum(deriv) == 0:
                    # print(deriv)
                    result = "interval"
                else:
                    if (
                        len(speed) > 8
                        and len(dspeed[dspeed == -1]) / len(dspeed) > 1 / 3
                    ):
                        result = "interval, check1"

                    elif len(speed) == 5 and len(dspeed[dspeed == -1]) == 2:
                        result = "interval, check2"
                    else:
                        result = "no interval, crit. 4, under investigation"
        return result

    def identify_sprints(self, max_time: float = 20.0, min_cadence: int = 98) -> bool:
        sprints = []
        for lnr in range(len(self.laps["duration"])):
            lapdur_str = self.laps["duration"][lnr]
            # lapcadence_max = self.laps["cadence"][lnr]["max"]
            lapdur = float(lapdur_str.lstrip("PT").rstrip("S"))
            if lapdur < max_time:  # and lapcadence_max > min_cadence:
                sprints.append(lnr)
        result = len(sprints) > 3
        return result
