import mysql.connector
from mysql.connector import Error

class CommentReaction:
    def __init__(self, reaction_ID, reacting_user, comment_ID):
        self.reaction_ID = reaction_ID
        self.reacting_user = reacting_user
        self.comment_ID = comment_ID

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
    def add_reaction(cls, comment_id, user_id, reaction_type):
        #Add a reaction (upvote/downvote) to a comment
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor()
            # Check if the user has already reacted
            cursor.execute("SELECT * FROM comment_reaction WHERE comment_ID = %s AND reacting_user = %s", (comment_id, user_id))
            existing_reaction = cursor.fetchone()

            if existing_reaction:
                cursor.close()
                connection.close()
                return  # User has already reacted

            cursor.execute(
                "INSERT INTO comment_reaction (reacting_user, comment_ID, reaction_type) VALUES (%s, %s, %s)",
                (user_id, comment_id, reaction_type)
            )
            connection.commit()
            cursor.close()
            connection.close()

    @classmethod
    def remove_reaction(cls, comment_id, user_id):
        """Remove a reaction from a comment"""
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM comment_reaction WHERE reacting_user = %s AND comment_ID = %s",
                (user_id, comment_id)
            )
            connection.commit()
            cursor.close()
            connection.close()

    @classmethod
    def get_upvotes(cls, comment_id):
        #Get the count of upvotes for a comment
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM comment_reaction WHERE comment_ID = %s AND reaction_type = 'upvote'",
                (comment_id,)
            )
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return result[0] if result else 0

    @classmethod
    def get_downvotes(cls, comment_id):
        #Get the count of downvotes for a comment
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM comment_reaction WHERE comment_ID = %s AND reaction_type = 'downvote'",
                (comment_id,)
            )
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return result[0] if result else 0