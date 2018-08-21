# get_game_info()
import os
from pymongo import MongoClient
import pandas as pd

config={
    'project_dir':os.path.abspath(os.path.join(os.getcwd(), "..")),
    'headers':{
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
}

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
