import requests
import json
import time


def get_tencent_data_history():
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


def get_tencent_data_today():
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
    return detail_data


print(get_tencent_data_history())
print(get_tencent_data_today())
