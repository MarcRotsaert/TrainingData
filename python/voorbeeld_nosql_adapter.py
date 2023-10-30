from nosql_adapter import MongoGarminfit, MongoForerunner, MongoPolar

# GET DATA FROM database

mongad = MongoPolar("testdatabase", "polar2014")
mongad.showConnections()
coll = mongad.getCollection()
mongad.put_jsonresume('training-session-2014-01-29-263915306-c594a26f-6a29-4752-8bbb-a70b61e2b742.json')
mongad.put_jsonresume('training-session-2014-01-29-263915306-c594a26f-6a29-4752-8bbb-a70b61e2b742.json')
print(len(mongad.returnDocs()))
mongad.delete_duplicates()
docs = mongad.returnDocs()
print(len(mongad.returnDocs()))

if True:
    docs = mongad.return_docsrunning()
    for it in docs:
        print(it["fname"])

if True:
    # remove fields
    items1 = mongad.getbyField("hr_reliability")
    for it in items1:
        mongad.deleteField(it["_id"], "hr_reliability")

    items2 = mongad.getbyField("hr_reliability")
    i = 0
    for it in items2:
        i += 1
    print(i)

# CHANGE DATABASE
if True:
    docs = mongad.returnDocs()
    ids = docs[0]["_id"]
    print(ids)
    if True:
        mongad.updateOne(ids, {"exportVersion": "69.0"})
    print("____________________________________")

monggf = MongoGarminfit("testdatabase", "garminfit")
monggf.put_jsonresume("marcrotsaert_169919458.fit")

mongfr = MongoForerunner("testdatabase", "polar2004")
mongfr.showDocs()
mongfr.put_jsonresume("20050725-190632.xml")
print(mongfr.returnDocs())

