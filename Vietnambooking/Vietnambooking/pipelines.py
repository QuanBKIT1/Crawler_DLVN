# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json 
import re
import pymongo
import mysql.connector

class TravelPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.collection_name = "Travel"
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # Remove the existing collection (if it exists)
        # self.db[self.collection_name].drop()

    def close_spider(self, spider):
        self.client.close()

    
    def process_item(self, item, spider):
                # Clean data
        item["service_des"] = ''.join(item["service_des"])
        keys_strip = ["ticket_ID", "description", "price" ,"duration", "departure_place", "adult_price", "chidren_price", "baby_price", "tour_des", "service_des", "highlights"]
        for key in keys_strip:
            item[key] = item[key].strip()

        # Remove \u00a0 character

        keys_remove = ["title", "description", "tour_des", "service_des"]
        for key in keys_remove:
            item[key] = item[key].replace('\u00a0', ' ')

        # Clean services 
        for i in range(len(item["services"])):
             item["services"][i] = item["services"][i]. replace('\u00a0', '')
        # Clean highlights, tour_des, service_des chains of character \r,\n
        keys_remove_chains = ["highlights", "tour_des", "service_des"]
        for key in keys_remove_chains:
            item[key] = re.sub(r'[\r\n\t]+', '\n', item[key])
        item['price'] = item['price'].replace(item["price_old"],"")

        self.db[self.collection_name].insert_one(dict(item))



class JSonPipeline(object):
    def open_spider(self, spider):
        self.file = open("items.jsonl", "w", encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        
        # Clean data
        item["service_des"] = ''.join(item["service_des"])
        keys_strip = ["ticket_ID", "description", "price" ,"duration", "departure_place", "adult_price", "chidren_price", "baby_price", "tour_des", "service_des", "highlights"]
        for key in keys_strip:
            item[key] = item[key].strip()
        
        # Remove \u00a0 character

        keys_remove = ["title", "description", "tour_des", "service_des"]
        for key in keys_remove:
            item[key] = item[key].replace('\u00a0', ' ')

        # Clean services 
        for i in range(len(item["services"])):
             item["services"][i] = item["services"][i]. replace('\u00a0', '')
        # Clean highlights, tour_des, service_des chains of character \r,\n
        keys_remove_chains = ["highlights", "tour_des", "service_des"]
        for key in keys_remove_chains:
            item[key] = re.sub(r'[\r\n\t]+', '\n', item[key])
        
        item['price'] = item['price'].replace(item["price_old"],"")

        line = json.dumps(dict(item))+"\n"
        self.file.write(line)
        return item
    

class MysqlPipeline(object):
    def __init__(self, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE):
        # Replace these values with your MySQL server and database information
        self.host = MYSQL_HOST
        self.user = MYSQL_USER
        self.password = MYSQL_PASSWORD
        self.database = MYSQL_DATABASE
        self.table = 'tourDLVN'
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            MYSQL_HOST=crawler.settings.get("MYSQL_HOST"),
            MYSQL_USER=crawler.settings.get("MYSQL_USER"),
            MYSQL_PASSWORD=crawler.settings.get("MYSQL_PASSWORD"),
            MYSQL_DATABASE=crawler.settings.get("MYSQL_DATABASE"),

        )
    def open_spider(self, spider):
        # Create a connection to the MySQL database
        # Create the database if it doesn't exist
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
        )        
        # CREATE DATABASE IF NONE EXISTS
        self.cur = self.conn.cursor()
        self.cur.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        self.cur.execute(f"USE {self.database}")
        
        # Create  table if none exists
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            id int NOT NULL auto_increment, 
            title text,
            ticket_ID text,
            price_old text,
            price text,
            duration text,
            description text,
            departure_place text,
            vehicle text,
            time_depart text,
            services text,
            highlights text,
            tour_des text,
            adult_price text,
            chidren_price text,
            baby_price text,
            service_des text,
            PRIMARY KEY (id)
        )
        """)
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
    
    def process_item(self, item, spider):
        # Clean data
        item["service_des"] = ''.join(item["service_des"])
        keys_strip = ["ticket_ID", "description", "price" ,"duration", "departure_place", "adult_price", "chidren_price", "baby_price", "tour_des", "service_des", "highlights"]
        for key in keys_strip:
            item[key] = item[key].strip()

        # Remove \u00a0 character

        keys_remove = ["title", "description", "tour_des", "service_des"]
        for key in keys_remove:
            item[key] = item[key].replace('\u00a0', ' ')

        # Clean services 
        for i in range(len(item["services"])):
             item["services"][i] = item["services"][i]. replace('\u00a0', '')
        # Clean highlights, tour_des, service_des chains of character \r,\n
        keys_remove_chains = ["highlights", "tour_des", "service_des"]
        for key in keys_remove_chains:
            item[key] = re.sub(r'[\r\n\t]+', '\n', item[key])
        item['price'] = item['price'].replace(item["price_old"],"")

        item['vehicle'] = ':'.join(item['vehicle'])
        item['services'] = ':'.join(item['services'])

        self.cur.execute(f""" insert into {self.table} (title,ticket_ID,price_old,price,duration,description,departure_place,vehicle,time_depart,services,highlights,tour_des,adult_price, chidren_price, baby_price, service_des) values 
                         (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
            item["title"],
            item["ticket_ID"],
            item["price_old"],
            item["price"],
            item["duration"],
            item["description"],
            item["departure_place"],
            item["vehicle"],
            item["time_depart"],
            item["services"],
            item["highlights"],
            item["tour_des"],
            item["adult_price"],
            item["chidren_price"],
            item["baby_price"],
            item["service_des"],
        ))
        ## Execute insert of data into database
        self.conn.commit()
