"""
Skin over mongodb nosql database voor Polar.
"""

import tomli
from pymongo import MongoClient
import pymongo

import polar_analyzer as pol_an
import forerunner_analyzer as for_an


class MongoAdapter:
    # Baseclass Mongo
    def __init__(self, mongoDB: str, collection: str):
        config = tomli.load(open("config.toml", "rb"))
        self.client = MongoClient(
            host=config["mongodb"]["host"],
            serverSelectionTimeoutMS=config["mongodb"]["timeout"],
            username=config["mongodb"]["loginname"],
            password=config["mongodb"]["password"],
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
    def simplequery(self, keyn: any, valn: any) -> pymongo.cursor.Cursor:
        collection = self.getCollection()
        cursor = collection.find({keyn: valn})
        return cursor

    def morecomplexquery(self, query: dict[any]) -> pymongo.cursor.Cursor:
        collection = self.getCollection()
        cursor = collection.find(query)
        return cursor

    def _has_duplicate(self, document: dict) -> bool:
        fname = document["fname"]
        res = self.simplequery("fname", fname)
        if len(list(res)) > 1:
            return True
        else:
            return False

    def find_duplicates(self):
        duplicates = set()
        docs = self.returnDocs()
        for doc in docs:
            if self._has_duplicate(doc):
                duplicates.add(doc["fname"])
        return duplicates

    def delete_duplicates(self) -> None:
        fnames_dupl = self.find_duplicates()
        for fname in fnames_dupl:
            cursor = self.simplequery("fname", fname)
            docs = list(cursor)
            for doc in docs[1:]:
                self.deleteDocument(doc)


class MongoPolar(MongoQuery):
    """
    Mongo-extension for Polar.
    Data for
    """

    def __init__(self, mongoDB: str, collection: str):
        # initiate collection
        super().__init__(mongoDB, collection)

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
        self.insertOne(resume)


class MongoForerunner(MongoQuery):
    """
    Mongo-extension for Forerunner data.
    Data for
    """

    def __init__(self, mongoDB: str, collection: str):
        # initiate collection
        super().__init__(mongoDB, collection)

    def put_jsonresume(self, path: str, fname: str) -> None:
        # Add JSON-file to a collection
        sess = for_an.Trainses_xml(path, fname)
        resume = sess.abstract
        SamAnal = for_an.SampleAnalyzerBasic(sess.samples)
        loc = SamAnal.determine_s_location()
        resume.update({"location": loc, "laps": sess.laps})
        self.insertOne(resume)


if __name__ == "__main__":
    # GET DATA FROM database
    config = tomli.load(open("config.toml", "rb"))
    mongfr = MongoForerunner(config["mongodb"]["database"], "polar2004")

    path = config["forerunner_xml"]["datapath"]
    mongfr.put_jsonresume(path, "20050725-190632.xml")
    print(mongfr.returnDocs())

    mongad = MongoPolar(config["mongodb"]["database"], "polar2014")
    mongad.showConnections()
    coll = mongad.getCollection()
    mongad.delete_duplicates()

    if True:
        mongad.showConnections()
        coll = mongad.getCollection()
        docs = mongad.returnDocs()
        ids = docs[0]["_id"]
        print(ids)

    if True:
        docs = mongad.return_docsrunning()
        for it in docs:
            print(it["fname"])

    if True:
        #
        curs = mongad.simplequery("exportVersion", "1.6")
        curs = mongad.morecomplexquery({"latitude": {"$gt": 0}})
        curs = mongad.morecomplexquery({"physicalInformationSnapshot.sex": "MALE"})
        curs = mongad.morecomplexquery({"exercises[0].distance": 8960.0})
        curs = mongad.morecomplexquery({"exercises.speed.avg": {"$gt": 14}})
        curs = mongad.morecomplexquery(
            {
                "exercises.speed.avg": {"$gt": 14},
                "exercises.heartRate.avg": {"$gt": 140},
            }
        )
        curs = mongad.morecomplexquery(
            {"trainingtype.interval": "interval, check", "trainingtype.easyrun": True}
        )
        curs = mongad.simplequery("trainingtype.interval", "interval, check")
        # print(dir(curs))
        for c in curs:
            print(c["fname"])

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
    docs = mongad.returnDocs()
    ids = docs[0]["_id"]
    print(ids)
    if True:
        mongad.updateOne(ids, {"exportVersion": "69.0"})
    print("____________________________________")
