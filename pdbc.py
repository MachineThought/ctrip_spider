# -*- coding: utf-8 -*-

import pymysql


class PDBC:
    def __init__(self):
        self.db_url = "192.168.1.11"
        self.db_username = "root"
        self.db_pass = "root"
        self.db_database = "ctrip"
        self.db = pymysql.connect(host=self.db_url, port=3306, user=self.db_username, passwd=self.db_pass, db=self.db_database)
        self.db.set_charset("utf8")
        self.cursor = self.db.cursor()
        self.cursor.execute('SET character_set_connection=utf8;')

    # 获取当前数据库中指定 column 值最大的数
    def get_bigger_column(self, table_name, column):
        max_index = 0
        sql = "select max(%s) from %s" % (column, table_name)
        try:
            self.cursor.execute(sql)
            for row in self.cursor.fetchall():
                max_index = row[0]
            if max_index is None:
                max_index = 1
            else:
                max_index = max_index + 1
        except:
            print("查询最大数出错")

        return max_index

    # 获取当前表中最大的id并返回 +1 后的值
    def get_bigger_id(self, table_name):
        return self.get_bigger_column(table_name, "id")

    # 添加所有目的地城市
    def insert_dest(self, dest_data):
        result = []
        for city in dest_data:
            index = int(self.get_bigger_id("dest_city"))
            sql = "insert into dest_city(id,city_name,city_url) values(%d,'%s','%s')" % (index, city["cityName"], city["cityUrl"])
            print(sql)
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except Exception as err:
                self.db.rollback()
                print(err)
        return result
