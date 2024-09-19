# data/settings.py

import json
import os

class Settings:
    """
    游戏设置类，管理用户的设置选项，如音量、分辨率等。
    """

    def __init__(self):
        """
        初始化设置，尝试从配置文件中加载，否则使用默认值。
        """
        self.config_file = "config.json"
        self.default_settings = {
            'screen_size': (800, 600),
            'bg_color': (30, 30, 30),
            'volume': 0.5,
            'music_on': True,
            'sound_effects_on': True,
            'fps': 60
        }
        self.settings = self.load_settings()

    def load_settings(self):
        """
        从配置文件中加载设置，如果文件不存在则使用默认设置。

        :return: dict，包含当前设置的字典
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    settings = json.load(f)
                print("成功加载配置文件。")
                return settings
            except Exception as e:
                print(f"加载配置文件出错：{e}，使用默认设置。")
        else:
            print("配置文件不存在，使用默认设置。")
        return self.default_settings.copy()

    def save_settings(self):
        """
        将当前设置保存到配置文件。
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            print("配置已保存。")
        except Exception as e:
            print(f"保存配置文件出错：{e}")

    def set_setting(self, key, value):
        """
        修改特定的设置项。

        :param key: str，设置项的键名
        :param value: 任意类型，设置项的值
        """
        if key in self.settings:
            self.settings[key] = value
            print(f"设置已更新：{key} = {value}")
        else:
            print(f"无效的设置项：{key}")

    def get_setting(self, key):
        """
        获取特定的设置项的值。

        :param key: str，设置项的键名
        :return: 任意类型，设置项的值
        """
        return self.settings.get(key, None)
