import pygame
import os

class Assets:
    """
    资源管理类，加载和管理游戏资源。
    """

    def __init__(self):
        """
        初始化资源管理器，加载所有需要的资源。
        """
        self.pattern_images = {}
        self.button_images = {}
        self.item_images = {}
        self.background_images = {}
        self.logo_images = {}
        self.load_assets()

    def load_assets(self):
        """
        加载游戏所需的图像和音频资源。
        """
        # 加载图案图片
        for i in range(10):  # 假设有10种图案
            image_path = os.path.join("assets", "patterns", f"pattern_{i}.png")
            if os.path.exists(image_path):
                image = pygame.image.load(image_path).convert_alpha()
                # 图案大小根据屏幕尺寸缩放，在使用时再缩放
                self.pattern_images[i] = image
            else:
                print(f"图案资源不存在：{image_path}")

        # 加载按钮图片
        button_names = ["start_button", "settings_icon", "rank_icon", "quit_button", "hint_button", "undo_button"]
        for name in button_names:
            image_path = os.path.join("assets", "buttons", f"{name}.png")
            if os.path.exists(image_path):
                image = pygame.image.load(image_path).convert_alpha()
                self.button_images[name] = image
            else:
                print(f"按钮资源不存在：{image_path}")

        # 加载道具图片
        item_names = ["hint_item", "undo_item"]
        for name in item_names:
            image_path = os.path.join("assets", "items", f"{name}.png")
            if os.path.exists(image_path):
                image = pygame.image.load(image_path).convert_alpha()
                self.item_images[name] = image
            else:
                print(f"道具资源不存在：{image_path}")

        # 加载背景图片
        background_names = ["menu_background", "game_background"]
        for name in background_names:
            image_path = os.path.join("assets", "backgrounds", f"{name}.png")
            if os.path.exists(image_path):
                image = pygame.image.load(image_path).convert()
                self.background_images[name] = image
            else:
                print(f"背景资源不存在：{image_path}")

        # 加载Logo和标题
        logo_names = ["game_logo", "game_title"]
        for name in logo_names:
            image_path = os.path.join("assets", "logo", f"{name}.png")
            if os.path.exists(image_path):
                image = pygame.image.load(image_path).convert_alpha()
                self.logo_images[name] = image
            else:
                print(f"Logo资源不存在：{image_path}")

    def get_image(self, filename):
        """
        通用的图像加载方法，根据文件名加载图像。

        :param filename: str，图像文件名
        :return: pygame.Surface，加载的图像对象
        """
        path = os.path.join("assets", filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            return image
        except FileNotFoundError:
            print(f"图像文件 '{filename}' 未找到。")
            return None

    def get_pattern_image(self, pattern_id):
        """
        获取指定图案ID的图像。

        :param pattern_id: int，图案ID
        :return: pygame.Surface 对象
        """
        return self.pattern_images.get(pattern_id, None)

    def get_button_image(self, name):
        """
        获取指定名称的按钮图像。

        :param name: str，按钮名称
        :return: pygame.Surface 对象
        """
        return self.button_images.get(name, None)

    def get_item_image(self, name):
        """
        获取指定名称的道具图像。

        :param name: str，道具名称
        :return: pygame.Surface 对象
        """
        return self.item_images.get(name, None)

    def get_background_image(self, name):
        """
        获取指定名称的背景图像。

        :param name: str，背景名称
        :return: pygame.Surface 对象
        """
        return self.background_images.get(name, None)

    def get_logo_image(self, name):
        """
        获取指定名称的Logo或标题图像。

        :param name: str，Logo名称
        :return: pygame.Surface 对象
        """
        return self.logo_images.get(name, None)
