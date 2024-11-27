import mysql.connector

mydb2 = mysql.connector.connect(host="localhost",  user="root",  password="root",  database="mini_bulletin")
mycursor2 = mydb2.cursor()

class userDB:
    db = None
    cursor = None

    def __init__(self):
        self.db = mydb2
        self.cursor = mydb2.cursor()

    def insert_user(self,user_name,user_password):
        query = "INSERT INTO users (username, password) VALUES (%s,%s)"
        args=[user_name,user_password]
        result = self.cursor.execute(query, args)
        self.db.commit()
    
    def retrieve_user(self):
        query = "SELECT username FROM users"
        self.cursor.execute(query)
        us = self.cursor.fetchall()
        return us
    
    def user_login(self,user_name,user_password):
        query = "SELECT username FROM users WHERE username=%s and password=%s"
        args=[user_name, user_password]
        self.cursor.execute(query,args)
        us = self.cursor.fetchall()
        if us ==[]:
            return False
        else:
            return True
    
    def get(self,name):
        query = "SELECT * FROM users WHERE username=%s"
        args = [name]
        self.cursor.execute(query, args)
        return self.cursor.fetchall()
    