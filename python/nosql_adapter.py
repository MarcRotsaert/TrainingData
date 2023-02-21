import sys
from pymongo import MongoClient

sys.path.append(r"C:\Users\marcr\Polar\Polar\python")
import polar_json as pj


class MongoAdapter:
    def __init__(self, mongoDB, collection):
        self.client = MongoClient(
            host="localhost:27017",
            serverSelectionTimeoutMS=3000,
            username="student",
            password="miw3",
        )
        self.dbname = mongoDB
        self.collection = collection

    def getClient(self):
        return self.client

    def getCollection(self):
        db = self.client[self.dbname]
        # db = self.client[dbName]
        return db[self.collection]

    def insertOne(self, dictToInsert):
        # collection = self.getCollection("polar", "resume")
        collection = self.getCollection()
        collection.insert_one(dictToInsert)

    def updateOne(self, objid, dictToUpdate):
        collection = self.getCollection()
        collection.update_one({"_id": objid}, {"$set": dictToUpdate})

    def deleteCollection(self):
        # collection = self.getCollection("polar", collectionName)
        collection = self.getCollection()
        collection.drop()

    def showDocs(self):
        # collection = self.getCollection("polar", collectionName)
        collection = self.getCollection()
        cursor = collection.find({})
        for doc in cursor:
            print(doc)

    def returnDocs(self):
        # collection = self.getCollection("polar", collectionName)
        collection = self.getCollection()
        cursor = collection.find({})
        return cursor

    def showConnections(self):
        client = self.getClient()
        print(client)

    def simplequery(self, keyn, valn):
        # collection = self.getCollection("polar", collectionName)
        collection = self.getCollection()
        cursor = collection.find({keyn: valn})
        return cursor

    def morecomplexquery(self, query):
        # {"distance":{"$gt":"7000"}}
        collection = self.getCollection()
        cursor = collection.find(query)
        return cursor

    def deleteDocument(self, document):
        collection = self.getCollection()
        collection.delete_one(document)


class MongoPolar(MongoAdapter):
    def __init__(self, mongoDB, collection):
        super().__init__(mongoDB, collection)

    def find_docsrunning(self):
        curs = self.simplequery("exercises.sport", "RUNNING")
        return curs

    def put_jsonresume(self, path, fname):
        sess = pj.Trainses(path, fname)
        resume = sess.abstract
        SamAnal = pj.SampleAnalyzerBasic(sess.samples)
        loc = SamAnal.return_s_location()
        resume.update({"location": loc, "laps": sess.laps, "autolaps": sess.alaps})
        # resume = sess.return_resume()
        self.insertOne(resume)


if __name__ == "__main__":
    # mongad = MongoAdapter("guess_who", "mongo-1")
    mongad = MongoPolar("polartest", "polardb")
    mongad.showConnections()
    mongad.getCollection()
    docs = mongad.returnDocs()
    ids = docs[0]["_id"]
    print(ids)
    # mongad.showDocs()
    # mongad.updateOne(ids, {"exercises.distance": 10000})
    if False:
        mongad.updateOne(ids, {"exportVersion": "69.0"})
        mongad.updateOne(ids, {"trainingtype": "blasting"})
    docs = mongad.returnDocs()
    ids = docs[0]["_id"]
    print(ids)

    # session = pj.Trainses(
    #     r"C:\Users\marcr\Polar\Polar\data\polar-user-data-export",
    #     "training-session-2013-12-29-263917040-9e3eaf26-016e-4401-b268-402cb95f389c.json",
    # )

    # res = mongad.find_docssport()
    # print(res)
    # mongad.insertOne(res)
    # xx
    # mongad = MongoAdapter("polartest", "mongo-1")
    # coll = mongad.getCollection("polartest", "mongo-1")
    mongad.showConnections()
    if False:
        resume = session.return_resume()
        mongad.insertOne(resume)

    # mongad.insertOne({"ja": [1]})

    print("____________________________________")

    # curs = mongad.simplequery("exportVersion", "1.6")
    curs = mongad.morecomplexquery({"latitude": {"$gt": 0}})
    curs = mongad.morecomplexquery({"physicalInformationSnapshot.sex": "MALE"})
    # curs = mongad.morecomplexquery({"exercises[0].distance": 8960.0})
    curs = mongad.morecomplexquery({"exercises.speed.avg": {"$gt": 14}})
    curs = mongad.morecomplexquery(
        {"exercises.speed.avg": {"$gt": 14}, "exercises.heartRate.avg": {"$gt": 140}}
    )
    # print(dir(curs))
    for c in curs:
        print(c["exercises"][0]["heartRate"]["avg"])
