import Communities.community
import mysql.connector
db = mysql.connector.connect(host='localhost', database='mini_bulletin', user='root', password='root')

cursor = db.cursor()

def insert(comm : Communities.community.community):
    descr = comm.description
    name = comm.name
    admin = comm.Admin
    query = "INSERT INTO community VALUES(%s,%s,%s)"
    args = (name, admin, descr)
    cursor.execute(query, args)

