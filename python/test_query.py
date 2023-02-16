from nosql_adapter import MongoPolar

mong = MongoPolar("polartest", "polardb")
curs = mong.morecomplexquery(
    {"exercises.distance": {"$gt": 10000}, "exercises.sport": "CYCLING"}
)
x = 0
for c in curs:
    print(c)
    x += 1
print(x)
