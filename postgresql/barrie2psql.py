import json
import psycopg as psql

from datetime import datetime

from nosql_adapter import MongoQuery

from analyzer import sample_analyzer as saman

# import analyzer.polar_analyzer as polan
import analyzer.garmin_analyzer as garan


conn = "postgresql://postgres:NederlandBelgie@localhost:5432/testdb?"
# obj = samobj.to_postgis("qgis2", conn)
# print(geopoint)

mongocurs = MongoQuery("barriedb", "garminfit").returnDocs()


with psql.connect(
    dbname="testdb", user="postgres", password="NederlandBelgie", host="localhost"
) as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:
        # Execute a command: this creates a new table
        cur.execute(
            """
            DROP TABLE IF EXISTS qgis_barrie
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS qgis_barrie (
                _id serial PRIMARY KEY,
                fname text,
                distance int,
                duration int,
                date date,
                geom geometry(LineString, 4326))
            """
        )
        conn.commit()
        # cur.execute("DELETE FROM qgis3 WHERE _id = %s ;", ("2",))

        for doc in mongocurs:
            # if doc["fname"] != "barrie_4@hotmail.com_196836519559.fit":
            #     continue
            starttime = doc["startTime"]
            datetimeobj = datetime.strptime(starttime[0:10], "%Y-%m-%d")
            if datetime.strptime(starttime[0:10], "%Y-%m-%d") < datetime(2023, 6, 1):
                continue
            date = datetimeobj.strftime("%Y-%m-%d")
            filename = doc["fname"]
            print(filename)
            training = garan.Trainses_fit(filename)
            if training.return_sport() == "RUNNING":
                samples = training.return_samples()
                samobj = saman.SamAnalExtra(samples)
                geoline = samobj._line2geojson()
                if geoline is None:
                    continue
                # geopoint = samobj._point2geojson()

                dist = training.abstract["distance"]
                dur = training.abstract["duration"]
                cur.execute(
                    "INSERT INTO qgis_barrie (_id, fname, distance, duration, date, geom ) VALUES (DEFAULT, %s, %s, %s, %s, ST_GeomFromGeoJSON(%s))",
                    (
                        filename,
                        dist,
                        dur,
                        date,
                        json.dumps(geoline["features"][0]["geometry"]),
                    ),
                )
            conn.commit()
            # break
