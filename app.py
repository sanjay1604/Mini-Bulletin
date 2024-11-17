import Communities.community as comm
from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory
from posts.post import Post
from reactions.reaction import PostReaction
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

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
def create():
    return render_template('createcommunity.html')

@app.route('/create-community', methods = ["POST"])
def create_community():
    print("i got here")
    x = comm.community("desc", "abc", "me")
    y = x.Create()
    return render_template('listofcommunities.html')
@app.route('/create-post', methods=["GET", "POST"])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        user_id = 1  
        community_id = 1  
        
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
        Post.create(title, message, user_id, community_id, image_url)
        
        return redirect(url_for('list_posts'))  
    
    return render_template('createpost.html')


@app.route('/update-post/<int:post_id>', methods=["GET", "POST"])
def update_post(post_id):
    post = Post.get_by_id(post_id)
    if not post:
        return redirect(url_for('list_posts'))  

    # Handle the POST request for updating the post
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
        return redirect(url_for('list_posts'))  

    return render_template('updatepost.html', post=post)

@app.route('/delete-post/<int:post_id>', methods=["POST"])
def delete_post(post_id):
    post = Post.get_by_id(post_id)
    if post:
        Post.delete(post_id)
    return redirect(url_for('list_posts'))  

@app.route('/list-posts', methods=["GET"])
def list_posts():
    posts = Post.get_all()  
    for post in posts:
        # Get upvote and downvote counts for each post using dictionary keys
        post['upvotes'] = PostReaction.get_upvote_count(post['postID'])
        post['downvotes'] = PostReaction.get_downvote_count(post['postID'])
    return render_template('listofposts.html', posts=posts)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/uploads', filename)

@app.route('/react-upvote/<int:post_id>', methods=["POST"])
def react_upvote(post_id):
    user_id = 1  
    PostReaction.upvote(post_id, user_id)
    return redirect(url_for('list_posts'))  

@app.route('/react-downvote/<int:post_id>', methods=["POST"])
def react_downvote(post_id):
    user_id = 1  
    PostReaction.downvote(post_id, user_id)
    return redirect(url_for('list_posts'))  

@app.route('/remove-reaction/<int:post_id>', methods=["POST"])
def remove_reaction(post_id):
    user_id = 1  
    PostReaction.remove_reaction(post_id, user_id)
    return redirect(url_for('list_posts'))  

if __name__ == '__main__':
    app.run(debug=True)
