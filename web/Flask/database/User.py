import sqlite3,os,sys
from flask_restful import Resource, reqparse


class User():
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def find_user(self, username, password):
        path = "{}/database/data.db".format(os.getcwd())
        #path ="/home/viettinh/Desktop/learing/AI/Project/Face_mask_web/BTL-python/web/Flask/database/data.db"
        connection = sqlite3.connect(path)
        cursor = connection.cursor()

        query = "SELECT * FROM user WHERE name = ? AND password = ?"
        result = cursor.execute(query, (username, password))
        row = result.fetchone()
        if row:
            user = User(row[1], row[2], row[3])
        else:
            user = None
        connection.close()
        return user
    @classmethod
    def create_user(self, username, password , email):
        path = "{}/database/data.db".format(os.getcwd())
        #path ="/home/viettinh/Desktop/learing/AI/Project/Face_mask_web/BTL-python/web/Flask/database/data.db"
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user")
 
        rows = cursor.fetchall()
        cnt_user =1
        for row in rows:
            cnt_user += 1

        cursor.execute("INSERT INTO user VALUES( ? , ?, ? , ?)",(cnt_user,username,password , email))
        connection.commit() 
        connection.close()