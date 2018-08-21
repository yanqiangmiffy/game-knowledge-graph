# get_game_info()
import os
from pymongo import MongoClient
import pandas as pd
from py2neo import Graph,Node,Relationship,NodeMatcher
from tqdm import tqdm

# 数据路径
config={
    'project_dir':os.path.abspath(os.path.join(os.getcwd(), "..")),
    'headers':{
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
}
info_file_path = os.path.join(config['project_dir'], 'data', 'game_info.csv')
data=pd.read_csv(info_file_path)
data['product_designer']=data['product_designer'].apply(lambda x: x.replace("制作发行：",'').strip())
keys=data.columns



def save_mongodb():
    """
    将数据存入到MongoDB
    :return:
    """
    conn=MongoClient('127.0.0.1',27017)
    db=conn.game # 连接game数据库，没有则自动创建
    my_set=db.game_info # 使用game_info集合，没有则自动创建
    print("正在将数据存入MongoDB。。")
    for i in tqdm(data.index):
        row=dict(zip(keys,data.loc[i].values[0:-1]))
        row['game_id']=int(row['game_id'])
        row['game_rating']=int(row['game_rating'])  # pymongo 不能编码numpy.int64，这里需要强制转化为int类型
        row['product_designer']=row['product_designer'].replace("制作发行：",'').strip()  # pymongo 不能编码numpy.int64，这里需要强制转化为int类型
        my_set.insert(row)


def save_neo4j():
    graph=Graph(
        host="127.0.0.1",
        user="neo4j",
        password="12345"
    )

    print("正在创建游戏发行商节点。。")
    # 创建发行商节点
    productor_names=set(data['product_designer'].tolist())
    for productor_name in tqdm(productor_names):
        productor_node=Node("Productor",name=productor_name)
        graph.create(productor_node)

    # 创建游戏节点以及与发行商的关系
    print("正在创建游戏节点以及与发行商的关系。。")
    matcher=NodeMatcher(graph)
    for i in tqdm(data.index):
        row = dict(zip(keys, data.loc[i].values[0:-1]))
        row['game_id'] = int(row['game_id'])
        row['game_rating'] = int(row['game_rating'])

        # 游戏节点
        productor_name=row.pop('product_designer')
        productor_node=matcher.match("Productor", name=productor_name).first()

        game_node=Node("Game")
        game_node.update(row)

        # 建立关系
        relation=Relationship(productor_node,"发行",game_node)
        node_re=productor_node|game_node|relation

        graph.create(node_re)


save_mongodb()