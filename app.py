"""
A simple 'bubble tea store locations' flask app.
"""
import flask
from flask.views import MethodView
from index import Index
from add import Add
from show import Show
from fun import Fun

app = flask.Flask(__name__)       # our Flask app
app.config['SECRET_KEY'] = '64322'

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/add/',
                 view_func=Add.as_view('add'),
                 methods=['GET', 'POST'])

app.add_url_rule('/show/',
                 view_func=Show.as_view('show'),
                 methods=["GET"])

app.add_url_rule('/fun/',
                 view_func=Fun.as_view('fun'),
                 methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
