import pymysql
import time
import requests
import json
import traceback


def get_server_time():
    '''
    获取服务器时间
    :return:
    '''
    time_str = time.strftime('%Y{}%m{}%d %H:%M:%S')  # 第二个参数没传就使用当前时间戳
    return time_str.format('-', '-')


def get_history_data():
    '''
    获取历史数据
    :return:历史数据
    '''
    # 接口地址
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    # 请求的时候带上请求头，模拟浏览器发送请求
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
    r = requests.get(url, headers)
    # print(r.text)
    ret = json.loads(r.text)
    # print(ret)
    # print(type(data_all),data_all)
    data_all = json.loads(ret['data'])
    # print(type(data_all), data_all)
    # print(data_all['chinaDayList'])
    history_data = {}
    # 每天的总人数
    for chinaDayList_item in data_all['chinaDayList']:
        # print(chinaDayList_item)
        # print(i['date'])
        date = '2020.' + chinaDayList_item['date']
        # print(type(date), date)  # <class 'str'> 2020.04.21
        date = time.strftime('%Y-%m-%d', time.strptime(date, '%Y.%m.%d'))  # 将2020.04.21的时间格式转换成2020-04-21，方便插入到数据库中
        # print(date)
        confirm_num = chinaDayList_item['confirm']  # 获取确诊人数
        # print(confirm_num)
        suspect_num = chinaDayList_item['suspect']  # 获取疑似人数
        dead_num = chinaDayList_item['dead']  # 获取死亡人数
        heal_num = chinaDayList_item['heal']  # 获取治愈人数
        history_data[date] = {'confirm_num': confirm_num, 'suspect_num': suspect_num, 'dead_num': dead_num,
                              'heal_num': heal_num}
    # 每天新增人数
    for chinaDayAddList_item in data_all['chinaDayAddList']:
        # print(chinaDayAddList_item)
        date = '2020.' + chinaDayAddList_item['date']
        # print(type(date), date)  # <class 'str'> 2020.04.21
        date = time.strftime('%Y-%m-%d', time.strptime(date, '%Y.%m.%d'))  # 将2020.04.21的时间格式转换成2020-04-21，方便插入到数据库中
        # print(date)
        confirm_add_num = chinaDayAddList_item['confirm']  # 获取新增确诊人数
        # print(confirm_num)
        suspect_add_num = chinaDayAddList_item['suspect']  # 获取新增疑似人数
        dead_add_num = chinaDayAddList_item['dead']  # 获取新增死亡人数
        heal_add_num = chinaDayAddList_item['heal']  # 获取新增治愈人数
        history_data[date].update(
            {'confirm_add_num': confirm_add_num, 'suspect_add_num': suspect_add_num, 'dead_add_num': dead_add_num,
             'heal_add_num': heal_add_num})
        # print(history_data[date])
    # print(history_data)
    return history_data


def get_detail_data():
    '''
    获取当日详细数据
    :return: 当日详细数据
    '''
    # 接口地址
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
    r = requests.get(url, headers)
    ret = json.loads(r.text)
    data_all = json.loads(ret['data'])
    # print(data_all)
    lastUpdateTime = data_all['lastUpdateTime']
    # print(lastUpdateTime)
    contries_data = data_all['areaTree']
    # print(contry_data)
    # print(type(contries_data), len(contries_data))  # <class 'list'> 1
    prinvices_data = contries_data[0]['children']
    # print(prinvices_data)
    detail_data = []
    for prinvices_data_item in prinvices_data:
        # print(prinvices_data_item)
        province_name = prinvices_data_item['name']
        # print(province_name)
        for citis_data in prinvices_data_item['children']:
            # print(citis_data)
            city_name = citis_data['name']
            city_confirm_num = citis_data['total']['confirm']
            suspect_num = citis_data['total']['suspect']
            heal = citis_data['total']['heal']
            city_add_num = citis_data['today']['confirm']
            detail_data.append(
                [lastUpdateTime, province_name, city_name, city_confirm_num, suspect_num, heal, city_add_num])
    return detail_data  # list


def insert_history_data():
    '''
    插入疫情历史数据
    :return:None
    '''
    conn = None
    cursor = None
    try:
        # print(get_tencent_history_data())
        dic = get_history_data()
        # print(dic)#{'2020-01-13': {'confirm_num': 41, 'suspect_num': 0, 'dead_num': 1, 'heal_num': 0}……}
        print(f'{time.asctime()} 开始插入疫情历史数据')  # 开始更新的时间
        conn, cursor = get_conn()
        sql = 'insert into history_data values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        for k, v in dic.items():
            # print(key, value)  # 2020-01-13 {'confirm_num': 41, 'suspect_num': 0, 'dead_num': 1, 'heal_num': 0}
            cursor.execute(sql, [k, v.get('confirm_num'), v.get('suspect_num'), v.get('dead_num'),
                                 v.get('heal_num'), v.get('confirm_add_num'), v.get('suspect_add_num'),
                                 v.get('dead_add_num'), v.get('heal_add_num')])
        conn.commit()
        print(f'{time.asctime()} 插入疫情历史数据完毕')  # 开始更新的时间
    except:
        traceback.print_exc()
    finally:
        cloe_conn(conn, cursor)


def update_history_data():
    '''
       更新疫情历史数据
       :return:None
       '''
    conn = None
    cursor = None
    try:
        # print(get_tencent_history_data())
        dic = get_history_data()
        # print(dic)#{'2020-01-13': {'confirm_num': 41, 'suspect_num': 0, 'dead_num': 1, 'heal_num': 0}……}
        print(f'{time.asctime()} 开始更新疫情历史数据')  # 开始更新的时间
        conn, cursor = get_conn()
        sql = 'insert into history_data values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_query = 'select confirm_num from history_data where date=%s'
        # '2020-01-13可以和2020-01-13 00:00:00等价'
        for k, v in dic.items():
            # print(k, v)  # 2020-01-13 {'confirm_num': 41, 'suspect_num': 0, 'dead_num': 1, 'heal_num': 0}
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [k, v.get('confirm_num'), v.get('suspect_num'), v.get('dead_num'),
                                     v.get('heal_num'), v.get('confirm_add_num'), v.get('suspect_add_num'),
                                     v.get('dead_add_num'), v.get('heal_add_num')])
            else:
                print(f'{time.asctime()} 已经是最新疫情历史数据')
        conn.commit()
        print(f'{time.asctime()} 疫情历史数据更新完毕')  # 开始更新的时间
    except:
        traceback.print_exc()
    finally:
        cloe_conn(conn, cursor)


def update_detail_data():
    '''
    更新当日疫情详细数据
    :return:None
    '''
    conn = None
    cursor = None
    try:
        lst = get_detail_data()
        # print(dic)
        last_update_time = lst[0][0]
        # print(last_update_time)
        # print(f'{time.asctime()}')  # 开始更新的时间
        print(f'{time.asctime()} 开始更新当日疫情最新详细数据')  # 开始更新的时间
        conn, cursor = get_conn()
        sql = 'insert into detail_data(lastUpdateTime,province_name,city_name,confirm_num,confirm_add_num,heal_num,dead_num) values (%s,%s,%s,%s,%s,%s,%s)'
        sql_query = 'select %s=(select lastUpdateTime from detail_data order by id desc limit 1)'
        cursor.execute(sql_query, last_update_time)
        # print(cursor.fetchone()[0])
        if not cursor.fetchone()[0]:
            for item in lst:
                # print(item)
                cursor.execute(sql, item)
            conn.commit()  # 提交事务，update、delete、inssert
            print(f'{time.asctime()} 已完成当日疫情最新详细数据的更新')  # 开始更新的时间
        else:
            print(f'{time.asctime()} 已经是当日疫情最新详细数据的更新')
    except:
        traceback.print_exc()  # 追踪异常的方法，把发生异常的调用堆信息打印出来
    finally:
        cloe_conn(conn, cursor)


def get_conn():
    '''
    连接数据库
    :return: conn，cursor
    '''
    # 建立连接
    conn = pymysql.connect(user='root', password='123456', database='epidemic_situation')
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor


def cloe_conn(cursor, conn):
    '''
    关闭数据库连接
    :param conn: 连接
    :param cursor: 游标
    :return: None
    '''
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql, *args):
    '''
    封装通用的查询
    :param sql:sql语句
    :param args:参数
    :return:查询的结果
    '''
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    ret = cursor.fetchall()  # 拿到所有数据
    cloe_conn(cursor, conn)
    return ret


def get_epidemic_situation():
    '''
    获取疫情关键信息
    :return:
    '''
    sql = 'select sum(confirm_num) as confirm_sum,(select suspect_num from history_data order by date desc limit 1) as suspect_sum,sum(heal_num) as heal_sum,sum(dead_num) as dead_sum from detail_data where lastUpdateTime=(select lastUpdateTime from detail_data order by lastUpdateTime desc limit 1);'
    ret = query(sql)
    # print(ret)
    return ret[0]


def get_host_search():
    from selenium.webdriver import Chrome, ChromeOptions
    # google chrome的无头模式，即不打开浏览器，后台自动加载数据，可以大幅度提高爬虫效率，
    option = ChromeOptions()
    option.add_argument('--headless')  # 一藏浏览器，可以大幅度提高爬虫效率
    option.add_argument('--no-sandbox')  # 部署的时候linux还会要求参数，需要禁用sandbox
    broswer = Chrome('driver_file/chromedriver', options=option)
    url = 'https://voice.baidu.com/act/virussearch/virussearch/'
    broswer.get(url)
    # print(broswer.page_source)
    more = broswer.find_element_by_css_selector(
        '#ptab-0 > div > div.VirusHot_1-5-6_32AY4F.VirusHot_1-5-6_2RnRvg > section > div')
    # print(more)
    more.click()
    # more.click()  # 点击展开
    time.sleep(1)  # 等待一定时间
    data_lst = broswer.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[1]/section/a/div/span[2]')  # list
    # for item in lst:
    #   print(item.text)
    # print(data_lst)
    context = [item.text for item in data_lst]  # 在关闭浏览器之前获取，否则报session失效
    broswer.close()  # 关闭浏览器
    # print(context)
    return context


def storage_host_search():
    conn = None
    cursor = None
    try:
        context = get_host_search()
        # print(context)
        print(f'{time.asctime()} 开始向数据库中插入今日疫情热搜数据')
        conn, cursor = get_conn()
        sql = 'insert host_search(dt,content) values(%s,%s)'
        # print(context)
        dt = time.strftime('%Y-%m-%d %X')
        # print(dt)
        for item in context:
            cursor.execute(sql, (dt, item))
        conn.commit()
        print(f'{time.asctime()} 已完成向数据库中插入今日疫情热搜数据')
    except:
        traceback.print_exc()
    finally:
        cloe_conn(conn, cursor)


if __name__ == '__main__':
    pass
    # get_host_search()
    # get_epidemic_situation()
    storage_host_search()
