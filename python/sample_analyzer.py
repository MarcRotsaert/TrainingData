import os
from typing import Tuple, Iterable, Union
import numpy as np
import datetime

import json
from matplotlib import pyplot as pp
import shapely as shp
import geopandas as gpd
import tomli

import vector


class SampleAnalyzerBasic:
    def __init__(self, samples: dict):
        config = tomli.load(open("config.toml", "rb"))
        self.samples = samples
        self.locations = config["running"]["sample_loc"]
        self.param = config["running"]["sample_param"]
        self.paces = config["running"]["sample_paces"]

        self.len_samples = len(samples['speed'])
        self.len_route = len(samples['recordedRoute'])

    def return_samples(self) -> dict[list]:
        return self.samples

    def return_s_heartrate(self) -> list[dict]:
        return self.samples["heartRate"]

    def return_s_route(self) -> Union[list[dict], None]:
        try:
            route = self.samples["recordedRoute"]
        except KeyError:
            route = None
        return route

    def return_s_rcoord(self) -> [list, list]:
        recordedroute = self.return_s_route()
        lon = [rec["longitude"] for rec in recordedroute]
        lat = [rec["latitude"] for rec in recordedroute]
        return lon, lat

    def return_s_timeroute(self, tzoffset: int = 0) -> np.array:
        recordedroute = self.return_s_route()
        # tzoffset=self.jsonobj['exercises'][0]['timezoneOffset']
        dtRoute = [
            datetime.datetime.fromisoformat(rec["dateTime"])
            - datetime.timedelta(0, seconds=tzoffset)
            for rec in recordedroute
        ]
        dtRoute = np.array(dtRoute)
        return dtRoute

    def return_s_timesamples(self) -> np.array:
        dump = self.return_s_speed()
        dt = [
            datetime.datetime.fromisoformat(d["dateTime"])
            for d in dump
        ]
        dt = np.array(dt)
        return dt

    def return_s_speed(self) -> list[dict]:
        return self.samples["speed"]

    def return_s_pointsel(
        self, pnr: Union[None, Iterable[int]] = None
    ) -> gpd.array.GeometryArray:
        # get points
        rlat = []
        rlon = []
        route = self.return_s_route()
        if pnr is None:
            pnr = range(len(route))

        for nr in pnr:
            temp = route[nr]
            rlon.append(temp["longitude"])
            rlat.append(temp["latitude"])
        points = gpd.points_from_xy(rlon, rlat, crs="EPSG:4326")
        pointsrd = points.to_crs("EPSG:28992")
        return pointsrd

    def determine_s_routecentre(self) -> shp.Point:
        rpointsrd = self.return_s_pointsel()
        rpolyrd = shp.Polygon([[p.x, p.y] for p in rpointsrd])
        return rpolyrd.centroid

    def determine_s_location(self) -> Union[str, None]:
        if self.return_s_route() is None:
            location = None
        else:
            location = None
            pnts = self.return_s_pointsel([5, -5])

            for loc, coord in self.locations.items():
                pointloc = shp.Point(coord[0][0], coord[0][1])
                diststart = pointloc.distance(pnts[0])
                distend = pointloc.distance(pnts[-1])
                maxdist = coord[1]
                if diststart < maxdist or distend < maxdist:
                    location = loc
        return location

    def plot(self, param: str) -> None:
        if param not in self.param:
            raise AttributeError
        pp.figure()
        values = [item["value"] for item in self.samples[param]]
        pp.plot(values)
        pp.grid()
        pp.show()

    def return_v_sample(self, param: str, idx: int) -> Union[float, None]:
        if 'value' in self.samples[param][idx]:
            value = self.samples[param][idx]['value']
        else:
            value = None
        return value


class SamAnalTiming(SampleAnalyzerBasic):
    def __init__(self, samples: dict[list]):
        super(SamAnalTiming, self).__init__(samples)

    def return_idx_bytime(self, dt: datetime.datetime,
                          param: str,
                          firstorlast: str = 'first') -> int:
        if param.lower() == 'recordedroute':
            dtimearr = self.return_s_timeroute()
        elif param.lower() == 'samples':
            dtimearr = self.return_s_timesamples()

        if firstorlast == 'first':
            idx = np.where(dtimearr >= dt)[0][0]
        elif firstorlast == 'last':
            idx = np.where(dtimearr <= dt)[0][0]
        return idx

    def determine_timediff_samp2route(self):
        dt = self.return_s_timesamples()
        dtroute = self.return_s_timeroute()
        diff_dt = [dt[0] - dtroute[0], dt[-1] - dtroute[-1]]
        return diff_dt

    def _lineup_tr2ts(self) -> int:
        if self.len_samples-self.len_route == 1:
            i_start = 1
        else:
            dt = self.return_s_timesamples()
            dtRoute = self.return_s_timeroute()
            diff_dt = self.determine_timediff_samp2route()
          
            if datetime.timedelta(0, -10, 0) < diff_dt[1] < datetime.timedelta(0, -1, 0):
                dtRoute = dtRoute + diff_dt[1]

            # Correction in time zone difference between samples and route
            # 2014 and 2015 data.
            if datetime.timedelta(0, -3000, 0) < diff_dt[1]:
                dtRoute = dtRoute + diff_dt[1]

            i_start = np.where(dt <= dtRoute[0])[0][-1]
        return i_start

    def _lineup_tr2ts_source(self):
        pass

    def _lineup_tr2ts_timezone(self):
        pass

    def lineup_troute2tsamples(self) -> int:
        """
        timing recorded route is not in always line with samples.
        Because
        - timezone, samples are in GMT, recordedroute in UMt (2014, 2015)
        - GPS failure, missing values for recorded route
        - source, recorded route takes timestring from GPS, samples from watch.
        """

        if self.len_samples == self.len_route:
            i_start = 0
        else:
            i_start = self._lineup_tr2ts()
        return i_start

    @staticmethod
    def timeshift(dt: np.array, deltat: datetime.timedelta) -> np.array:
        return dt+deltat

    def check_tzcoor_samples2route(self):
        """
        Check if timing route corresponds to timing.
        """
        pass


class SamAnalExtra(SamAnalTiming):
    def __init__(self, samples: dict[list]):
        super(SamAnalExtra, self).__init__(samples)

    def return_idxlowmovement(self) -> Tuple[Union[int, None], Union[int, None]]:
        # return index of  low activity at beginning and end of a session
        speed = self.return_s_speed()
        speedlist = [sp["value"] for sp in speed]
        speed_arr = np.array(speedlist)
        i_b = np.argwhere(speed_arr > self.paces["low_movement"])[0][0]
        i_e = np.where(speed_arr > self.paces["low_movement"])[0][-1]
        if i_e == speed_arr.shape[0] - 1:
            i_e = None
        if i_b == 0:
            i_e = None
        return i_b, i_e

    def extract_heading(self) -> list[float]:
        """
        Haal ruwe heading to uit de route
        """
        heading = [0]
        lon, lat = self.return_s_rcoord()

        for i in range(len(lon) - 1):
            heading.append(
                vector.degn_cart2naut_gt(lon[i + 1] - lon[i], lat[i + 1] - lat[i])
            )
        return heading

    def calc_relwindrichting(self, windricht: float) -> np.array:
        """
        Bereken relatieve windrichting voor
        """
        heading = self.return_normalizedheading()
        relwind = []
        for h in heading:
            difwind = h - windricht
            if difwind <= -180:
                relwind.append(np.mod(difwind, 360))
            elif difwind < 0:
                relwind.append(-difwind)
            elif difwind >= 180:
                relwind.append((-difwind % 360))
            else:
                relwind.append(difwind)
        return np.array(relwind)

    def return_normalizedheading(
        self,
    ):
        """
        array, heading, die opgelijnd is met de samples.
        """
        heading = self.extract_heading()
        return np.array(heading)

    def return_normalizedrelwind(self, windrich: float) -> list:
        """
        array, relatieve wind van afgelegde route.
        """
        relwind = self.calc_relwindrichting(windrich)
        # inds1 = self._stripstartindexroute()
        # inds2 = self._stripendindexroute()
        # relwind = relwind[inds1:inds2]
        return relwind

    def export_geojson(self, filename="geojsontest", pad=r"C:\temp") -> None:
        dtRoute = self.return_s_timeroute()
        lon, lat = self.return_s_rcoord()
        dt = self.return_s_timesamples()
        i_start = self.lineup_troute2tsamples()
        print('_______________________________________')

        if abs(len(dt[i_start:])-len(dtRoute)) > 30:
            raise IndexError

        if len(dt[i_start:]) < len(dtRoute):
            l_index = len(dt[i_start:])
        else:
            l_index = len(dtRoute)

        features = []
        for i in range(0, l_index):
            level310 = {
                "speed": self.return_v_sample("speed", i + i_start),
                "heartrate": self.return_v_sample("heartRate", i + i_start),
                "distance": self.return_v_sample("distance", i + i_start),
                "tijd": dt[i + i_start].isoformat(),
            }
            level300 = {"type": "Point",
                        "coordinates": [lon[i],
                                        lat[i]]}
            level20 = {"type": "Feature",
                       "geometry": level300,
                       "properties": level310}
            features.append(level20)
        level1 = {"type": "FeatureCollection",
                  "features": features}
        fp = open(os.path.join(pad, filename + "_punt.json"), "w")
        json.dump(level1, fp)
        fp.close()

        features = []
        linecoordinates = [[lon[i], lat[i]] for i in range(len(lon))]
        level301 = {"type": "LineString", "coordinates": linecoordinates}
        level311 = {"sport": "dummy"}
        level21 = {"type": "feature",
                   "geometry": level301,
                   "properties": level311}
        features.append(level21)
        level1 = {"type": "FeatureCollection",
                  "features": features}
        fp = open(os.path.join(pad, filename + "_lijn.json"), "w")
        json.dump(level1, fp)
        fp.close()
