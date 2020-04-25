from flask import Flask, render_template
from utils.get_server_time import get_server_time

app = Flask(__name__)

'''
@app.route('/')
def hello_world():
    return 'Hello World!'
'''


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/get_time')
def get_time():
    return get_server_time()


if __name__ == '__main__':
    app.debug = True
    app.run()
