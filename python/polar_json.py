import os
import json
from typing import Iterable, Union
import geopandas as gpd
import shapely as shp
import numpy as np
from matplotlib import pyplot as pp

# import seaborn


class Trainses:
    def __init__(self, path, file):
        self.path = path
        self.file = file
        self.read_json()
        self.data = True

    def read_json(self):
        with open(os.path.join(self.path, self.file)) as g:
            temp = g.read()
        data = json.loads(temp)
        self.add_data(data)

    def add_data_db(self, datadb):
        self.laps = datadb.pop("laps")
        self.alaps = datadb.pop("autolaps")
        self.abstract = datadb
        self.data = True

    def add_data(self, data):
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

        param = ["speed", "heartrate", "ascent", "decent", "sport"]
        for par in param:
            if par in data:
                data.update({par: data["exercises"][0][par]})

        data.pop("exercises")
        self.abstract = data
        self.data = True

    def _returninit(self):
        if not self.data:
            self.read_json()

    def return_laps(self):
        self._returninit()
        return self.laps

    def return_autolaps(self):
        self._returninit()
        return self.alaps

    def return_sport(self):
        self._returninit()
        return self.abstract["sport"]


class LapAnalyzerBasic:
    """
    basic class for automatic and manual laps
    """

    def __init__(self, laps: dict):

        self.laps = self._reshapelaps(laps)

    def _reshapelaps(self, laps):
        param = ["distance", "duration", "heartRate", "speed", "ascent", "descent"]
        result = {}
        for par in param:
            try:
                temp = {par: [la[par] for la in laps]}
            except KeyError:
                temp = {par: None}
            result.update(temp)
        return result

    def print_nrlaps(self):
        print(len(self.laps["speed"]))

    def compare_hr_sp(self):
        if self.laps["heartRate"] == None or self.laps["speed"] == None:
            print("no heartrate or speed")
            # return
        else:
            heartr = self.laps["heartRate"]
            speed = self.laps["speed"]
            avgspeed = [sp["avg"] for sp in speed]
            avgheartr = [hr["avg"] for hr in heartr]

            print(np.corrcoef(avgspeed, avgheartr)[0, 1])


class LapAnalyzerManual(LapAnalyzerBasic):
    def __init__(self, laps):
        super(LapAnalyzerManual, self).__init__(laps)

    def return_startuprunoutlaps(self):
        su_speed = 13.5
        idx_su = []
        i1 = 0
        while (
            self.laps["speed"][i1]["avg"] < su_speed
            and i1 < len(self.laps["speed"]) - 1
        ):
            idx_su.append(i1)
            i1 += 1
        idx_ro = []
        i2 = len(self.laps["speed"]) - 1
        while self.laps["speed"][i2]["avg"] < su_speed and i2 > i1:
            idx_ro.append(i2)
            i2 -= 1
        return idx_su, idx_ro


class SampleAnalyzerBasic:
    def __init__(self, samples: dict):
        self.samples = samples

    def return_samples(self):
        # self._returninit()
        return self.samples

    def return_s_heartrate(self):
        return self.samples["heartRate"]

    def return_s_routecentre(self):
        rpointsrd = self.return_s_pointsel()
        rpolyrd = shp.Polygon([[p.x, p.y] for p in rpointsrd])
        # rpolyrd = rpoly.to_crs("EPSG:28992")
        return rpolyrd.centroid

    def return_s_route(self):
        # self._returninit()
        try:
            route = self.samples["recordedRoute"]
        except KeyError:
            route = None
        return route

    def return_s_speed(self):
        return self.samples["speed"]

    def return_s_heartrate(self):
        # self._returninit()
        return self.samples["heartRate"]

    # def return_s_pointsel(self, pnr=None):
    def return_s_pointsel(self, pnr: Union[None, Iterable] = None):
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

    def return_s_location(self):
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
        if self.return_s_route() == None:
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

    def plot(self, param):
        fig = pp.figure()
        values = [item["value"] for item in self.samples[param]]
        pp.plot(values)
        pp.show()


class SamAnalExtra(SampleAnalyzerBasic):
    def __init__(self, samples):
        super(SamAnalExtra, self).__init__(samples)
        # print(self.return_s_heartrate())

    def return_idxlowmovement(self):
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

    file = "training-session-2022-08-28-7472610630-322188f8-2d0a-43c6-b85f-7e797fc0ebb2.json"

    session = Trainses(path, file)
    session = LapAnalyzerManual(session.laps)
    print(session.return_startuprunoutlaps())
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
        if True:
            if session.laps != None:
                # session = LapAnalyzerBasic(session.laps)
                # session.print_nrlaps()
                # session.compare_hr_sp()
                session = LapAnalyzerManual(session.laps)
                print(session.return_startuprunoutlaps())
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
