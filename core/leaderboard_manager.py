# core/leaderboard_manager.py

import json
import os

class LeaderboardManager:
    def __init__(self, file_path='leaderboard.json'):
        """
        初始化排行榜管理器。
        :param file_path: 排行榜数据文件路径
        """
        self.file_path = file_path
        self.leaderboard = self.load_leaderboard()

    def load_leaderboard(self):
        """
        从JSON文件加载排行榜数据。
        :return: 排行榜列表
        """
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    return json.load(file).get('high_scores', [])
            except json.JSONDecodeError:
                print("排行榜数据文件损坏，初始化为空排行榜。")
                return []
        else:
            return []

    def save_leaderboard(self):
        """
        将当前排行榜数据保存到JSON文件。
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump({"high_scores": self.leaderboard}, file, ensure_ascii=False, indent=4)

    def add_score(self, player_name, score, time_taken):
        """
        添加新分数到排行榜，并按分数降序和时间升序排序。
        :param player_name: 玩家姓名
        :param score: 玩家得分
        :param time_taken: 完成游戏的时间（秒）
        """
        self.leaderboard.append({
            "player": player_name,
            "score": score,
            "time": time_taken
        })
        # 按分数降序，时间升序排序
        self.leaderboard.sort(key=lambda x: (-x['score'], x['time']))
        # 保持排行榜前10名
        self.leaderboard = self.leaderboard[:10]
        self.save_leaderboard()
        print(f"排行榜已更新: {self.leaderboard}")

    def get_leaderboard(self):
        """
        获取当前排行榜数据。
        :return: 排行榜列表
        """
        return self.leaderboard
