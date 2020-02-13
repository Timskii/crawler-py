import pymongo

connection = pymongo.MongoClient(
            host= '192.168.1.208',
            port= 27017,
            username= 'u',
            password= 'u123',
            authSource= 'crawlers'
        )

db = connection.crawlers