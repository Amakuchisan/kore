from base64 import b64encode
from flask import Flask, render_template, request, redirect, url_for
import io
from PIL import Image
import sys
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy.sql import text

sys.path.append('/work/src')
from bookmark import Bookmark

from setting import session
import wc
import word

sys.path.append('/work/src/model')
from user import *


app = Flask(__name__, template_folder='/work/templates')

output = io.BytesIO()
wc.create_wordcloud('').save(output, format='PNG')
sample_image = b64encode(output.getvalue()).decode("utf-8")
image = sample_image

bookmark = Bookmark()
hatena_id=""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        entries = bookmark.get_hotentry(hatena_id, "it")
        return render_template("index.html", hatena_id = hatena_id, entries = entries, image=image)
    
    elif request.method == 'POST':
        update_wordcloud()
        return redirect(url_for('index'))

@app.route('/id', methods=['POST'])
def id():
    if request.method == 'POST':
        global hatena_id
        global image
        hatena_id = request.form["user_id"]
        img = find_wordcloud(hatena_id)
        if (img is None):
            image = sample_image
        else:
            image = img.decode("utf-8")

    return redirect(url_for('index'))

@app.route('/recommended', methods=['POST'])
def recommended():
    if request.method == 'POST':
        bookmark.init(hatena_id)
        bookmark.get_osusume(hatena_id)
    return redirect(url_for('index'))

def update_wordcloud():
    global image
    global output
    titles = bookmark.get_title(hatena_id)
    output = io.BytesIO()
    wc.create_wordcloud(word.get_noun(' '.join(titles))).save(output, format='PNG')
    image = b64encode(output.getvalue()).decode("utf-8")
    save(b64encode(output.getvalue()))

def save(image):
    if find_wordcloud(hatena_id) is None:
        user = User()
        user.hatena_id = hatena_id
        user.wordcloud = image
        session.add(user)
        session.commit()
        return
    user = session.query(User).filter(User.hatena_id==hatena_id).first()
    user.wordcloud = image
    session.commit()

def find_wordcloud(hatena_id: str):
    user = session.query(User.wordcloud).filter(User.hatena_id==hatena_id).first()
    if user is not None:
        return user.wordcloud
    return None

if __name__ == "__main__":
    app.run(debug=True)
