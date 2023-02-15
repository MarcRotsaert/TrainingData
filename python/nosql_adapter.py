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

    def deleteDocument(self, document):
        collection = self.getCollection()
        collection.delete_one(document)


if __name__ == "__main__":
    # mongad = MongoAdapter("guess_who", "mongo-1")
    session = pj.Trainses(
        r"C:\Users\marcr\Polar\Polar\data\polar-user-data-export",
        "training-session-2013-12-29-263917040-9e3eaf26-016e-4401-b268-402cb95f389c.json",
    )

    mongad = MongoAdapter("polartest", "mongo-1")
    # coll = mongad.getCollection("polartest", "mongo-1")
    mongad.showConnections()
    if False:
        resume = session.return_resume()
        mongad.insertOne(resume)

    # mongad.insertOne({"ja": [1]})
    docs = mongad.returnDocs()

    print("____________________________________")

    # curs = mongad.simplequery("exportVersion", "1.6")
    curs = mongad.simplequery("lowerLimit", 165)
    # print(dir(curs))
    for c in curs:
        print(c)
    x
