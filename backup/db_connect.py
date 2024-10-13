import mysql.connector
import psycopg2
import pymongo
import sqlite3

def connect_to_db(db_type, config):
    try:
        if db_type == "mysql":
            conn = mysql.connector.connect(
                host=config['host'], user=config['user'], password=config['password'], database=config['database'])
        elif db_type == "postgresql":
            conn = psycopg2.connect(
                host=config['host'], user=config['user'], password=config['password'], dbname=config['database'])
        elif db_type == "mongodb":
            conn = pymongo.MongoClient(f"mongodb://{config['host']}:{config['port']}")
        elif db_type == "sqlite":
            conn = sqlite3.connect(config['database'])
        print("Connection successful!")
        return conn
    except Exception as e:
        print(f"Connection failed: {e}")
        return None
