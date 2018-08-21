# game-knowledge-graph
:video_game: 关于PC游戏的知识图谱构建，目的主要是为了学习知识图谱构建的相关流程

## 数据获取

- 地址：[【游侠网】单机游戏大全](http://down.ali213.net/pcgame/all/0-0-0-0-new-pic-1.html)
- 爬取思路主要是先获取每个游戏的链接，然后根据链接爬取每个游戏的基本信息，两个步骤分开
- 注意的问题：
    - 部分游戏下载链接不存在
    - 存在游戏封面图片不存在
    - 游戏英文名字不存在
    
    
## 数据存储

- MongoDB

将爬取的信息存储到MongoDB，利用d3.js或者echart.js做前端可视化

- 将Neo4j存储到图数据库

![](https://github.com/yanqiangmiffy/game-knowledge-graph/blob/master/assets/neo4j.png)
