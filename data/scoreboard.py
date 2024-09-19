# data/scoreboard.py

import json
import os

class Scoreboard:
    """
    排行榜类，管理玩家的分数和排名。
    """

    def __init__(self):
        """
        初始化排行榜，尝试从文件中加载数据。
        """
        self.score_file = "scores.json"
        self.scores = self.load_scores()

    def load_scores(self):
        """
        从文件中加载排行榜数据。

        :return: list，包含玩家分数的列表
        """
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as f:
                    scores = json.load(f)
                print("成功加载排行榜数据。")
                return scores
            except Exception as e:
                print(f"加载排行榜数据出错：{e}，使用空的排行榜。")
        else:
            print("排行榜文件不存在，使用空的排行榜。")
        return []

    def save_scores(self):
        """
        将当前排行榜数据保存到文件。
        """
        try:
            with open(self.score_file, 'w') as f:
                json.dump(self.scores, f, indent=4)
            print("排行榜已保存。")
        except Exception as e:
            print(f"保存排行榜数据出错：{e}")

    def add_score(self, player_name, score):
        """
        添加新的玩家分数到排行榜。

        :param player_name: str，玩家昵称
        :param score: int，玩家得分
        """
        self.scores.append({'name': player_name, 'score': score})
        self.scores = sorted(self.scores, key=lambda x: x['score'], reverse=True)
        print(f"新分数已添加：{player_name} - {score}")
        self.save_scores()

    def get_top_scores(self, top_n=10):
        """
        获取排行榜上的前N名玩家。

        :param top_n: int，要获取的排名数量
        :return: list，包含前N名玩家分数的列表
        """
        return self.scores[:top_n]
