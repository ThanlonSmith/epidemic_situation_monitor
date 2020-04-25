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
