from flask import Flask, render_template
from utils import get_server_time, get_epidemic_situation
from flask import jsonify

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


@app.route('/get_key_info')
def get_key_info():
    data = get_epidemic_situation()
    # print(data)  # (Decimal('84330'), 4642, Decimal('78413'), Decimal('19'))
    # jsonify将字典转换成json字符串
    # print('确诊人数:', data[0], type(data[0]))  # <class 'decimal.Decimal'>
    # print('疑似人数:', data[1], type(data[1]))
    # print('治愈人数:', data[2], type(data[2]))
    # print('死亡人数:', data[3], type(data[3]))
    return jsonify(
        {'confirm_num': data[0], 'suspect_num': data[1], 'heal_num': data[2], 'dead_num': int(data[3])})


if __name__ == '__main__':
    app.debug = True
    app.run()
