import os
import json
import geopandas as gpd
import shapely as shp


class Trainses:
    def __init__(self, path, file):
        self.path = path
        self.file = file
        self.data = False

    def read_json(self):
        with open(os.path.join(self.path, self.file)) as g:
            temp = g.read()
        data = json.loads(temp)
        self.samples = data["exercises"][0].pop("samples")
        try:
            self.laps = data["exercises"][0].pop("laps")
        except KeyError:
            pass
        try:
            self.alaps = data["exercises"][0].pop("autoLaps")
        except KeyError:
            pass
        data.update({"fname": self.file})
        self.resume = data
        self.data = True

    def _returninit(self):
        if not self.data:
            self.read_json()

    def return_resume(self):
        self._returninit()
        return self.resume

    def return_laps(self):
        self._returninit()
        return self.laps

    def return_autolaps(self):
        self._returninit()
        return self.alaps

    def return_sport(self):
        self._returninit()
        return self.resume["sport"]

    def return_samples(self):
        self._returninit()
        return self.samples

    def return_route(self):
        self._returninit()
        return self.samples["recordedRoute"]

    def return_heartrate(self):
        self._returninit()
        return self.samples["heartRate"]

    def return_pointsel(self, pnr=None):
        rlat = []
        rlon = []
        route = self.return_route()
        if pnr == None:
            pnr = range(len(route))

        for nr in pnr:
            temp = route[nr]
            rlon.append(temp["longitude"])
            rlat.append(temp["latitude"])
        points = gpd.points_from_xy(rlon, rlat, crs="EPSG:4326")
        pointsrd = points.to_crs("EPSG:28992")
        return pointsrd

    def return_location(self):
        deflocs = {
            "de velden": [[85575, 440076], 100],
            "baanbras": [[85085, 449400], 100],
            "kopjesloop": [[85055, 448570], 75],
            "schiehaven": [[90775, 435330], 600],
            "wippolder": [[86255, 446810], 150],
            "bergenopzoom": [[81385, 389191], 400],
            "menmoerhoeve": [[104258, 394390], 200],
        }
        location = None
        pnts = self.return_pointsel([5, -5])

        for loc in deflocs:
            pointloc = shp.Point(deflocs[loc][0][0], deflocs[loc][0][1])

            diststart = pointloc.distance(pnts[0])
            distend = pointloc.distance(pnts[-1])
            maxdist = deflocs[loc][1]
            if diststart < maxdist or distend < maxdist:
                location = loc
        return location

    def return_routecentre(self):
        rpointsrd = self.return_pointsel()
        rpolyrd = shp.Polygon([[p.x, p.y] for p in rpointsrd])
        # rpolyrd = rpoly.to_crs("EPSG:28992")
        return rpolyrd.centroid


if __name__ == "__main__":
    path = r"C:\Users\marcr\Polar\Polar\data\polar-user-data-export"
    import glob

    files = glob.glob(os.path.join(path, "training-session-2019-12*.json"))
    for fi in files:
        # "training-session-2014-12-07-263916482-2cbe9312-6b71-4693-8519-a9a860a23cbc.json"
        filename = fi.split("\\")[-1]
        session = Trainses(path, filename)
        if False:
            resume = session.return_resume()
            samples = session.return_samples()
            laps = session.return_laps()
            alaps = session.return_autolaps()

            print(session.return_location())
            print(laps)
            print(alaps)
            print(samples)
            print(resume)
        print(filename + ":" + str(session.return_routecentre()))
        # print(filename + ":" + str(session.return_location()))
    xx
    # print(type(temp))
    # print(temp)
    # print(len(data))
    # print(data.keys())
    # print(data.keys())
    # Trainses()

    # data["exercises"][0]
    # data["exercises"][0]["sport"]

    # data["exercises"][0]["laps"][1]
    # data["exercises"][0]["samples"]["recordedRoute"][10]["latitude"]
    # data["exercises"][0]["samples"]["speed"][10]["value"]
    # data["exercises"][0]["samples"]["speed"][10]["dateTime"]
    # data["exercises"][0]["samples"]["distance"]
    # data["exercises"][0]["samples"]["heartRate"]
    # lat = data["exercises"][0]["latitude"]
    # lon = data["exercises"][0]["longitude"]

    # # point = Point(lon, lat)

    # locations = {
    #     "develden": [85575, 440076],
    #     "baanbras": [85085, 449400],
    #     "kopjesloop": [85055, 448570],
    #     "schiehaven": [90775, 435330],
    #     "wippolder": [86255, 446810],
    # }

    # """
    # point = gpd.points_from_xy([lon], [lat], crs="EPSG:4326")
    # pointrd = point.to_crs("EPSG:28992")
    # for loc in locations:
    #     pointloc = shp.Point(locations[loc][0], locations[loc][1])
    #     print(pointloc.distance(pointrd[0]))
    # """

    # route = data["exercises"][0]["samples"]["recordedRoute"]
    # rlon = []
    # rlat = []
    # for dpoint in route:
    #     rlon.append(dpoint["longitude"])
    #     rlat.append(dpoint["latitude"])
    # rpoints = gpd.points_from_xy(rlon, rlat, crs="EPSG:4326")
    # rpointsrd = rpoints.to_crs("EPSG:28992")

    # #
    # for loc in locations:
    #     pointloc = shp.Point(locations[loc][0], locations[loc][1])
    #     print(pointloc.distance(rpointsrd[-1]))

    # # centroid of route
    # rpolyrd = shp.Polygon([[p.x, p.y] for p in rpointsrd])
    # # rpolyrd = rpoly.to_crs("EPSG:28992")
    # print(rpolyrd.centroid)
    # for loc in locations:
    #     pointloc = shp.Point(locations[loc][0], locations[loc][1])
    #     print(pointloc.distance(rpolyrd.centroid))

    # dir(point)
