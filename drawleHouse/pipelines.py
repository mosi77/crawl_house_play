# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
from _md5 import md5

import pymysql.cursors
from twisted.enterprise import adbapi

# 将抓取的小说自动入库
class MysqlStoreBookPiperline(object):

    # piperline自动回调调用
    def process_item(self, item, spider):

        self._do_upinsert(item)

        return item

    # 将每行更新或写入数据库中
    def _do_upinsert(self, item):

        try:
            config = {
                'host': 'localhost',
                'port': 3306,
                'user': 'root',
                'password': 'root',
                'db': 'crawl',
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor,
            }
            # 创建连接
            conn = pymysql.connect(**config)

            with conn.cursor() as cursor:
                urlmd5 = self._get_urlmd5id(item['url'])
                cursor.execute(" select 1 from cb_chapter where url_md5 = %s", (urlmd5))
                ret = cursor.fetchone()

                if ret:
                    cursor.execute("""
                                    update cb_chapter set  content = %s where url_md5 = %s
                                """, (item['content'], urlmd5))

                else:
                    cursor.execute("""
                                    INSERT INTO cb_chapter (book_id, chapter_no, chapter_name, words_num, update_time, url, url_md5, content)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                """, (
                        1, 100, item['title'], 0, datetime.datetime.now().replace(microsecond=0).isoformat(' '),
                        item['url'], urlmd5, item['content']))


                # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                conn.commit()

        finally:
            conn.close();




    # url进行md5处理，为避免重复采集设计
    def _get_urlmd5id(self, url):
        return md5(url.encode('utf-8')).hexdigest()

    # 异常处理
    def _handle_error(self, failue, item, spider):
        print(failue)


class InsertDB(object):
    def process_item(self, item, spider):
        # 执行sql语句
        try:
            config = {
                'host': 'localhost',
                'port': 3306,
                'user': 'root',
                'password': 'root',
                'db': 'crawl',
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor,
            }
            # 创建连接
            connection = pymysql.connect(**config)

            with connection.cursor() as cursor:
                # 执行sql语句，插入记录
                sql = 'INSERT INTO cb_chapter (book_id, chapter_no, chapter_name, words_num, update_time, url, content) VALUES (%s, %s, %s, %s, %s, %s, %s)'

                cursor.execute(sql, (1, 100, item['title'], 0, datetime.datetime.now().replace(microsecond=0).isoformat(' '), item['url'], item['content']));
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            connection.commit()

        finally:
            connection.close();

        return item



