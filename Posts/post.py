import mysql.connector
from mysql.connector import Error
import Comments.comment as comm
from Reactions.CommentReactions.commentReaction import CommentReaction


class Post:
    def __init__(self, post_title, post_message, user_id, c_name, post_id=None, image_url=None, comments = None):
        self.post_id = post_id
        self.post_title = post_title
        self.post_message = post_message
        self.user_id = user_id
        self.c_name = c_name
        self.image_url = image_url  # Store image URL/path if available
        self.comments = comments

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
    def create(cls, post_title, post_message, username, c_name, image_url=None):
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO posts (post_title, post_msg, post_user, c_name, image_url) VALUES (%s, %s, %s, %s, %s)",
                (post_title, post_message, username, c_name, image_url)
            )
            connection.commit()
            cursor.close()
            connection.close()

    @classmethod
    def get_all(cls):
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM posts")
            posts = cursor.fetchall()
            cursor.close()
            connection.close()
            return posts
        return []

    
    @classmethod
    def get_by_community(cls,c_name):
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM posts WHERE c_name=%s",[c_name])
            posts = cursor.fetchall()
            cursor.close()
            connection.close()
            for post in posts:
                post['comments'] = comm.Comment.get_comments_by_post(post['postID']) 
                for comment in post['comments']:
                    comment['upvotes'] = CommentReaction.get_upvotes(comment['comment_ID'])
                    comment['downvotes'] = CommentReaction.get_downvotes(comment['comment_ID'])
            return posts
        return []


    @classmethod
    def get_by_id(cls, post_id):
        connection = cls.get_db_connection()
        
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM posts WHERE postID=%s", (post_id,))
            post = cursor.fetchone()
            cursor.close()
            connection.close()
            if post:
                return cls(
                    post_title=post['post_title'],
                    post_message=post['post_msg'],
                    user_id=post['post_user'],
                    c_name=post['c_name'],
                    post_id=post['postID'],
                    image_url=post['image_url'],  # Ensure this is set correctly
                    comments=comm.Comment.get_comments_by_post(post['postID'])
                )
        return None

    @classmethod
    def update(cls, post_id, new_title, new_message, image_url=None):
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE posts SET post_title = %s, post_msg = %s, image_url = %s WHERE postID = %s",
                (new_title, new_message, image_url, post_id)
            )
            connection.commit()
            cursor.close()
            connection.close()

    @classmethod
    def delete(cls, post_id):
        connection = cls.get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM posts WHERE postID = %s", (post_id,))
            connection.commit()
            cursor.close()
            connection.close()
