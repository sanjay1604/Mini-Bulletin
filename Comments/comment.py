import mysql.connector
from mysql.connector import Error

class Comment:
    def __init__(self, comment_id, commenting_user, comment_message, post_id):
        self.comment_id = comment_id
        self.commenting_user = commenting_user
        self.comment_message = comment_message
        self.post_id = post_id

    @classmethod
    def get_db_connection(cls):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='mini_bulletin'
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    @classmethod
    def add_comment(cls, commenting_user, comment_message, post_id):
        connection = cls.get_db_connection()  # Assuming this is a method to get DB connection
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO comments (commenting_user, comment_message, post_ID) VALUES (%s, %s, %s)",
                (commenting_user, comment_message, post_id)  # Make sure post_id is passed as integer
            )
            connection.commit()
            cursor.close()
            connection.close()
    
    @classmethod 
    def delete_comment(cls, comment_id):
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM comments WHERE comment_ID = %s",(comment_id,)
            )
        connection.commit()
        cursor.close()
        connection.close()



    @classmethod
    def get_comments_by_post(cls, post_id):
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM comments WHERE post_ID = %s", (post_id,))
            comments = cursor.fetchall()
            cursor.close()
            connection.close()
            return comments
        return []
    
    @classmethod
    def get_by_id(cls,comment_id):
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("select * from comments where comment_id=%s",[comment_id])
            comment = cursor.fetchone()
            cursor.close()
            connection.close()
            return comment
            
