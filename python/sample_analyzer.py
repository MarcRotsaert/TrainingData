from typing import Tuple, Iterable, Union
import numpy as np
from matplotlib import pyplot as pp
import shapely as shp
import geopandas as gpd

from polar_base import Base_polar


class SampleAnalyzerBasic:
    def __init__(self, samples: dict):
        self.samples = samples
        self.locations = Base_polar.run_classattr["sample_loc"]
        self.param = Base_polar.run_classattr["sample_param"]
        self.paces = Base_polar.run_classattr["sample_paces"]

    def return_samples(self) -> dict[dict]:
        return self.samples

    def return_s_heartrate(self) -> list[dict]:
        return self.samples["heartRate"]

    def return_s_route(self) -> Union[list[dict], None]:
        try:
            route = self.samples["recordedRoute"]
        except KeyError:
            route = None
        return route

    def return_s_speed(self) -> list[dict]:
        return self.samples["speed"]

    def return_s_heartrate(self):
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
    def __init__(self, samples: dict[dict]):
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
