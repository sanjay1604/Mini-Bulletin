#import Communities.community
import Users.users as user
import mysql.connector

mydb = mysql.connector.connect(host="localhost",  user="root",  password="root",  database="mini_bulletin")
mycursor = mydb.cursor()

class communityDB:
    db = None
    cursor = None

    def __init__(self):
        self.db = mydb
        self.cursor = mydb.cursor()

    def insert(self, descr, name, admin):
        query = "INSERT INTO community (c_name, Admin, descr) VALUES (%s,%s,%s)"
        args = name, admin, descr
        result = self.cursor.execute(query, args)
        self.db.commit()
        print(args)
        print("row inserted")
        print(result)
        
    def retrieve(self, username):
        query = "SELECT C.c_name, C.descr, C.Admin, M.c_name FROM community C LEFT JOIN members M ON C.c_name=M.c_name AND M.username = %s"
        args = [username]
        self.cursor.execute(query, args)
        comms = self.cursor.fetchall()
        return comms
    
    def addMember(self, name, username):
        query = "INSERT INTO members (c_name, username) VALUES (%s,%s)"
        args = [name, username]
        result = self.cursor.execute(query,args)
        self.db.commit()

    def remove(self,name):
        query = "DELETE FROM community WHERE c_name=%s"
        args = [ name ]
        result=self.cursor.execute(query,args)
        self.db.commit()

    def update(self,name, newDesc):
        query = "UPDATE community SET descr = %s WHERE c_name=%s"
        args = [newDesc, name]
        result = self.cursor.execute(query, args)
        self.db.commit()

    def get(self,name):
        query = "SELECT * FROM community WHERE c_name=%s"
        args = [name]
        self.cursor.execute(query, args)
        return self.cursor.fetchall()
    
    def userRetrieve(self,admin):
        query = "SELECT * FROM community WHERE admin=%s"
        args = [admin]
        self.cursor.execute(query, args)
        return self.cursor.fetchall()
    
    def adminRetrieve(self,admin):
        query = "select Admin from community where Admin=%s"
        args=[admin]
        self.cursor.execute(query,args)
        return self.cursor.fetchone()
    
    def removeMembers(self,name):
        query = "delete from members where c_name=%s"
        args = [name]
        self.cursor.execute(query, args)
        self.db.commit()
    
    def removeMember(self,name,username):
        query = "delete from members where c_name=%s and username=%s"
        args=[name,username]
        self.cursor.execute(query, args)
        self.db.commit()

    def getCommunityName(self,c_name):
        query = "SELECT c_name FROM community WHERE c_name=%s"
        args = [c_name]
        self.cursor.execute(query, args)
        return self.cursor.fetchone()