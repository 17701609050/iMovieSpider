# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImoviespiderItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    translation_name = scrapy.Field()  # 译名
    moviename = scrapy.Field()  # 电影名
    chinese_movie_name = scrapy.Field()  # 电影名
    style = scrapy.Field()  # 类别
    country = scrapy.Field()  # 产地
    doubanscore = scrapy.Field()  # 豆瓣评分
    doubancounter = scrapy.Field()  # 豆瓣评分人数
    language = scrapy.Field()  # 语言
    dateyear = scrapy.Field()  # 上映日期
    imdbscore = scrapy.Field()  # IMDB评分
    imdbcounter = scrapy.Field()  # IMDB评分人数
    movie_length = scrapy.Field()  # 片长
    director = scrapy.Field()  # 导演
    actor = scrapy.Field()  # 主演
    aboutmovie = scrapy.Field()  # 简介
    downloadlink = scrapy.Field()  # 下载地址
    movie_head_pic = scrapy.Field()  # 电影海报
    movie_detail_pic = scrapy.Field()  # 电影详情图片
    dyttsearch = scrapy.Field()  # 电影天堂地址
