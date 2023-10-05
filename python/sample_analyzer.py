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

    def return_s_timeroute(self, tzoffset=0) -> np.array:
        recordedroute = self.return_s_route()
        # tzoffset=self.jsonobj['exercises'][0]['timezoneOffset']
        dtRoute = [
            datetime.datetime.fromisoformat(rec["dateTime"])
            - datetime.timedelta(0, seconds=tzoffset * 60)
            for rec in recordedroute
        ]
        dtRoute = np.array(dtRoute)
        return dtRoute

    def return_s_timesamples(self, tzoffset: int = 0) -> np.array:
        samples = {}
        # tzoffset=self.jsonobj['exercises'][0]['timezoneOffset']
        dump = self.return_s_speed()
        dt = [
            datetime.datetime.fromisoformat(d["dateTime"])
            - datetime.timedelta(0, seconds=tzoffset * 60)
            for d in dump
        ]
        dt = np.array(dt)
        return dt

    def return_s_speed(self) -> list[dict]:
        return self.samples["speed"]

    def return_s_heartrate(self) -> list[dict]:
        return self.samples["heartRate"]

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


class SamAnalExtra(SampleAnalyzerBasic):
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

    def _stripstartindexroute(
        self,
    ) -> Union[int, None]:
        """
        indexnummer voor het strippen tijd Route aan begin.
        """
        dt = self.return_s_timesamples()
        dtRoute = self.return_s_timeroute()
        inds1 = np.where(dtRoute >= dt[0])[0]
        if len(inds1) == 0:
            inds1 = None
        else:
            inds1 = inds1[0]
        return inds1

    def _stripendindexroute(
        self,
    ) -> Union[int, None]:
        """
        indexnummer voor het strippen tijd Route aan einde.
        """

        dt = self.return_s_timesamples()
        dtRoute = self.return_s_timeroute()
        inds2 = np.where(dtRoute > dt[-1])[0]
        if len(inds2) == 0:
            inds2 = None
        else:
            inds2 = inds2[0] - 1
        return inds2

    def _stripstartindexsamples(
        self,
    ) -> Union[int, None]:
        """
        indexnummer voor het strippen Samples aan begin.
        """
        dt = self.return_s_timesamples()
        dtRoute = self.return_s_timeroute()
        inds1 = np.where(dt >= dtRoute[0])[0]
        if len(inds1) == 0:
            inds1 = None
        else:
            inds1 = inds1[0]
        return inds1

    def _stripendindexsamples(
        self,
    ) -> Union[int, None]:
        """
        integer, indexnummer voor het strippen Samples aan einde.
        """
        dt = self.return_s_timesamples()
        dtRoute = self.return_s_timeroute()
        inds2 = np.where(dt > dtRoute[-1])[0]
        if len(inds2) == 0:
            inds2 = None
        else:
            inds2 = inds2[0] - 1
        return inds2

    def return_normalizedroute(
        self,
    ) -> Tuple[list, list, list]:
        """
        Oplijnen van array route ten opzichte van tijd van samples (hartslag, snelheid).
        uitvoer:
            uitvoer: array, tijdstippen genormaliseerde  lengtegraad en breedtegraad en bijbehorende tijd
        """
        dtRoute = self.return_s_timeroute()
        lon, lat = self.return_s_rcoord()
        inds1 = self._stripstartindexroute()
        inds2 = self._stripendindexroute()
        dtRoute = dtRoute[inds1:inds2]
        lon = lon[inds1:inds2]
        lat = lat[inds1:inds2]
        return dtRoute, lon, lat

    def return_normalizedheading(
        self,
    ):
        """
        array, heading, die opgelijnd is met de samples.
        """
        heading = self.extract_heading()
        inds1 = self._stripstartindexroute()
        inds2 = self._stripendindexroute()
        heading = heading[inds1:inds2]
        return np.array(heading)

    def return_normalizedrelwind(self, windrich: float) -> list:
        """
        array, relatieve wind van afgelegde route.
        """
        relwind = self.calc_relwindrichting(windrich)
        inds1 = self._stripstartindexroute()
        inds2 = self._stripendindexroute()
        relwind = relwind[inds1:inds2]
        return relwind

    def return_normalizedsamples(
        self,
    ):
        """
        array, genormaliseerde samples
        """
        # samples = self.extract_samples()
        dt = self.return_s_timesamples()
        inds1 = self._stripstartindexsamples()
        inds2 = self._stripendindexsamples()
        dt = dt[inds1:inds2]
        samples = self.samples
        for sam in self.samples:
            samples[sam] = samples[sam][inds1:inds2]

        dtRoute = self.return_s_timeroute()
        inds1 = self._stripstartindexroute()
        inds2 = self._stripendindexroute()
        dtRoute = dtRoute[inds1:inds2]

        ind1 = [0]
        while len(ind1) != 0:
            # try:
            deltat = dt[0 : len(dtRoute)] - dtRoute
            # except:
            #    print(len(dt))
            #    print(len(dtRoute))
            #    return dt,dtRoute
            ind1 = np.where(deltat < datetime.timedelta(0, -1, 0))[0]

            if len(ind1) == 0:
                continue
            ind2 = np.where(dtRoute[ind1[0]] < dt)[0]
            print(ind1)
            print(ind2)
            dt = np.concatenate((dt[0:ind1[0]], dt[ind2[0]-1:]))
            for sam in samples:
                samples[sam] = np.concatenate(
                    (samples[sam][0:ind1[0]], samples[sam][ind2[0]-1:])
                )

    def export_geojson(self, filename="geojsontest", pad=r"C:\temp") -> None:
        features = []
        dtroute, lon, lat = self.return_normalizedroute()
        dt, samples = self.return_normalizedsamples()
        heading = self.return_normalizedheading()

        for i in range(len(dtroute) - 1):
            # for i in range(50):
            level310 = {
                "speed": samples["speed"][i],
                "heartrate": samples["heartRate"][i],
                "distance": samples["distance"][i],
                "heading": heading[i],
                "tijd": dt[i].isoformat(),
            }
            level300 = {"type": "Point",
                        "coordinates": [lon[i], lat[i]]}
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
