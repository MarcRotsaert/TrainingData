import psycopg as psql
import bson
from nosql_adapter import MongoQuery



with psql.connect(
    dbname="testdb", user="postgres", password="NederlandBelgie", host="localhost"
) as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM test2")
        it = cur.fetchone()
        print(it)

mongoq = MongoQuery("polartest", "polar2023")
mongocur =  mongoq.simplequery("_id", bson.ObjectId(it[0]))
x = list(mongocur)
print(x)
# print(list(mongocur))
# mongocur =  mongoq.simplequery("fname", it[3])
# print(list(mongocur))
