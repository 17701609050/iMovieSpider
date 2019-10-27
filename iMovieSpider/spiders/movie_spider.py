# -*- coding: utf-8 -*-
import scrapy
import sys
import re
import time
import requests
from pprint import pprint
from ..items import ImoviespiderItem


class DmozSpider(scrapy.Spider):
    name = "movie"
    base_url = "https://www.ygdy8.net"
    allowed_domains = ["www.ygdy8.net"]
    start_urls = [
        "https://www.ygdy8.net",

    ]
    headers = {
        'connection': "keep-alive",
        'pragma': "no-cache",
        'cache-control': "no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
        'dnt': "1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'cookie': "XLA_CI=97928deaf2eec58555c78b1518df7727",
    }
    movies = []

    def start_requests(self):
        base_url = 'https://www.ygdy8.net/html/gndy/{}/index.html'
        categories = ['china', 'rihan', 'oumei', 'dyzz']
        # categories = ['oumei']
        for category in categories:
            yield scrapy.Request(base_url.format(category), headers=self.headers, callback=self.parse)

    def parse(self, response):
        # xpath('//div[contains(@class,"a") and contains(@class,"b")]') #它会取class含有有a和b的元素
        detail_urls = response.xpath('//a[@class="ulink"]/@href').extract()
        detail_urls = [url for url in detail_urls if 'index' not in url]
        print(detail_urls)

        for url in detail_urls:
            yield scrapy.Request(response.urljoin(url), headers=self.headers, callback=self.parse_movie_detail)
        next_page = response.xpath(u'.//a[text()="下一页"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, headers=self.headers, callback=self.parse)

    def parse_movie_detail(self, response):
        item = ImoviespiderItem()

        movie_title = response.xpath('//div[@class="title_all"]//h1//font[@color="#07519a"]')
        if len(movie_title) > 0:
            print(movie_title[0].xpath(".//text()")[0])
            item['chinese_movie_name'] = movie_title[0].xpath(".//text()")[0].root
        if len(response.xpath("//div[@id='Zoom']")) > 0:
            zoom = response.xpath("//div[@id='Zoom']")[0]
        text_list = zoom.xpath(".//text()")     # 版本3.0，直接获取页面中的文本，进行过滤
        for (index, text) in enumerate(text_list):
            text = text.root
            if text.startswith("◎译　　名"):
                item["translation_name"] = text.replace("◎译　　名", "").strip()
            elif text.startswith("◎片　　名"):
                item["moviename"] = text.replace("◎片　　名", "").strip()
            elif text.startswith("◎年　　代"):
                item["dateyear"] = text.replace("◎年　　代", "").strip()
            elif text.startswith("◎产　　地"):
                item["country"] = text.replace("◎产　　地", "").strip()
            elif text.startswith("◎类　　别"):
                item["style"] = text.replace("◎类　　别", "").strip()
            elif text.startswith("◎语　　言"):
                item["language"] = text.replace("◎语　　言", "").strip()
            elif text.startswith("◎上映日期"):
                item["dateyear"] = text.replace("◎上映日期", "").strip()
            elif text.startswith("◎豆瓣评分"):
                douban = text.replace("◎豆瓣评分", "").strip().split('/')
                if len(douban) == 1:
                    item["doubanscore"] = douban[0]
                if len(douban) == 2:
                    item["doubanscore"] = douban[0]
                    item["doubancounter"] = self.get_counter(douban[1])
            elif text.startswith("◎IMDb评分"):
                imdb = text.replace("◎IMDb评分", "").strip().split('/')
                if len(imdb) == 1:
                    item["imdbscore"] = imdb[0]
                if len(imdb) == 2:
                    item["imdbscore"] = imdb[0]
                    item["imdbcounter"] = self.get_counter(imdb[1])
            elif text.startswith("◎片　　长"):
                item["movie_length"] = text.replace("◎片　　长", "").strip()
            elif text.startswith("◎导　　演"):
                item["director"] = text.replace("◎导　　演", "").strip()
            elif text.startswith("◎主　　演"):
                actors = []
                actors.append(text.replace("◎主　　演", "").strip())
                for num in range(index + 1, index + 10):
                    if text_list[num].root.startswith("◎简　　介"):
                        break
                    else:
                        actors.append(text_list[num].root.strip())
                item["actor"] = ','.join(actors)
            elif text.startswith("◎简　　介"):
                conttent_index = index + 1
                item["aboutmovie"] = text_list[conttent_index].root.strip()

            self.movies.append(item)

        imgs = zoom.xpath(".//img/@src")#[1]
        if len(imgs) is not None:
            if len(imgs) == 1:
                item['movie_head_pic'] = imgs[0].extract().split('/')[-1]
            elif len(imgs) == 2:
                item['movie_head_pic'] = imgs[0].extract().split('/')[-1]
                item['movie_detail_pic'] = imgs[1].extract().split('/')[-1]
            # for img in imgs:
            #     print img.extract()
            #     img_url = img.extract()
            #     time.sleep(0.5)
            #     self.write_img(img_url)
        # 由于页面的原因，对下载链接进行特殊过滤
        # 取到下载链接，实际上这里有两个
        download_link = response.xpath('//tbody//td[@style="WORD-WRAP: break-word"]//a/@href').extract()
        # 有些电影是没有下载地址的，所以要判断一下，有的才继续下一步。
        if len(download_link) is not None:
            # 首先获取到FTP的地址
            # 有些是没有迅雷下载地址的，所以要判断一下，没有thunder_download_link就为空，不然会报错。
            if len(download_link) == 1:
                item['downloadlink'] = download_link[0]
            elif len(download_link) == 2:
                item['downloadlink'] = download_link[1]
            else:
                item['downloadlink'] = ''

        item["dyttsearch"] = response.url
        yield item

    def write_img(self, imgurl):
        img_name = imgurl.split('/')[-1]
        # 1. 打开文件，返回一个文件对象
        with open('/home/zipinglx/movie/'+str(img_name), 'wb') as f:
            # 2. 获取图片里的内容
            images = requests.get(imgurl)
            # 3. 调用文件对象write() 方法，将图片的内容写入到文件里
            f.write(images.content)

    def get_counter(self, score_str):
        score_str = score_str.replace(' ', '')
        score_str = score_str.replace('10from', '').replace(',', '').replace('users', '')
        return score_str

