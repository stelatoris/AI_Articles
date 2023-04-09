from flask import Flask, request, jsonify, make_response, redirect
import json

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
    articleTimers = []  # <--- here
    for i, article in enumerate(articles):
        time = 0
        try:
            time = int(localStorage.getItem('time-' + i)) or 600
        except:
            pass
            article_list += "<li id='article-" + str(i) + "'><a href='" + article['url'] + "' target='_blank'>" + article['title'] + "</a> <span id='time-" + str(i) + "'>" + str(
                time) + "s</span> <button onclick='startStopTimer(" + str(i) + ")' id='button-" + str(i) + "'>Start Timer</button> <button onclick='removeArticle(" + str(i) + ")'>Remove</button></li>"
    return """
        <html>
            <head>
                <title>Articles about AI and Machine Learning</title>
                <script>
                    var articleTimers = []; // <--- initialization here

                    function setCookie(name, value, days) {
                        var expires = "";
                        if (days) {
                            var date = new Date();
                            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                            expires = "; expires=" + date.toUTCString();
                        }
                        document.cookie = name + "=" + (value || "") + expires + "; path=/; SameSite=None; Secure";
                    }

                    function getCookie(name) {
                        var nameEQ = name + "=";
                        var ca = document.cookie.split(';');
                        for (var i = 0; i < ca.length; i++) {
                            var c = ca[i];
                            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
                            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
                        }
                        return null;
                    }
                    
                    function startStopTimer(index) {
                        var button = document.getElementById('button-' + index);
                        if (button.textContent == 'Start Timer') {
                            console.log('Starting timer for article ' + index);
                            var time = parseInt(localStorage.getItem('time-' + index)) || 600;
                            console.log('Initial time for article ' + index + ': ' + time + 's');
                            var timer = setInterval(function() {
                                time--;
                                console.log('Time left for article ' + index + ': ' + time + 's');
                                document.getElementById('time-' + index).textContent = time + 's';
                                localStorage.setItem('time-' + index, time);
                                if (time == 0) {
                                    clearInterval(timer);
                                    alert('Time is up!');
                                }
                            }, 1000);
                            articleTimers[index] = timer;
                            button.textContent = 'Stop Timer';
                        } else {
                            console.log('Stopping timer for article ' + index);
                            clearInterval(articleTimers[index]);
                            button.textContent = 'Start Timer';
                        }
                    }



                   function removeArticle(index) {
                        console.log('Removing article ' + index);
                        
                        // Remove timer from localStorage
                        localStorage.removeItem('time-' + index);
                        
                        // Remove article from articles array in localStorage
                        var articles = JSON.parse(localStorage.getItem('articles')) || [];
                        articles.splice(index, 1);
                        localStorage.setItem('articles', JSON.stringify(articles));

                        // Remove article from the HTML list
                        var articleList = document.getElementById('article-' + index);
                        articleList.parentNode.removeChild(articleList);

                        // Remove the article from cookies as well
                        var cookieArticles = JSON.parse(getCookie('articles') || '[]');
                        cookieArticles.splice(index, 1);
                        setCookie('articles', JSON.stringify(cookieArticles), 30);

                        // Reload the page
                        location.reload();
                        }

                    function resetTimer() {
                        localStorage.clear();
                        location.reload();
                    }
                </script>
            </head>
            <body>
                <h1>Articles about AI and Machine Learning</h1>
                <ul>
                    """ + article_list + """
                </ul>
                <button onclick="location.href='/add-article'">Add Article</button>
                <button onclick="resetTimer()">Reset Timer</button>
            </body>
        </html>
    """
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

@app.route('/bookmarks')
def bookmarks():
    bookmarks = []
    try:
        with open(r'C:\Users\VRED\AppData\Local\Google\Chrome\User Data\Default\Bookmarks') as f:
            data = json.load(f)
            for item in data['roots']['bookmark_bar']['children']:
                if 'url' in item:
                    bookmarks.append({'title': item['name'], 'url': item['url']})
    except FileNotFoundError:
        print('Chrome bookmarks file not found.')
    return jsonify(bookmarks)


if __name__ == '__main__':
    app.run(debug=True)
