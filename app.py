import Communities.community as comm
import Communities.communityDB as comdb
import Users.users as user
import Users.userdb as userdb
from Posts.post import Post
from Reactions.PostReactions.reaction import PostReaction
from Reactions.CommentReactions.commentReaction import CommentReaction
from Comments.comment import Comment
import os
from werkzeug.utils import secure_filename
from flask import render_template, Flask, request, redirect, session, url_for
from flask_session import Session
from flask import send_from_directory

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Configure the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/createuserform')
def createuserform():
    return render_template('createuser.html')

@app.route('/user-login', methods=["POST"])
def user_login():
    username = request.form['userName']
    password = request.form['password']
    x = user.users()
    result = x.login(username, password)

    if result:
        session['username'] = username
        return render_template('welcome.html',users=username)
    else:
        return login()
    
@app.route('/homepage',methods=["POST"])
def welcome():
    if 'username' in session:
        username = session['username']
        return render_template('welcome.html',users=username)

@app.route('/viewcommunities', methods=["POST"])
def view_communities():
    if 'username' in session:
        username = session['username']
        x = comm.community()
        result = x.listOne(username)
        return render_template('viewcommunities.html', communities=result)
    else:
        return render_template('welcome.html', users=username)

@app.route('/toviewcommunities', methods=["POST"])
def view_all_communities():
    if 'username' in session:
        username = session['username']
        x=comm.community()
        result = x.ListAll(username)
        return render_template('listofcommunities.html', communities=result, users=username)
    else:
       return render_template('login.html') 

@app.route('/logout', methods=["POST"])
def logout():
    if 'username' in session:
        username = session['username']
        return render_template('login.html')

@app.route('/createuser', methods=["POST"])
def create_user():
        username = request.form['userName']
        password = request.form['password']
        x = user.users()
        x.setProperties(username,password)
        y = x.create_user()
        return redirect('/')


@app.route('/tocreatecommunity', methods=["POST"])
def toCreateCommunity():
    return render_template('createcommunity.html')

@app.route('/tocreatepost',methods=["POST"])
def tocreatepost():
    communityName = request.form['communityName']
    return render_template('createpost.html',community=communityName)

@app.route('/toviewposts/<communityName>', methods=["GET"])
def view_community_posts(communityName):
    if 'username' in session:
        username = session['username']
        return view_community_posts_by_community_name(communityName,username)
    else:
        return render_template('welcome.html', users=username)

def view_community_posts_by_community_name(communityName,username):
    posts = Post.get_by_community(communityName)
    for post in posts:
        post['upvotes'] = PostReaction.get_upvote_count(post['postID'])
        post['downvotes'] = PostReaction.get_downvote_count(post['postID'])
    return render_template('listofposts.html', posts=posts, community=communityName, username=username)

    
@app.route('/create-post', methods=["GET","POST"])
def create_post():
    if 'username' in session:
        username = session['username']
        community = request.form['communityName']
        title = request.form['title']
        message = request.form['message']
        user_id = username         # replace with real logged-in username
        c_name = community    # replace with real c_name
        
        # Handle the image upload
        image_url = None
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                image_url = filename
                
        # Create the post
        Post.create(title, message, user_id, c_name, image_url)
        return redirect("/toviewposts/"+community)


@app.route('/update-post/<int:post_id>', methods=["GET", "POST"])
def update_post(post_id):
    if 'username' in session:
        username = session['username']
        post = Post.get_by_id(post_id)
        community = post.c_name
        if not post:
            return redirect(url_for('list_posts'))  

        # Handle the POST request for updating the post
        x = comm.community()
        admin = x.adminSeek(username)
        if username == admin or username == post.user_id:
            if request.method == 'POST':
                new_title = request.form['new_title']
                new_message = request.form['new_message']
                
                # Handle image upload for update
                image_url = post.image_url  
                if 'image' in request.files:
                    image = request.files['image']
                    if image and allowed_file(image.filename):
                        filename = secure_filename(image.filename)
                        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        image.save(image_path)
                        image_url = filename  

                    Post.update(post_id, new_title, new_message, image_url)
                    post = Post.get_by_id(post_id)
            return render_template('updatepost.html', post=post,community=community)
        return redirect("/toviewposts/"+post.c_name)

 

@app.route('/delete-post/<int:post_id>', methods=["POST"])
def delete_post(post_id):
    if 'username' in session:
        username = session['username']
        post = Post.get_by_id(post_id)
        x = comm.community()
        admin = x.adminSeek(username)
        if post:
            if username == admin or username == post.user_id:
                Post.delete(post_id)
            return redirect("/toviewposts/"+post.c_name)

@app.route('/list-posts', methods=["GET"])
def list_posts():
    if 'username' in session:
        username = session['username']
        posts = Post.get_all()  
        for post in posts:
            # Get upvote and downvote counts for each post using dictionary keys
            post['upvotes'] = PostReaction.get_upvote_count(post['postID'])
            post['downvotes'] = PostReaction.get_downvote_count(post['postID'])
        
        return render_template('listofposts.html', posts=posts,username=username)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/uploads', filename)

@app.route('/react-upvote/<int:post_id>', methods=["POST"])
def react_upvote(post_id):
    if 'username' in session:
        username = session['username']
        user_id =  username              
        PostReaction.upvote(post_id, user_id)
        post = Post.get_by_id(post_id)
        return redirect("/toviewposts/"+post.c_name)

@app.route('/react-downvote/<int:post_id>', methods=["POST"])
def react_downvote(post_id):
    if 'username' in session:
        username = session['username']
        user_id = username                
        PostReaction.downvote(post_id, user_id)
        post = Post.get_by_id(post_id)
        return redirect("/toviewposts/"+post.c_name)

@app.route('/remove-reaction/<int:post_id>', methods=["POST"])
def remove_reaction(post_id):
    if 'username' in session:
        username = session['username']
        user_id = username                 
        PostReaction.remove_reaction(post_id, user_id)
        post = Post.get_by_id(post_id)
        return redirect("/toviewposts/"+post.c_name) 

@app.route('/create-community', methods = ["POST"])
def create_community():
    if 'username' in session:
        username = session['username']
        communityName = request.form['communityName']
        communityDesc = request.form['communityDesc']
        username = session['username']
        x = comm.community()
        x.SetProperties(communityDesc,communityName, username)

        y = x.Create()
        z = x.join(communityName,username)

        return render_template('welcome.html',users=username)

@app.route('/join_community',methods=["POST"])
def join_community():
    if 'username' in session:
        username = session['username']
        communityName = request.form['communityName']
        x=comm.community()
        out=x.join(communityName,username) 
        return render_template('welcome.html',users=username)

@app.route('/exit_community',methods=["POST"])
def exit_community():
    if 'username' in session:
        username = session['username']
        communityName = request.form['communityName']
        x=comm.community()
        out=x.Exit(communityName,username)
        return render_template('welcome.html',users=username)

@app.route('/deleteCommunity', methods=["POST"])
def delete_community():
    if 'username' in session:
        username = session['username']
        communityName = request.form['communityName']
        x = comm.community()
        out = x.Delete(communityName)
        return render_template('welcome.html',users=username)

@app.route('/renderForUpdate',methods=["POST"])
def renderForUpdate():
    communityName = request.form['communityName']
    x = comm.community()
    cObj = x.Get(communityName)
    return render_template('updatecommunity.html',community=cObj)

@app.route('/updateCommunity',methods=["POST"])
def update_community():
    communityName = request.form['communityName']
    communityDesc = request.form['communityDesc']
    x = comm.community()
    x.Update(communityName, communityDesc)
    return redirect("/toviewposts/"+communityName)

@app.route('/add-comment/<int:post_id>', methods=["POST"])
def add_comment(post_id):
    if 'username' in session:
        username = session['username']
    if request.method == "POST":
        comment_message = request.form['comment_message']
        commenting_user = username  # Replace with real logged-in username
        
        Comment.add_comment(commenting_user, comment_message, post_id)
        post = Post.get_by_id(post_id)
        return redirect("/toviewposts/"+post.c_name) 

@app.route('/delete-comment/<int:comment_id>', methods=["POST"])
def delete_comment(comment_id):
    if 'username' in session:
        username = session['username']
        comment = Comment.get_by_id(comment_id)
        x = comm.community()
        admin = x.adminSeek(username)
        if comment and (comment['commenting_user'] == username or admin==username): 
            Comment.delete_comment(comment_id)
        
        post = Post.get_by_id(comment['post_ID'])
        return redirect("/toviewposts/"+post.c_name)
    else:
        return redirect(url_for('login'))

    
@app.route('/react-comment-upvote/<int:comment_id>', methods=["POST"])
def react_comment_upvote(comment_id):
    if 'username' in session:
        username = session["username"]
        user_id = username  # Replace with real logged-in username
        CommentReaction.add_reaction(comment_id, user_id, 'upvote')
        comment = Comment.get_by_id(comment_id)
        post = Post.get_by_id(comment['post_ID'])
        return redirect("/toviewposts/"+post.c_name)  

@app.route('/react-comment-downvote/<int:comment_id>', methods=["POST"])
def react_comment_downvote(comment_id):
    if 'username' in session:
        username = session["username"]
        user_id = username  # Replace with real logged-in username
        CommentReaction.add_reaction(comment_id, user_id, 'downvote')
        comment = Comment.get_by_id(comment_id)
        post = Post.get_by_id(comment['post_ID'])
        return redirect("/toviewposts/"+post.c_name)   

@app.route('/remove-comment-reaction/<int:comment_id>', methods=["POST"])
def remove_comment_reaction(comment_id):
    if 'username' in session:
        username = session["username"]
        user_id = username  
        CommentReaction.remove_reaction(comment_id, user_id)
        comment = Comment.get_by_id(comment_id)
        post = Post.get_by_id(comment['post_ID'])
        return redirect("/toviewposts/"+post.c_name)  
    
#render_template('listofcommunities.html')
    
if __name__ == '__main__':
    app.run(debug=True)
