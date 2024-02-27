import psycopg as psql

from nosql_adapter import MongoQuery


mongocurs = MongoQuery("polartest", "polar2023").returnDocs()


with psql.connect(
    dbname="testdb", user="postgres", password="NederlandBelgie", host="localhost"
) as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:
        # Execute a command: this creates a new table
        cur.execute("DROP TABLE IF EXISTS test2")
        cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        cur.execute(
            """
            CREATE TABLE test2 (
                _id text PRIMARY KEY,
                num integer,
                fname text)
            """
        )

        for nr, it in enumerate(mongocurs):
            fname = it["fname"]
            _id = str(it["_id"])
            print(fname)
            # Pass data to fill a query placeholders and let Psycopg perform
            # the correct conversion (no SQL injections!)
            cur.execute(
                "INSERT INTO test2 (_id, num,  fname) VALUES (%s, %s, %s)",
                (_id, nr, fname),
            )

        # Query the database and obtain data as Python objects.
        cur.execute("SELECT * FROM test2")
        cur.fetchall()
        # will return (1, 100, "abc'def")

        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        for record in cur:
            print(record)

        # Make the changes to the database persistent
        conn.commit()
