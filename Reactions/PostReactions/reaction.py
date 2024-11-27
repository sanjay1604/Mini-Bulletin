import mysql.connector
from mysql.connector import Error

class PostReaction:
    def __init__(self, reaction_ID, reacting_user, post_ID):
        self.reaction_ID = reaction_ID
        self.reacting_user = reacting_user
        self.post_ID = post_ID

    @classmethod
    def get_db_connection(cls):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Ganesh123*', 
                database='minibulletin'
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    @classmethod
    def upvote(cls, post_ID, reacting_user):
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor()
            # Check if the user has already reacted
            cursor.execute("SELECT * FROM reactions WHERE post_ID = %s AND reacting_user = %s", (post_ID, reacting_user))
            existing_reaction = cursor.fetchone()

            if existing_reaction:
                print(f"User {reacting_user} has already reacted to this post.")
                cursor.close()
                connection.close()
                return  # User has already reacted

            # Insert the new upvote reaction into the database
            cursor.execute(
                "INSERT INTO reactions (post_ID, reacting_user, reaction_type) VALUES (%s, %s, 'upvote')",
                (post_ID, reacting_user)
            )
            connection.commit()
            print(f"User {reacting_user} upvoted the post {post_ID}")
            cursor.close()
            connection.close()

    @classmethod
    def downvote(cls, post_ID, reacting_user):
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor()
            # Check if the user has already reacted
            cursor.execute("SELECT * FROM reactions WHERE post_ID = %s AND reacting_user = %s", (post_ID, reacting_user))
            existing_reaction = cursor.fetchone()

            if existing_reaction:
                print(f"User {reacting_user} has already reacted to this post.")
                cursor.close()
                connection.close()
                return  # User has already reacted

            # Insert the new downvote reaction into the database
            cursor.execute(
                "INSERT INTO reactions (post_ID, reacting_user, reaction_type) VALUES (%s, %s, 'downvote')",
                (post_ID, reacting_user)
            )
            connection.commit()
            print(f"User {reacting_user} downvoted the post {post_ID}")
            cursor.close()
            connection.close()

    @classmethod
    def remove_reaction(cls, post_ID, reacting_user):
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM reactions WHERE post_ID = %s AND reacting_user = %s", (post_ID, reacting_user))
            connection.commit()
            print(f"User {reacting_user} removed their reaction from post {post_ID}")
            cursor.close()
            connection.close()

    @classmethod
    def get_upvote_count(cls, post_ID):
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM reactions WHERE post_ID = %s AND reaction_type = 'upvote'", (post_ID,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return result[0] if result else 0
        return 0

    @classmethod
    def get_downvote_count(cls, post_ID):
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM reactions WHERE post_ID = %s AND reaction_type = 'downvote'", (post_ID,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return result[0] if result else 0
        return 0
