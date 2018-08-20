import requests
import os
from lxml import etree
import pymysql
import csv
import re
import time
from urllib.request import urlretrieve # 用来下载图片

config={
    'project_dir':os.path.abspath(os.path.join(os.getcwd(), "..")),
    'headers':{
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
}


def safe_mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_game_urls(page_num=614):

    safe_mkdir(os.path.join(config['project_dir'],'data'))  # 如果data文件夹不存在，就创建
    file_path = os.path.join(config['project_dir'],'data', 'game_urls.csv')
    out_data=open(file_path, 'w', encoding='utf-8', newline='')
    csv_writer=csv.writer(out_data)
    csv_writer.writerow(('id', 'name','rating', 'url'))

    id=0
    try:
        for page in range(1,page_num+1):
            url="http://down.ali213.net/pcgame/all/0-0-0-0-new-pic-{}.html".format(page)
            print("正在爬取第{}页：{}".format(page,url))

            res=requests.get(url=url,headers=config['headers'])
            res.encoding='utf-8'
            html=etree.HTML(res.text)
            names=html.xpath('//div[@id="rqjxhb"]/div[@class="list_body_contain"]/div/div[@class="list_body_con_con"]/a/text()')
            urls=html.xpath('//div[@id="rqjxhb"]/div[@class="list_body_contain"]/div/a[@class="list_body_con_down"]/@href')
            urls=["http://down.ali213.net"+url for url in urls]

            # 评分
            pfs=html.xpath('//div[@id="rqjxhb"]/div[@class="list_body_contain"]/div[@class="list_body_con"]/div[@class="list_body_con_pf"]')
            ratings=[]
            for pf in pfs:
                rating=pf.xpath('span[not(contains(@class,"another"))]')
                ratings.append(len(rating)-1)

            for name, rating,url in zip(names, ratings,urls):
                csv_writer.writerow((id, name, rating,url))
                id+=1
        out_data.close()
    except Exception as e:
        print(e)

def get_game_info():
    url_file_path = os.path.join(config['project_dir'], 'data', 'game_urls.csv')
    in_data=open(url_file_path,'r',encoding='utf-8')
    csv_reader=csv.reader(in_data)

    info_file_path = os.path.join(config['project_dir'], 'data', 'game_info.csv')
    out_data = open(info_file_path, 'a', encoding='utf-8',newline='')
    csv_writer = csv.writer(out_data)
    csv_writer.writerow(('game_id','game_name','game_rating','game_url',
                         'cn_title','en_title','pic_url','game_category',
                         'product_designer','release_date','file_size','game_tags',
                         'game_intro','down_url'))
    for i,row in enumerate(csv_reader):
        if i>0:
            game_id=row[0]
            game_name=row[1]
            game_rating=row[2]
            game_url=row[3]
            print("正在爬取: {} 的信息 ：{}".format(game_name,game_url))

            # game_url='http://down.ali213.net/pcgame/darkestdungeon.html'
            res=requests.get(game_url,headers=config['headers'])
            res.encoding='utf-8'
            html=etree.HTML(res.text)

            # 标题
            title_tag=html.xpath('//div[@class="newdown_l1_tit"]/h1[@class="newdown_l1_tit_cn"]')[0]
            cn_title=title_tag.xpath('string(.)')
            try:
                en_title=html.xpath('//div[@class="newdown_l1_tit"]/div[@class="newdown_l1_tit_en"]/text()')[0]
            except:
                en_title=''

            # 封面图片
            pic_url=html.xpath('//div[@class="newdown_l1"]/div[@class="newdown_l_con"]/div[@class="newdown_l_con_pic"]/img/@src')[0]
            img_dir=os.path.join(config['project_dir'],'images')
            safe_mkdir(img_dir)
            img_path=os.path.join(img_dir,str(game_id)+'.jpg')
            try:
                if not os.path.exists(img_path):
                    urlretrieve(pic_url,img_path)
            except:
                print(game_name+" 游戏图片不存在")

            # 基本信息
            infos=html.xpath('//div[@class="newdown_l1"]/div[@class="newdown_l_con"]/div[@class="newdown_l_con_con"]/div[@class="newdown_l_con_con_info"]')
            game_category=infos[0].xpath("string(.)")
            product_designer=infos[0].xpath("string(.)")
            release_date=infos[0].xpath("string(.)")
            file_size=infos[0].xpath("string(.)")

            # 游戏标签
            tags_parent=html.xpath('//div[@class="newdown_l1"]/div[@class="newdown_l_con"]/div[@class="newdown_l_con_con"]/div[@class="newdown_l_con_con_tag"]/div')[0]
            game_tags=";".join(tags_parent.xpath('.//a/text()'))

            # 游戏介绍
            game_intro=html.xpath('//div[@class="detail_body_con_bb"]/div[@class="detail_body_con_bb_con"]/div[@class="detail_body_con_bb_con1"]')[0].xpath("string(.)").strip()
            game_intro=re.sub('\s','',game_intro)

            #下载链接
            try:
                pattern=re.compile(r'<script>var downUrl ="(.*?)";</script>')
                down_url=re.findall(pattern,res.text)[0]
                down_url='http://www.soft50.com'+down_url
                csv_writer.writerow((game_id, game_name, game_rating, game_url,
                                     cn_title, en_title, pic_url, game_category,
                                     product_designer, release_date, file_size, game_tags,
                                     game_intro, down_url))
            except IndexError:
                print(game_name+"下载链接不存在")
                csv_writer.writerow((game_id, game_name, game_rating, game_url,
                                     cn_title, en_title, pic_url, game_category,
                                     product_designer, release_date, file_size, game_tags,
                                     game_intro, ''))

            time.sleep(1)

    in_data.close()
    out_data.close()
# get_game_info()
from pymongo import MongoClient
import pandas as pd
conn=MongoClient('127.0.0.1',27017)
db=conn.game # 连接game数据库，没有则自动创建
my_set=db.game_info # 使用game_info集合，没有则自动创建
info_file_path = os.path.join(config['project_dir'], 'data', 'game_info.csv')

data=pd.read_csv(info_file_path)
keys=data.columns



for indexs in data.index:
    row=dict(zip(keys,data.loc[indexs].values[0:-1]))
    row['game_id']=int(row['game_id'])
    row['game_rating']=int(row['game_rating'])  # pymongo 不能编码numpy.int64，这里需要强制转化为int类型
    my_set.insert(row)

