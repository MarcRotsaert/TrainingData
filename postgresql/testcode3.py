import json
import psycopg as psql


from nosql_adapter import MongoQuery

from analyzer import sample_analyzer as saman
import analyzer.polar_analyzer as polan
from trainsession import Trainsession_file

training = polan.Trainses_json(
    "training-session-2023-12-28-7788129097-dec336e5-f1c8-405d-872d-0c73bc6cffe4.json"
)

samples = training.return_samples()
samobj = saman.SamAnalExtra(samples)


conn = "postgresql://postgres:NederlandBelgie@localhost:5432/testdb?"
# obj = samobj.to_postgis("qgis2", conn)
geoline = samobj._line2geojson()
# geopoint = samobj._point2geojson()

print(geoline)
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
            CREATE TABLE IF NOT EXISTS qgis3 (
                _id text PRIMARY KEY,
                fname text,
                geom geometry(LineString, 4326))
            """
        )

        cur.execute("DELETE FROM qgis3 WHERE _id = %s ;", ("2",))

        cur.execute(
            "INSERT INTO qgis3 (_id, fname, geom ) VALUES (%s, %s, ST_GeomFromGeoJSON(%s))",
            (2, "dummy.json", json.dumps(geoline["features"][0]["geometry"])),
        )
    conn.commit()
