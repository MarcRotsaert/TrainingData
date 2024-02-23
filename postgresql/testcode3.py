import json
import psycopg as psql


from nosql_adapter import MongoQuery

from analyzer import sample_analyzer as saman
import analyzer.polar_analyzer as polan


conn = "postgresql://postgres:NederlandBelgie@localhost:5432/testdb?"
# obj = samobj.to_postgis("qgis2", conn)
# print(geopoint)

mongocurs = MongoQuery("polartest", "polar2023").returnDocs()
with psql.connect(
    dbname="testdb", user="postgres", password="NederlandBelgie", host="localhost"
) as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:
        # Execute a command: this creates a new table
        cur.execute(
            """
            DROP TABLE IF EXISTS qgis3
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS qgis3 (
                _id serial PRIMARY KEY,
                fname text,
                distance int,
                duration int,
                geom geometry(LineString, 4326))
            """
        )
        conn.commit()
        # cur.execute("DELETE FROM qgis3 WHERE _id = %s ;", ("2",))

        for doc in mongocurs:
            filename = doc["fname"]
            print(filename)
            training = polan.Trainses_json(filename)
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
                    "INSERT INTO qgis3 (_id, fname, distance, duration, geom ) VALUES (DEFAULT, %s, %s, %s, ST_GeomFromGeoJSON(%s))",
                    (
                        filename,
                        dist,
                        dur,
                        json.dumps(geoline["features"][0]["geometry"]),
                    ),
                )
    conn.commit()
