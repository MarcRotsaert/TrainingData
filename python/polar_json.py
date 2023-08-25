# Processing data export polar data json files

import os
import json
from typing import Tuple, Iterable, Union
import geopandas as gpd
import shapely as shp
import numpy as np
from polar_base import Base_polar_json

from matplotlib import pyplot as pp
from shapely.geometry.point import Point
from geopandas.array import GeometryArray

# import seaborn


class Trainses:
    def __init__(self, path: str, file: str):
        self.path = path
        self.file = file
        self.read_json()
        self.data = True

    def read_json(self) -> None:
        with open(os.path.join(self.path, self.file)) as g:
            temp = g.read()
        data = json.loads(temp)
        self.add_data(data)

    def add_data_db(self, datadb: dict) -> None:
        self.laps = datadb.pop("laps")
        self.alaps = datadb.pop("autolaps")
        self.abstract = datadb
        self.data = True

    def add_data(self, data: dict):
        self.data = data
        try:
            self.samples = data["exercises"][0].pop("samples")
        except:
            pass
        try:
            self.laps = data["exercises"][0].pop("laps")
        except KeyError:
            self.laps = None
        try:
            self.alaps = data["exercises"][0].pop("autoLaps")
        except KeyError:
            self.alaps = None
        data.update({"fname": self.file})

        param = ["speed", "heartrate", "ascent", "descent", "sport"]
        for par in param:
            if par in data["exercises"][0]:
                data.update({par: data["exercises"][0][par]})

        data.pop("exercises")
        self.abstract = data
        self.data = True

    def _returninit(self) -> None:
        if not self.data:
            self.read_json()

    def return_laps(self) -> list[dict]:
        self._returninit()
        return self.laps

    def return_autolaps(self) -> list[dict]:
        self._returninit()
        return self.alaps

    def return_sport(self) -> str:
        self._returninit()
        return self.abstract["sport"]


class Trainses_mongo(Trainses):
    def __init__(self, datadb):
        self.laps = datadb.pop("laps")
        self.alaps = datadb.pop("autolaps")
        self.abstract = datadb
        self.data = True


class RLapAnalyzerBasic:
    """
    basic class for analyzing manual/automatic laps
    """

    def __init__(self, laps: dict):
        self.param = Base_polar_json.run_classattr["lap_param"]
        self.paces = Base_polar_json.run_classattr["lap_paces"]
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
        if self.laps["heartRate"] == None or self.laps["speed"] == None:
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
        stdv = np.std(hrt)
        maxhrt = np.max(hrt)
        minhrt = np.max(hrt)
        return stdhrt, maxhrt, minhrt

    def identify_roadrace(
        self, ignorelaps: list = [], min_speed: float or None = None
    ) -> bool:
        if min_speed == None:
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
        # else:
        # params = self.return_speedvariability()
        # if all(np.array(self.return_paraslist('speed'))>min_speed)
        #     if std
        return result

    def identify_easyrun(self, max_speed: float or None = None) -> bool:
        if max_speed == None:
            max_speed = self.paces["maxeasy"]

        # laps = self.return_lapswithoutsu()
        speed = np.array([sp["avg"] for sp in self.laps["speed"]])
        if any(speed > max_speed):
            result = False
        else:
            result = True

        return result
        # for la in laps:


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
        if su_speed == None:
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

        if len(sprints) > 3:
            result = True
        else:
            result = False

        return result


class SampleAnalyzerBasic:
    def __init__(self, samples: dict):
        self.samples = samples
        self.locations = Base_polar_json.run_classattr["sample_loc"]

    def return_samples(self) -> dict[dict]:
        # self._returninit()
        return self.samples

    def return_s_heartrate(self) -> list[dict]:
        return self.samples["heartRate"]

    def return_s_route(self) -> Union[list[dict], None]:
        # self._returninit()
        try:
            route = self.samples["recordedRoute"]
        except KeyError:
            route = None
        return route

    def return_s_speed(self) -> list[dict]:
        return self.samples["speed"]

    def return_s_heartrate(self):
        # self._returninit()
        return self.samples["heartRate"]

    # def return_s_pointsel(self, pnr=None):
    def return_s_pointsel(
        self, pnr: Union[None, Iterable[int]] = None
    ) -> GeometryArray:
        # get points
        rlat = []
        rlon = []
        route = self.return_s_route()
        if pnr == None:
            pnr = range(len(route))

        for nr in pnr:
            temp = route[nr]
            rlon.append(temp["longitude"])
            rlat.append(temp["latitude"])
        points = gpd.points_from_xy(rlon, rlat, crs="EPSG:4326")
        pointsrd = points.to_crs("EPSG:28992")
        return pointsrd

    def determine_s_routecentre(self) -> Point:
        rpointsrd = self.return_s_pointsel()
        rpolyrd = shp.Polygon([[p.x, p.y] for p in rpointsrd])
        # rpolyrd = rpoly.to_crs("EPSG:28992")
        return rpolyrd.centroid

    def determine_s_location(self) -> Union[str, None]:
        deflocs = {
            "de velden": [[85575, 440076], 100],
            "baanbras": [[85085, 449400], 100],
            "kopjesloop": [[85055, 448570], 50],
            "schiehaven": [[90775, 435330], 600],
            "wippolder": [[86255, 446810], 150],
            "bergenopzoom": [[81385, 389191], 400],
            "menmoerhoeve": [[104258, 394390], 200],
            "sola": [[395744, -72146], 15000],
            "meijendel": [[82905, 460500], 300],
        }
        if self.return_s_route() is None:
            location = None
        else:
            location = None
            pnts = self.return_s_pointsel([5, -5])

            for loc in deflocs:
                pointloc = shp.Point(deflocs[loc][0][0], deflocs[loc][0][1])
                diststart = pointloc.distance(pnts[0])
                distend = pointloc.distance(pnts[-1])
                maxdist = deflocs[loc][1]
                if diststart < maxdist or distend < maxdist:
                    location = loc
        return location

    def plot(self, param: str) -> None:
        fig = pp.figure()
        # try:
        values = [item["value"] for item in self.samples[param]]
        pp.plot(values)
        # except:
        #    xx
        # pp.ylim(8, 22)
        pp.grid()
        pp.show()


class SamAnalExtra(SampleAnalyzerBasic):
    def __init__(self, samples: dict[dict]):
        super(SamAnalExtra, self).__init__(samples)
        # print(self.return_s_heartrate())

    def return_idxlowmovement(self) -> Tuple[Union[int, None], Union[int, None]]:
        # return index of  low activity at beginning and end of a
        speed = self.return_s_speed()
        speedlist = [sp["value"] for sp in speed]
        speed_arr = np.array(speedlist)
        i_b = np.argwhere(speed_arr > 7)[0][0]
        i_e = np.where(speed_arr > 7)[0][-1]
        if i_e == speed_arr.shape[0] - 1:
            i_e = None
        if i_b == 0:
            i_e = None
        return i_b, i_e


if __name__ == "__main__":
    path = r"C:\Users\marcr\Polar\Polar\data\polar-user-data-export"
    import glob

    if False:
        file = "training-session-2015-04-18-263883440-3be46e75-6a93-4746-a320-96c9660f809c.json"
        session = Trainses(path, file)
        # alaps = session.return_alaps()
        lapses = RAutoLapAnalyzer(session.alaps)
        result = lapses.return_accelartion()
        print(result)
        print(sum(result))
        xx
    if True:
        # file = "training-session-2019-10-30-4009640085-5105bf47-b37c-47c3-a96c-d74653ae0d5a.json"
        file = "training-session-2015-06-26-263879702-2d485ab0-ef26-4100-b2ae-1ca9c5f144d6.json"
        # training-session-2015-07-03-263876996-e9c14b6c-bc80-4c10-b335-91081c2552e7.json
        # training-session-2015-09-20-263873564-7f116bac-8756-4f54-a5a0-9272ec0f44ee.json
        # training-session-2015-09-22
        # training-session-2015-09-29-263860670-b456e24e-4325-411f-b2c6-3e3a3bc29de6.json
        # training-session-2015-10-24-263861018-3690058d-71c0-47c3-8539-e7b67e8099fe.json

        # training-session-2015-10-17-263860916-1b563b91-c4f4-4991-878c-5c1225f84b2c.json
        session = Trainses(path, file)
        laps = session.return_laps()
        lapses = RManualLapAnalyzer(laps)

        x = lapses.return_paraslist("speed")
        result = lapses.determine_startuprunoutlaps()
        print(lapses.identify_interval())
        samses = SamAnalExtra(session.samples)
        samses.plot("speed")
        # xx

    if True:
        file = "training-session-2015-01-14-263888618-3d72bde3-4957-4db4-8fa6-662a180a2d23.json"
        session = Trainses(path, file)
        # alaps = session.return_alaps()
        lapses = RAutoLapAnalyzer(session.alaps)
        result = lapses.identify_roadrace()
        # xx
    if True:
        file = "training-session-2015-04-18-263883440-3be46e75-6a93-4746-a320-96c9660f809c.json"

        session = Trainses(path, file)
        laps = session.return_laps()
        lapses = RManualLapAnalyzer(session.laps)
        # xx
        # print(session.return_startuprunoutlaps())
        # laps = session.return_lapswithoutsu()
        # result = session.identify_easyrun()
        # result = session.identify_interval()

        # su_laps = lapses.return_startuprunoutlaps()
        # ignorelaps = su_laps[0] + su_laps[1]
        # result = lapses.identify_roadrace(ignorelaps)
        # print(result)
        # xx

    # xx
    if False:
        session = SampleAnalyzerBasic(session.samples)
        session = SamAnalExtra(session.samples)
        X = session.filter_lowmovement()

        # if True:
        x
    files = glob.glob(os.path.join(path, "training-session-2022-*.json"))
    pointcoll = []
    for fi in files:
        # "training-session-2014-12-07-263916482-2cbe9312-6b71-4693-8519-a9a860a23cbc.json"
        filename = fi.split("\\")[-1]
        print(filename)
        session = Trainses(path, filename)

        if False:
            if session.laps != None:
                # session = RLapAnalyzerBasic(session.laps)
                # session.print_nrlaps()
                session = RManualLapAnalyzer(session.laps)
                # print(session.return_startuprunoutlaps())
                # print(session.return_startuprunoutlaps())
                # laps = session.return_lapswithoutsu()
                print(result)
                session.compare_hr_sp()
        if True:
            if session.laps != None:
                sessionl = RManualLapAnalyzer(session.laps)
                result = sessionl.identify_interval()
                print(result)

                result = sessionl.identify_sprints()
                print("sprints? " + str(result))

            if session.alaps != None:
                try:
                    sessiona = RManualLapAnalyzer(session.alaps)
                    sessiona = RManualLapAnalyzer(session.alaps)
                    result = sessiona.identify_easyrun()
                    print("easyrun?" + str(result))
                except:
                    pass

            print("_______________________________")
        if False:
            session = SamAnalExtra(session.samples)
            session.plot("speed")
        if False:
            # resume = session.return_resume()
            # print(resume)
            # xx
            # samples = session.return_samples()
            # laps = session.return_laps()
            # print(laps)
            alaps = session.return_autolaps()
            print(alaps)

            print(session.return_s_location())
            print(session.samples)
        if False:
            pointcoll.append(session.return_s_routecentre())
            print(filename + ":" + str(session.return_s_routecentre()))
            # print(filename + ":" + str(session.return_s_location()))
            gdf = gpd.GeoDataFrame(geometry=pointcoll, crs="EPSG:28992")
            gdf.to_file("C:/temp/polartest.shp")
