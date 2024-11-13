import Communities.community as comm
from flask import render_template, Flask

app = Flask(__name__)

@app.route('/')
def create():
    return render_template('createcommunity.html')

@app.route('/create-community', methods = ["POST"])
def create_community():
    print("i got here")
    x = comm.community("desc", "abc", "me")
    y = x.Create()
    return render_template('listofcommunities.html')

if __name__ == '__main__':
    app.run(debug=True)