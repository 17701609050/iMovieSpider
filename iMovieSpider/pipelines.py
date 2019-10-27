# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
import sys


class ImoviespiderPipeline(object):

    def process_item(self, item, spider):
        return item


class MySQLPipeline(object):
    def __init__(self):
        # 链接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,         # 数据库端口
            db='iblog',        # 数据库名称
            user='root',       # 数据库用户名
            passwd='root',     # 数据库密码
            charset='utf8',    # 数据库编码
            use_unicode=True
        )
        # 拿到操作数据库的游标
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        print(item)
        moviename = item.get('moviename', '')
        translation_name = item.get('translation_name', '')
        chinese_movie_name = item.get('chinese_movie_name', '')
        doubanscore = item.get('doubanscore', '')
        doubancounter = item.get('doubancounter', 0)
        imdbscore = item.get('imdbscore', '')
        imdbcounter = item.get('imdbcounter', 0)
        style = item.get('style', '')
        country = item.get('country', '')
        language = item.get('language', '')
        dateyear = item.get('dateyear', '')
        movie_length = item.get('movie_length', '')
        director = item.get('director', '')
        actor = item.get('actor', '')#.replace("'", ' ').replace('ô', ' ')
        aboutmovie = item.get('aboutmovie', '')
        downloadlink = item.get('downloadlink', '')
        movie_head_pic = item.get('movie_head_pic', '')
        movie_detail_pic = item.get('movie_detail_pic', '')
        dyttsearch = item.get('dyttsearch', '')
        sql = '''
            insert into movie_movie(moviename, translation_name, doubanscore, doubancounter, imdbscore, 
            imdbcounter, style, country, `language`, dateyear, movie_length, director, actor, aboutmovie, downloadlink, 
            movie_head_pic, movie_detail_pic, dyttsearch, chinese_movie_name)
            VALUE ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', 
            '{14}', '{15}', '{16}', '{17}', '{18}')'''.format(pymysql.escape_string(moviename),
                                                              pymysql.escape_string(translation_name),
                                                              doubanscore, doubancounter,
                                                              imdbscore, imdbcounter, style,
                                                              country, language, dateyear,
                                                              movie_length, pymysql.escape_string(director),
                                                              pymysql.escape_string(actor),
                                                              pymysql.escape_string(aboutmovie), downloadlink,
                                                              movie_head_pic,
                                                              movie_detail_pic, dyttsearch,
                                                              pymysql.escape_string(chinese_movie_name)
                                                              )
        print(sql)
        self.cursor.execute(sql)
        # 提交sql
        self.connect.commit()
        return item
