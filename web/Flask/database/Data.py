import sqlite3,os,sys
from flask_restful import Resource, reqparse
class Data():
    def __init__(self):
        self.path = "{}/database/data.db".format(os.getcwd())
        #cursor = connection.cursor()

    def insert(self, query):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

    def select(self, query):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute(query)
        data = []
        for row in cursor:
            data.append(row)
        return data