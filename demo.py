from pymongo import MongoClient

conn=MongoClient('127.0.0.1',27017)

db=conn.game # 连接game数据库，没有则自动创建
my_set=db.game_info # 使用game_info集合，没有则自动创建

my_set.insert({'game_id': 0, 'game_name': '暗黑地牢', 'game_rating': 5, 'game_url': 'http://down.ali213.net/pcgame/darkestdungeon.html', 'cn_title': '《暗黑地牢》免安装简体中文绿色版[Ancestral版|Build 24353|官方中文]', 'en_title': 'Darkest Dungeon', 'pic_url': 'http://imgs.ali213.net/oday/uploadfile/2015/01/05/2015010530506624.jpg', 'game_category': '游戏类型：策略战棋SLG', 'product_designer': '游戏类型：策略战棋SLG', 'release_date': '游戏类型：策略战棋SLG', 'file_size': '游戏类型：策略战棋SLG', 'game_tags': '单人单机;2D画面;不支持手柄;菜鸟入门;RPG;策略', 'game_intro': '《暗黑地牢(DarkestDungeon)》是一款充满地狱色彩的RPG。画风硬朗不凡，颇具美式动漫的风格。爆裂的火花，凶恶的地牢战士，赤红的鲜血……一切都被一把燃烧着希望之光的火把联系起来。在这样充满压抑和恐惧的氛围中，将会发生怎样的故事呢？《暗黑地牢》将采用回合制RPG的方式进行战斗，丰富的人物属性和技能需要玩家更深入的掌控。与ARPG不同，回合制RPG或许在战斗方面更加考验玩家对人物编排，设定，以及属性方面的了解。'})
