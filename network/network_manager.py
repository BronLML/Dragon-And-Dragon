# network/network_manager.py

import requests
import json

class NetworkManager:
    """
    网络管理类，处理与服务器的通信，实现全球排行榜等在线功能。
    """

    def __init__(self, server_url):
        """
        初始化网络管理器。

        :param server_url: str，服务器的基础 URL
        """
        self.server_url = server_url
        self.session = requests.Session()

    def upload_score(self, player_name, score):
        """
        上传玩家的得分到服务器。

        :param player_name: str，玩家昵称
        :param score: int，玩家得分
        :return: dict，服务器返回的结果
        """
        endpoint = f"{self.server_url}/upload_score"
        data = {
            'name': player_name,
            'score': score
        }
        try:
            response = self.session.post(endpoint, json=data)
            if response.status_code == 200:
                result = response.json()
                print("得分上传成功。")
                return result
            else:
                print(f"得分上传失败，状态码：{response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"网络请求异常：{e}")
        return None

    def get_global_rankings(self, top_n=10):
        """
        从服务器获取全球排行榜数据。

        :param top_n: int，要获取的排名数量
        :return: list，包含前N名玩家分数的列表
        """
        endpoint = f"{self.server_url}/get_rankings"
        params = {'top_n': top_n}
        try:
            response = self.session.get(endpoint, params=params)
            if response.status_code == 200:
                rankings = response.json()
                print("成功获取全球排行榜。")
                return rankings
            else:
                print(f"获取排行榜失败，状态码：{response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"网络请求异常：{e}")
        return []
