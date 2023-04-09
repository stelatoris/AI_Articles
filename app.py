from flask import Flask, request, jsonify, make_response, redirect, render_template

import os
import sqlite3
import json


import my_chrome_bookmarks

def getBookmarks():
    bookmarks = []
    try:
        bookmark_file_path = 'C:/Users/VRED/AppData/Local/Google/Chrome/User Data/Default/Bookmarks'
        if not os.path.exists(bookmark_file_path):
            print('Chrome bookmarks file not found.')
            return bookmarks

        with open(bookmark_file_path) as f:
            data = json.load(f)
            for item in data['roots']['bookmark_bar']['children']:
                if 'url' in item:
                    title = item.get('name', 'No Title')  # Default to 'No Title' if title field is not present
                    url = item['url']
                    bookmarks.append({'title': title, 'url': url})

    except Exception as e:
        print(f'Error: {e}')

    print(bookmarks)  # Print the bookmarks to see if title field is extracted correctly
    return bookmarks



app = Flask(__name__)


@app.route('/')
def index():
    return """
        <html>
            <head>
                <title>Homepage</title>
            </head>
            <body>
                <h1>Welcome to the AI and Machine Learning News Reader!</h1>
                <p>Click on the Articles link to start reading!</p>
                <button onclick="location.href='/articles'">Articles</button>
                <button onclick="location.href='/add-article'">Add Article</button>
            </body>
        </html>
    """

@app.route('/articles')
def articles():
    articles = json.loads(request.cookies.get('articles', '[]'))
    article_list = ""
    articleTimers = []
    for i, article in enumerate(articles):
        time = 0
        try:
            time = int(localStorage.getItem('time-' + i)) or 600
        except:
            pass

        article_list += "<li id='article-" + str(i) + "'><a href='" + article['url'] + "' target='_blank'>" + article['title'] + "</a> <span id='time-" + str(i) + "'>" + str(time) + "s</span> <button onclick='startStopTimer(" + str(i) + ")' id='button-" + str(i) + "'>Start Timer</button> <button onclick='removeArticle(" + str(i) + ")'>Remove</button></li>"

    # Get bookmarks
    bookmarks = getBookmarks()

    return render_template('articles.html', articles=article_list, bookmarks=bookmarks)



@app.route('/update-articles', methods=['POST'])
def update_articles():
    articles = request.json
    response = make_response()
    response.set_cookie('articles', json.dumps(articles))
    return response


@app.route('/add-article')
def add_article():
    return """
        <html>
            <head>
                <title>Add Article</title>
            </head>
            <body>
                <h1>Add Article</h1>
                <form method="post" action="/save-article">
                    <label for="url">Web Address:</label>
                    <input type="text" id="url" name="url"><br><br>
                    <label for="title">Title:</label>
                    <input type="text" id="title" name="title"><br><br>
                    <input type="submit" value="Save">
                </form>
            </body>
        </html>
    """


@app.route('/save-article', methods=['POST'])
def save_article():
    url = request.form['url']
    title = request.form['title']
    articles = json.loads(request.cookies.get('articles', '[]'))
    articles.append({'url': url, 'title': title, 'read': False, 'time': 0})
    response = make_response(redirect('/articles'))
    response.set_cookie('articles', json.dumps(articles))
    return response


@app.route('/remove-article')
def remove_article():
    index = int(request.args.get('index'))
    articles = json.loads(request.cookies.get('articles', '[]'))
    del articles[index]
    response = make_response(redirect('/articles'))
    response.set_cookie('articles', json.dumps(articles))
    return response


if __name__ == '__main__':
    app.run(debug=True)
