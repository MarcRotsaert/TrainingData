"""
Skin over mongodb nosql database voor Polar.
"""

import sys
from pymongo import MongoClient
import pymongo


import polar_analyzer as pol_an
from polar_base import Base_nosql


class MongoAdapter:
    # Baseclass Mongo
    def __init__(self, mongoDB: str, collection: str):
        self.client = MongoClient(
            host="localhost:27017",
            serverSelectionTimeoutMS=3000,
            username="student",
            password="miw3",
        )
        self.dbname: str = mongoDB
        self.collection: str = collection

    def getClient(self) -> MongoClient:
        return self.client

    def showConnections(self) -> None:
        client = self.getClient()
        print(client)

    def _getDatabase(self) -> pymongo.database.Database:
        return self.client[self.dbname]

    def getCollection(self) -> pymongo.collection.Collection:
        db = self._getDatabase()
        return db[self.collection]

    def insertOne(self, dictToInsert: dict) -> None:
        collection = self.getCollection()
        collection.insert_one(dictToInsert)

    def updateOne(self, objid: str, dictToUpdate: dict) -> None:
        collection = self.getCollection()
        collection.update_one({"_id": objid}, {"$set": dictToUpdate})

    def deleteField(self, objid: str, fieldToDelete: str) -> None:
        collection = self.getCollection()
        temp = collection.update_one({"_id": objid}, {"$unset": {fieldToDelete: ""}})
        print(temp.raw_result)

    def deleteCollection(self) -> None:
        collection = self.getCollection()
        collection.drop()

    def showDocs(self) -> None:
        cursor = self._cursorDocs()
        for doc in cursor:
            print(doc)

    def returnDocs(self) -> list[dict]:
        cursor = self._cursorDocs()
        docs = [doc for doc in cursor]
        return docs

    def _cursorDocs(self) -> pymongo.cursor.Cursor:
        collection = self.getCollection()
        cursor = collection.find({})
        return cursor

    def getbyField(self, fieldname: str) -> list[dict]:
        collection = self.getCollection()
        items = collection.find({fieldname: {"$exists": True}})
        return items

    def deleteDocument(self, document) -> None:
        collection = self.getCollection()
        collection.delete_one(document)


class MongoQuery(MongoAdapter):
    # def __init__(self, mongoDB, collection):
    #    super().__init__(mongoDB, collection)

    def simplequery(self, keyn: any, valn: any) -> pymongo.cursor.Cursor:
        collection = self.getCollection()
        cursor = collection.find({keyn: valn})
        return cursor

    def morecomplexquery(self, query: dict[any]) -> pymongo.cursor.Cursor:
        collection = self.getCollection()
        cursor = collection.find(query)  # {"distance":{"$gt":"7000"}}
        return cursor


class MongoPolar(MongoQuery):
    """
    Mongo-extension for Polar.
    Data for
    """

    def __init__(self, mongoDB: str, collection: str):
        # initiate collection
        # MongoAdapter.__init__(self, mongoDB, collection)
        # MongoQuery.__init__(self, mongoDB, collection)
        super().__init__(mongoDB, collection)

    def print_resumeattributes(self) -> None:
        # print content resume.
        print(Base_nosql.RESUME)

    def return_docsrunning(self) -> pymongo.cursor.Cursor:
        curs = self.simplequery("sport", "RUNNING")
        return curs

    def put_jsonresume(self, path: str, fname: str) -> None:
        # Add JSON-file to a collection
        sess = pol_an.Trainses_json(path, fname)
        resume = sess.abstract
        SamAnal = pol_an.SampleAnalyzerBasic(sess.samples)
        loc = SamAnal.determine_s_location()
        resume.update({"location": loc, "laps": sess.laps, "autolaps": sess.alaps})
        # resume = sess.return_resume()
        self.insertOne(resume)


if __name__ == "__main__":
    # mongad = MongoAdapter("guess_who", "mongo-1")
    mongad = MongoPolar("polartest4", "polar2018")
    mongad.print_resumeattributes()
    if True:
        mongad.showConnections()
        coll = mongad.getCollection()
        docs = mongad.returnDocs()
        ids = docs[0]["_id"]
        # xx
        print(ids)
        # mongad.showDocs()

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
        # xx
        # mongad.updateOne(ids, {"exercises.distance": 10000})

    if False:
        mongad.updateOne(ids, {"exportVersion": "69.0"})
        mongad.updateOne(ids, {"trainingtype": "blasting"})
    docs = mongad.returnDocs()
    ids = docs[0]["_id"]
    print(ids)

    # session = pol_an.Trainses(
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
    if True:
        # curs = mongad.simplequery("exportVersion", "1.6")
        # curs = mongad.morecomplexquery({"latitude": {"$gt": 0}})
        # curs = mongad.morecomplexquery({"physicalInformationSnapshot.sex": "MALE"})
        # curs = mongad.morecomplexquery({"exercises[0].distance": 8960.0})
        # curs = mongad.morecomplexquery({"exercises.speed.avg": {"$gt": 14}})
        # curs = mongad.morecomplexquery(
        #     {"exercises.speed.avg": {"$gt": 14}, "exercises.heartRate.avg": {"$gt": 140}}
        # )
        curs = mongad.morecomplexquery(
            {"trainingtype.interval": "interval, check", "trainingtype.easyrun": True}
        )
        curs = mongad.simplequery("trainingtype.interval", "interval, check")
        # print(dir(curs))
        for c in curs:
            print(c["fname"])
