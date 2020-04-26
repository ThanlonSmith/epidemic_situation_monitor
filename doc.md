>@[toc]
>**Tip：项目是跟网上老师学习，然后自己实践总结的!!!**
##### 1. 项目概述
项目基于Python语言、Python的Flask框架和Echarts来做的，涉及的技术有Python网络爬虫；Python与MySQL数据库的交互；Flask框架构建Web项目；Echarts数据可视化显示；Linux部署web项目以及爬虫。
##### 2. 数据获取
###### 2.1 爬取并处理腾讯疫情数据
目标站点分析，需要确定数据接口地址：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200424153257627.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoYW5sb24=,size_16,color_FFFFFF,t_70)
获取历史数据和当日详细数据：

<kbd>get_tencent_data.py：</kbd>

```py
import requests
import json
import time


def get_tencent_history_data():
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


def get_tencent_detail_data():
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


if __name__ == '__main__':
    print(get_tencent_history_data())
    # print(get_tencent_detail_data())
```
###### 2.2 selnium爬取百度热搜
目标站点分析，爬取的是“今日疫情热搜”：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200424204747389.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoYW5sb24=,size_16,color_FFFFFF,t_70)

百度的数据页面使用的是动态渲染技术，`使用普通的请求方式是获取不到数据的`：
```py
# 使用普通的爬取方式
url = 'https://voice.baidu.com/act/virussearch/virussearch/'
ret = requests.get(url)
print(ret.text)
```
`没有爬取我们想要的数据：`
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200427020347792.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoYW5sb24=,size_16,color_FFFFFF,t_70)
但是可以使用selenium模块来爬取，selenium是一个用于web程序测试的工具，直接运行在浏览器上，就如真正的用户在操作一样。安装selenium模块：`pip install selenium -i https://mirrors.aliyun.com/pypi/simple`。此外还需要下载安装浏览器和下载浏览器对应版本的驱动，因为selenium是模拟浏览器工作的。我这里使用的是chrome浏览器，驱动的下载地址是：[http://npm.taobao.org/mirrors/chromedriver/](http://npm.taobao.org/mirrors/chromedriver/)。selenium的基本使用：**① 创建浏览器对象；② 浏览器对象.get()方法向url地址发起请求；③ 利用浏览器打开的地址使用浏览器.find方法查找资源。**
```py
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
    lst = broswer.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[1]/section/a/div/span[2]')  # list
    for item in lst:
        print(item.text)
    broswer.close()  # 关闭浏览器

 if __name__ == '__main__':
    get_host_search()
```
`爬取的结果：`
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200427024545236.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoYW5sb24=,size_16,color_FFFFFF,t_70)
##### 3. 数据持久化
###### 3.1 疫情数据的持久化
mysql数据库操作：
```sql
# 创建数据库
mysql> create database epidemic_situation default charset utf8;
# 切换到这个数据库
mysql> use epidemic_situation
#创建历史数据表
CREATE TABLE history_data
(
date DATE COMMENT '日期',
confirm_num INT(11) DEFAULT NULL COMMENT '累积确诊人数',
confirm_add_num INT(11) DEFAULT NULL COMMENT '当日新增确诊人数',
suspect_num INT(11) DEFAULT NULL COMMENT '剩余的疑似人数',
suspect_add_num INT(11) DEFAULT NULL COMMENT '当日新增疑似人数',
heal_num INT(11) DEFAULT NULL COMMENT '累积治愈人数',
heal_add_num INT(11) DEFAULT NULL COMMENT '当日新增治愈人数',
dead_num INT(11) DEFAULT NULL COMMENT '累积死亡人数',
dead_add_num INT(11) DEFAULT NULL COMMENT '当日新增死亡人数',
PRIMARY KEY(date) USING BTREE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
#创建历史数据表
CREATE TABLE detail_data
(
id INT(11) AUTO_INCREMENT COMMENT 'id',
lastUpdateTime datetime DEFAULT NULL COMMENT '数据最后更新的时间',
province_name varchar(20) DEFAULT NULL COMMENT '省的名称',
city_name varchar(20) DEFAULT NULL COMMENT '市的名称',
confirm_num INT(11) DEFAULT NULL COMMENT '累积确诊人数',
confirm_add_num INT(11) DEFAULT NULL COMMENT '当日新增确诊人数',
heal_num INT(11) DEFAULT NULL COMMENT '累积治愈人数',
dead_num INT(11) DEFAULT NULL COMMENT '累积死亡人数',
PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
持久化到数据库，首先安装pymysql模块：**`pip install pymysql -i https://mirrors.aliyun.com/pypi/simple`**

持久化到数据库的业务逻辑：

<kbd>store_tencent_data.py：</kbd>
```py
import pymysql
import time
from .get_tencent_data import get_tencent_history_data
from .get_tencent_data import get_tencent_detail_data
import traceback


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


def cloe_conn(conn, cursor):
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


def insert_history_data():
    '''
    插入疫情历史数据
    :return:None
    '''
    conn = None
    cursor = None
    try:
        # print(get_tencent_history_data())
        dic = get_tencent_history_data()
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
        dic = get_tencent_history_data()
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
        lst = get_tencent_detail_data()
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


if __name__ == '__main__':
    insert_history_data()
    update_history_data()
    update_detail_data()
```
###### 3.2 百度热搜数据的持久化

##### 4. web开发与可视化
###### 4.1 可视化大屏模板设计
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200425140815148.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoYW5sb24=,size_16,color_FFFFFF,t_70)
>**项目源代码在文章的最下面，仅供参考!!!**

###### 4.2 时间的实时更新
获取服务器时间的后台逻辑：

<kbd>get_server_time.py：</kbd>
```py
import time


def get_server_time():
    time_str = time.strftime('%Y{}%m{}%d %H:%M:%S')  # 第二个参数没传就使用当前时间戳
    return time_str.format('-', '-')


if __name__ == '__main__':
    print(get_server_time(), type(get_server_time()))  # 2020-04-26 01:04:44 <class 'str'>
```
<kbd>app.py：</kbd>
```py
@app.route('/get_time')
def get_time():
    return get_server_time()
```
前台ajax请求服务器时间逻辑：

<kbd>get_time.js：</kbd>
```js
function get_time() {
    $.ajax({
        url: "/get_time",
        timeout: 10000,//超时时间设置为10秒
        success: function (data) {
            $('#time').html(data);
        }, error: function (xhr, type, errorThrown) {

        }
    })
}

setInterval(get_time, 1000);
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200426014830961.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoYW5sb24=,size_16,color_FFFFFF,t_70)
###### 4.3 疫情概况的实现

###### 4.4 全国疫情地图的实现

###### 4.5 全国累积与新增趋势的实现

###### 4.6 

###### 4.7 今日热搜的实现

##### 5. 项目部署
###### 5.1 部署流程
###### 5.2 定时调度爬虫
>**Github：[https://github.com/ThanlonSmith/epidemic_situation_monitor](https://github.com/ThanlonSmith/epidemic_situation_monitor)**