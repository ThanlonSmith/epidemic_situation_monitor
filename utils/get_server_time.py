import time


def get_server_time():
    time_str = time.strftime('%Y{}%m{}%d %H:%M:%S')  # 第二个参数没传就使用当前时间戳
    return time_str.format('-', '-')


if __name__ == '__main__':
    print(get_server_time(), type(get_server_time()))  # 2020-04-26 01:04:44 <class 'str'>
