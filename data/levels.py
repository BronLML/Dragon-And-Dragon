import random

class LevelManager:
    """
    关卡管理器，管理游戏的关卡配置和难度设置。
    """

    def __init__(self):
        """
        初始化关卡管理器。
        """
        self.levels = self.load_levels()
        self.current_level = 1  # 默认从第1关开始

    def load_levels(self):
        """
        加载关卡配置，可以从文件或预定义的数据中加载。

        :return: dict，包含所有关卡配置的字典
        """
        # 修改关卡配置为不同模式
        levels = {
            'easy': {
                'pattern_types': 5,
                'total_patterns': 30,
                'layer_count': 3,
                'time_limit': 600,     # 增加时间限制
                'hint_limit': 5,       # 增加提示次数
                'undo_limit': 5,       # 增加撤销次数
                'storage_limit': 8     # 增加暂存区容量
            },
            'hard': {
                'pattern_types': 7,
                'total_patterns': 42,
                'layer_count': 5,
                'time_limit': 400,
                'hint_limit': 3,
                'undo_limit': 3,
                'storage_limit': 7
            },
            'hell': {
                'pattern_types': 10,
                'total_patterns': 60,
                'layer_count': 7,
                'time_limit': 300,
                'hint_limit': 1,
                'undo_limit': 1,
                'storage_limit': 7
            }
        }
        return levels

    def get_level_config(self, mode):
        """
        获取指定模式的关卡配置。

        :param mode: str，游戏模式（'easy', 'hard', 'hell'）
        :return: dict，关卡配置参数
        """
        return self.levels.get(mode, None)

    def reset(self):
        """
        重置关卡进度，回到第一关。
        """
        self.current_level = 1

    def randomize_pattern_positions(self, patterns):
        """
        随机化图案的摆放顺序，确保每次游戏都有新鲜感。

        :param patterns: list，图案对象列表
        """
        random.shuffle(patterns)
        # 可以在这里实现更复杂的随机化逻辑，如确保特定难度
