# core/timer.py

import time

class Timer:
    """
    倒计时器类，管理游戏时间。
    """

    def __init__(self, total_time):
        self.total_time = total_time  # 总时间限制
        self.start_time = time.time()  # 记录开始时间
        self.remaining_time = total_time

    def update(self):
        """
        更新剩余时间，每帧调用一次。
        """
        elapsed_time = time.time() - self.start_time
        self.remaining_time = self.total_time - elapsed_time

    def time_up(self):
        """
        检查时间是否到期。
        """
        return self.remaining_time <= 0

    def get_time_taken(self):
        """
        返回已用的时间。
        """
        return time.time() - self.start_time

    def add_time(self, seconds):
        """
        增加倒计时时间，用于加时道具。

        :param seconds: int，增加的秒数
        """
        self.time_limit += seconds
        print(f"已增加 {seconds} 秒，新的总时长为 {self.time_limit} 秒。")
