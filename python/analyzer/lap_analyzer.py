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

    def return_paraslist(
        self, par: str, ext_par: str = None, ind: Union[None, list] = None
    ) -> list[float]:
        temp = self.laps_an[par]
        values = []
        # if len(arg) == 0:
        # values = temp
        # else:
        if ind is None:
            lapsel = range(len(temp))
        else:
            lapsel = ind

        # for la in temp:
        for la in lapsel:
            if ext_par is not None:
                try:
                    val = temp[la][ext_par]
                except KeyError:
                    val = -999
            else:
                val = temp[la]
            values.append(val)

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

    def _classify_speedupdown(self, speedlist: list) -> np.array:
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

    def return_idx_intrec(self) -> [np.array, np.array]:
        """determine index of intervals and recovery in manual laps"""
        idx_su, idx_ru = self.determine_startuprunoutlaps()

        speedlist = self.return_paraslist("speed", "avg")
        speed_updown = self._classify_speedupdown(speedlist)
        for i in idx_su + idx_ru:
            speed_updown[i] = 0

        idx_int = np.where(speed_updown == 1)[0]
        idx_rec = np.where(speed_updown == -1)[0]
        return idx_int, idx_rec

    @staticmethod
    def _return_corrected_speed(
        m_speed: np.array, m_dist: np.array, c_dist: np.array
    ) -> np.array:
        """
        Calculate corrected speed
        m_speed: measured speed,
        m_dist: measured distance
        c_dist: corrected distance
        """
        return np.round(m_speed * c_dist / m_dist, 1)

    def determine_corrspeed_int(self) -> np.array:
        """Determine corrected speed after correction distance of a lap"""
        int_strtype, _, corr_int, _ = self.determine_intervals()
        if int_strtype == "distance":
            idx_int, _ = self.return_idx_intrec()
            int_dist_meas = self.return_distance(idx_int)
            int_speed_meas = self.return_paraslist("speed", "avg", idx_int)

            corr_speed = self._return_corrected_speed(
                int_speed_meas, int_dist_meas, corr_int
            )
            return corr_speed

        else:
            return None

    def determine_intervals(self) -> [str, str, list, list]:
        """determine lapinterval size in distance or time"""
        idx_int, idx_rec = self.return_idx_intrec()

        distance_interval = self.return_distance(idx_int)
        duration_interval = self.return_duration(idx_int)
        distance_recovery = self.return_distance(idx_rec)
        duration_recovery = self.return_duration(idx_rec)

        regis_interval = self._classify_timedistance(
            distance_interval, duration_interval
        )
        regis_recovery = self._classify_timedistance(
            distance_recovery, duration_recovery
        )
        int_strtype = regis_interval[0]
        corr_int = regis_interval[1]
        rec_strtype = regis_recovery[0]
        corr_rec = regis_recovery[1]
        return int_strtype, rec_strtype, corr_int, corr_rec

    def return_intervalstring(self) -> str:
        int_strtype, rec_strtype, corr_int, corr_rec = self.determine_intervals()

        if rec_strtype != "undetermined" and int_strtype != "undetermined":
            if len(corr_int) - len(corr_rec) == 1:
                regis_laps = self._prepare_convertorl2str(
                    int_strtype, rec_strtype, corr_int, corr_rec
                )
                trainingstr = self.convertor_length2str(regis_laps)
            else:
                trainingstr = "error: nr. interval laps equals nr recovery laps"

        else:
            trainingstr = "undetermined"

        return trainingstr

    def _prepare_convertorl2str(
        self, int_strtype: str, rec_strtype: str, corr_int: list, corr_rec: list
    ) -> list:
        convertlist = []
        for i in range(len(corr_rec)):
            convertlist.append([corr_int[i], int_strtype])
            convertlist.append([corr_rec[i], "P" + rec_strtype])

        convertlist.append([corr_int[i + 1], int_strtype])
        return convertlist

    def convertor_length2str(self, regis_laps: list) -> str:
        """ """
        trainingstr = ""
        for r_lap in regis_laps:
            if r_lap[1] in ["time", "distance"]:
                if r_lap[1] == "time":
                    temp = self._convertor_lapduration2str(r_lap[0]) + ","
                else:
                    temp = self._convertor_lapdistance2str(r_lap[0]) + ","

                temp = temp.ljust(7)
                trainingstr += temp
        trainingstr += "\n"

        x = True
        for r_lap in regis_laps:
            if r_lap[1] in ["Ptime", "Pdistance"]:
                if r_lap[1] == "Ptime":
                    temp = "P" + self._convertor_lapduration2str(r_lap[0]) + ","
                else:
                    temp = "P" + self._convertor_lapdistance2str(r_lap[0]) + ","

                if x:
                    temp = temp.rjust(10)
                    x = False
                else:
                    temp = temp.rjust(7)
                trainingstr += temp
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
        recovspeed = self._classify_speedupdown(speedlist)

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
