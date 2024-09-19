# ui/ui_manager.py

import pygame
import sys
from ui.assets import Assets
from ui.utils import Button
from core.game_logic import GameLogic
from data.settings import Settings
from data.scoreboard import Scoreboard
from data.levels import LevelManager
from network.network_manager import NetworkManager

class UIManager:
    """
    用户界面管理器，处理所有的界面显示和用户交互。
    """
    def __init__(self):
        """
        初始化界面管理器。
        """

        pygame.init()
        self.settings = Settings()
        # 修改屏幕尺寸为竖屏模式
        self.settings.settings['screen_size'] = (500, 780)
        self.screen_width, self.screen_height = self.settings.settings['screen_size']
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("龙了个龙")
        self.clock = pygame.time.Clock()
        self.assets = Assets()
        self.current_scene = "main_menu"  # 当前场景
        self.game_logic = None  # 游戏逻辑对象
        # 动态调整字体大小
        self.font_size = int(self.screen_height * 0.03)
        # 修改字体为支持中文的字体，例如 "SimHei"
        self.font = pygame.font.SysFont("SimHei", self.font_size, bold=True)  # 加粗字体
        self.scoreboard = Scoreboard()
        self.level_manager = LevelManager()
        self.network_manager = NetworkManager("https://example.com/api")  # 示例服务器地址

        # 定义按钮尺寸
        self.button_width = int(self.screen_width * 0.5)
        self.button_height = int(self.screen_height * 0.08)
        self.small_button_size = (int(self.screen_width * 0.1), int(self.screen_width * 0.1))  # 小按钮尺寸
        self.spacing = int(self.screen_height * 0.02)    # 界面元素之间的间距

        # 主菜单界面元素（文字按钮）
        center_x = self.screen_width / 2

        self.start_button = Button(
            screen=self.screen,
            text="开始游戏",
            position=(center_x, self.screen_height * 0.5),
            size=(self.button_width, self.button_height),
            font_size=int(self.screen_height * 0.04),
            font_name="SimHei",
            text_color=(0, 0, 0),
            bg_color=(200, 200, 200),  # 按钮背景颜色，可以根据需要调整
            shape='rect'
        )

        self.settings_button = Button(
            screen=self.screen,
            text="设置",
            position=(center_x, self.start_button.position[1] + self.button_height + self.spacing),
            size=(self.button_width, self.button_height),
            font_size=int(self.screen_height * 0.04),
            font_name="SimHei",
            text_color=(0, 0, 0),
            bg_color=(200, 200, 200),
            shape='rect'
        )

        self.rank_button = Button(
            screen=self.screen,
            text="排行榜",
            position=(center_x, self.settings_button.position[1] + self.button_height + self.spacing),
            size=(self.button_width, self.button_height),
            font_size=int(self.screen_height * 0.04),
            font_name="SimHei",
            text_color=(0, 0, 0),
            bg_color=(200, 200, 200),
            shape='rect'
        )

        self.quit_button = Button(
            screen=self.screen,
            text="退出游戏",
            position=(center_x, self.rank_button.position[1] + self.button_height + self.spacing),
            size=(self.button_width, self.button_height),
            font_size=int(self.screen_height * 0.04),
            font_name="SimHei",
            text_color=(0, 0, 0),
            bg_color=(200, 200, 200),
            shape='rect'
        )

        # 模式选择界面元素（文字按钮）
        self.easy_mode_button = Button(
            screen=self.screen,
            text="简单模式",
            position=(center_x, self.screen_height * 0.4),
            size=(self.button_width, self.button_height),
            font_size=int(self.screen_height * 0.04),
            font_name="SimHei",
            text_color=(0, 0, 0),
            bg_color=(200, 200, 200),
            shape='rect'
        )

        self.hard_mode_button = Button(
            screen=self.screen,
            text="困难模式",
            position=(center_x, self.easy_mode_button.position[1] + self.button_height + self.spacing),
            size=(self.button_width, self.button_height),
            font_size=int(self.screen_height * 0.04),
            font_name="SimHei",
            text_color=(0, 0, 0),
            bg_color=(200, 200, 200),
            shape='rect'
        )

        self.hell_mode_button = Button(
            screen=self.screen,
            text="地狱模式",
            position=(center_x, self.hard_mode_button.position[1] + self.button_height + self.spacing),
            size=(self.button_width, self.button_height),
            font_size=int(self.screen_height * 0.04),
            font_name="SimHei",
            text_color=(0, 0, 0),
            bg_color=(200, 200, 200),
            shape='rect'
        )

        # 游戏界面道具按钮（使用图标按钮）
        self.hint_icon = self.assets.get_image("hint_icon.png")
        if self.hint_icon:
            self.hint_icon = pygame.transform.scale(self.hint_icon, self.small_button_size)
        else:
            # 如果没有提示图标，使用带有文字的矩形按钮
            self.hint_icon = pygame.Surface(self.small_button_size)
            self.hint_icon.fill((173, 216, 230))
            hint_text = self.font.render("提", True, (255, 255, 255))
            hint_rect = hint_text.get_rect(center=(self.small_button_size[0] / 2, self.small_button_size[1] / 2))
            self.hint_icon.blit(hint_text, hint_rect)

        self.hint_button = Button(
            screen=self.screen,
            image=self.hint_icon,
            position=(self.screen_width - self.small_button_size[0] / 2 - self.spacing, self.screen_height - self.small_button_size[1] / 2 - self.spacing),
            size=self.small_button_size,
            shape='rect'  # 根据您的 Button 类，这里仍然是 'rect'，如果需要不同形状可以调整
        )

        self.undo_icon = self.assets.get_image("undo_icon.png")
        if self.undo_icon:
            self.undo_icon = pygame.transform.scale(self.undo_icon, self.small_button_size)
        else:
            # 如果没有撤销图标，使用带有文字的矩形按钮
            self.undo_icon = pygame.Surface(self.small_button_size)
            self.undo_icon.fill((173, 216, 230))
            undo_text = self.font.render("撤", True, (255, 255, 255))
            undo_rect = undo_text.get_rect(center=(self.small_button_size[0] / 2, self.small_button_size[1] / 2))
            self.undo_icon.blit(undo_text, undo_rect)

        self.undo_button = Button(
            screen=self.screen,
            image=self.undo_icon,
            position=(self.small_button_size[0] / 2 + self.spacing, self.screen_height - self.small_button_size[1] / 2 - self.spacing),
            size=self.small_button_size,
            shape='rect'
        )

        # 游戏结束界面元素（文字按钮）
        self.restart_button = Button(
            screen=self.screen,
            text="重新开始",
            position=(center_x, self.screen_height * 0.6),
            size=(self.button_width, self.button_height),
            font_size=int(self.screen_height * 0.04),
            font_name="SimHei",
            text_color=(0, 0, 0),
            bg_color=(200, 200, 200),
            shape='rect'
        )
        self.main_menu_button = Button(
            screen=self.screen,
            text="主菜单",
            position=(center_x, self.restart_button.position[1] + self.button_height + self.spacing),
            size=(self.button_width, self.button_height),
            font_size=int(self.screen_height * 0.04),
            font_name="SimHei",
            text_color=(0, 0, 0),
            bg_color=(200, 200, 200),
            shape='rect'
        )

        self.selected_mode = None  # 记录玩家选择的模式

    def run(self):
        """
        运行界面主循环。
        """
        while True:
            self.clock.tick(self.settings.settings['fps'])
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()

    def handle_events(self):
        """
        处理全局事件。
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        """
        处理鼠标点击事件。
        :param pos: (x, y) 鼠标点击位置
        """
        if self.current_scene == "main_menu":
            if self.start_button.is_clicked(pos):
                self.current_scene = "mode_selection"
            elif self.settings_button.is_clicked(pos):
                self.open_settings()
            elif self.rank_button.is_clicked(pos):
                self.current_scene = "leaderboard"  # 切换到排行榜界面
            elif self.quit_button.is_clicked(pos):
                pygame.quit()
                sys.exit()
        elif self.current_scene == "leaderboard":
            if self.main_menu_button.is_clicked(pos):
                self.current_scene = "main_menu"
        elif self.current_scene == "mode_selection":
            if self.easy_mode_button.is_clicked(pos):
                self.selected_mode = 'easy'
                self.start_game()
            elif self.hard_mode_button.is_clicked(pos):
                self.selected_mode = 'hard'
                self.start_game()
            elif self.hell_mode_button.is_clicked(pos):
                self.selected_mode = 'hell'
                self.start_game()
        elif self.current_scene == "game":
            # 检查道具按钮
            if self.hint_button.is_clicked(pos):
                self.game_logic.use_hint()
            elif self.undo_button.is_clicked(pos):
                self.game_logic.use_undo()
            else:
                self.game_logic.handle_player_action(pos)
        elif self.current_scene == "game_over":
            if self.restart_button.is_clicked(pos):
                self.current_scene = "mode_selection"
            elif self.main_menu_button.is_clicked(pos):
                self.current_scene = "main_menu"

    def start_game(self):
        """
        开始新游戏。
        """
        level_config = self.level_manager.get_level_config(self.selected_mode)
        if level_config:
            # 初始化 GameLogic 对象
            self.game_logic = GameLogic(level_config, self.screen_width, self.screen_height)
            self.current_scene = "game"
        else:
            print("无法获取关卡配置！")
            self.current_scene = "main_menu"

    def open_settings(self):
        """
        打开设置界面。（待实现）
        """
        print("打开设置界面")

    def open_rankings(self):
        """
        打开排行榜界面。（待实现）
        """
        print("打开排行榜界面")

    def update(self):
        if self.current_scene == "game":
            self.game_logic.update()
            if self.game_logic.is_game_over:
                self.current_scene = "game_over"
                self.is_victory = self.game_logic.is_victory

                # 在游戏结束时调用 end_game 方法
                self.game_logic.end_game(player_name="Player1")

                # 上传玩家得分到服务器
                self.upload_player_score()


    def render(self):
        """
        渲染当前场景。
        """
        if self.current_scene == "main_menu":
            self.render_main_menu()
        elif self.current_scene == "mode_selection":
            self.render_mode_selection()
        elif self.current_scene == "game":
            self.render_game()
        elif self.current_scene == "game_over":
            self.render_game_over()
        elif self.current_scene == "leaderboard":
            self.render_leaderboard()  # 渲染排行榜

    def render_main_menu(self):
        """
        渲染主菜单界面。
        """
        background = self.assets.get_background_image("menu_background")
        if background:
            # 调整背景图像大小以适应屏幕
            background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(self.settings.settings['bg_color'])

        # 绘制游戏Logo
        game_logo = self.assets.get_logo_image("game_logo")
        if game_logo:
            logo_size = (int(self.screen_width * 0.7), int(self.screen_height * 0.25))  # 增大 Logo 尺寸
            game_logo = pygame.transform.scale(game_logo, logo_size)
            logo_rect = game_logo.get_rect(center=(self.screen_width / 2, self.screen_height * 0.2))
            self.screen.blit(game_logo, logo_rect)
        else:
            # 如果没有Logo图片，使用文字标题
            title_font = pygame.font.SysFont("SimHei", int(self.screen_height * 0.1), bold=True)
            title_text = title_font.render("羊了个羊", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.screen_width / 2, self.screen_height * 0.2))
            self.screen.blit(title_text, title_rect)

        self.start_button.draw()
        self.settings_button.draw()
        self.rank_button.draw()
        self.quit_button.draw()

    def render_mode_selection(self):
        """
        渲染模式选择界面，使用游戏背景。
        """
        # 使用游戏背景
        background = self.assets.get_background_image("game_background")
        if background:
            # 调整背景图像大小以适应屏幕
            background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(self.settings.settings['bg_color'])

        # 绘制模式选择标题
        title_font = pygame.font.SysFont("SimHei", int(self.screen_height * 0.06), bold=True)
        title_text = title_font.render("请选择游戏模式", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width / 2, self.screen_height * 0.25))
        self.screen.blit(title_text, title_rect)

        self.easy_mode_button.draw()
        self.hard_mode_button.draw()
        self.hell_mode_button.draw()

    def render_game(self):
        """
        渲染游戏界面。
        """
        background = self.assets.get_background_image("game_background")
        if background:
            background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(self.settings.settings['bg_color'])

        # 绘制游戏图案
        for pattern in sorted(self.game_logic.patterns, key=lambda p: p.layer):
            if not pattern.is_cleared:
                pattern_image = self.assets.get_pattern_image(pattern.id)
                x, y = pattern.position
                if pattern_image:
                    pattern_image = pygame.transform.scale(pattern_image, pattern.size)
                    pattern_rect = pattern_image.get_rect(center=(x, y))
                    self.screen.blit(pattern_image, pattern_rect)
                else:
                    pygame.draw.rect(
                        self.screen,
                        (255, 255, 255),
                        pygame.Rect(x - pattern.size[0] / 2, y - pattern.size[1] / 2, *pattern.size)
                    )

                # 如果该图案在提示列表中，或者鼠标悬停在图案上，绘制红色边框
                if pattern in self.game_logic.hint_patterns or pattern == self.game_logic.hovered_pattern:
                    pygame.draw.rect(
                        self.screen,
                        (255, 0, 0),
                        pygame.Rect(x - pattern.size[0] / 2, y - pattern.size[1] / 2, *pattern.size),
                        3  # 边框宽度
                    )

        # 绘制玩家暂存区
        self.render_player_storage()

        # 绘制道具按钮
        self.hint_button.draw()
        self.undo_button.draw()

        # 绘制计分板和倒计时
        self.render_scoreboard()

        # 绘制道具剩余次数
        self.render_item_counts()

    def render_item_counts(self):
        """
        渲染提示和撤销道具的剩余次数，并使其居中放置。
        """
        hint_count_str = f"提示剩余: {self.game_logic.item_manager.hint_limit - self.game_logic.item_manager.hint_used}"
        undo_count_str = f"撤销剩余: {self.game_logic.item_manager.undo_limit - self.game_logic.item_manager.undo_used}"

        # 渲染文本
        hint_count_text = self.font.render(hint_count_str, True, (255, 255, 255))
        undo_count_text = self.font.render(undo_count_str, True, (255, 255, 255))

        # 获取文本矩形
        hint_text_rect = hint_count_text.get_rect(
            center=(self.screen_width // 2, self.screen_height - self.spacing * 4))
        undo_text_rect = undo_count_text.get_rect(
            center=(self.screen_width // 2, self.screen_height - self.spacing * 2))

        # 绘制文本，使其居中
        self.screen.blit(hint_count_text, hint_text_rect)
        self.screen.blit(undo_count_text, undo_text_rect)

    def render_player_storage(self):
        """
        绘制玩家的暂存区，在界面底部 Undo 和 Hint 按钮上方显示已选中的图案。
        """
        max_storage = self.game_logic.player.storage_limit  # 获取暂存区容量限制
        item_size = int((self.screen_width - self.spacing * (max_storage + 1)) / max_storage)  # 计算物品尺寸

        y = self.undo_button.position[1] - self.small_button_size[1] / 2 - self.spacing - item_size / 2

        x_start = self.spacing + item_size / 2

        x = x_start
        for i in range(max_storage):
            if i < len(self.game_logic.player.selected_patterns):
                pattern = self.game_logic.player.selected_patterns[i]
                pattern_image = self.assets.get_pattern_image(pattern.id)
                if pattern_image:
                    pattern_image = pygame.transform.scale(pattern_image, (item_size, item_size))
                    pattern_rect = pattern_image.get_rect(center=(x, y))
                    self.screen.blit(pattern_image, pattern_rect)
                else:
                    pygame.draw.rect(
                        self.screen,
                        (255, 255, 255),
                        pygame.Rect(x - item_size / 2, y - item_size / 2, item_size, item_size)
                    )
            else:
                # 绘制空的占位符，表示可用的暂存位置
                pygame.draw.rect(
                    self.screen,
                    (200, 200, 200),
                    pygame.Rect(x - item_size / 2, y - item_size / 2, item_size, item_size),
                    2  # 边框宽度
                )
            x += item_size + self.spacing  # 间距

    def render_scoreboard(self):
        """
        绘制计分板和倒计时。
        """
        # 显示得分
        score_text_str = f"得分: {self.game_logic.player.score}"
        score_text = self.font.render(score_text_str, True, (255, 255, 255))
        self.screen.blit(score_text, (self.spacing, self.spacing))

        # 显示倒计时
        time_remaining = int(self.game_logic.timer.remaining_time)
        time_text_str = f"时间: {time_remaining}(s)"
        time_text = self.font.render(time_text_str, True, (255, 255, 255))
        text_width, text_height = self.font.size(time_text_str)
        self.screen.blit(time_text, (self.screen_width - text_width - self.spacing, self.spacing))

    def render_game_over(self):
        """
        渲染游戏结束界面。
        """
        background = self.assets.get_background_image("menu_background")
        if background:
            # 调整背景图像大小以适应屏幕
            background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(self.settings.settings['bg_color'])

        result_text = "胜利！" if self.is_victory else "游戏结束！"
        result_font = pygame.font.SysFont("SimHei", int(self.screen_height * 0.08), bold=True)
        result_render = result_font.render(result_text, True, (255, 255, 255))

        score_render = self.font.render(f"得分: {self.game_logic.player.score}", True, (255, 255, 255))

        # 居中显示结果
        self.screen.blit(result_render, result_render.get_rect(center=(self.screen_width / 2, self.screen_height * 0.3)))
        self.screen.blit(score_render, score_render.get_rect(center=(self.screen_width / 2, self.screen_height * 0.4)))

        self.restart_button.draw()
        self.main_menu_button.draw()

    def upload_player_score(self):
        """
        上传玩家的得分到服务器。
        """
        player_name = "Player1"  # 可以让玩家输入昵称
        score = self.game_logic.player.score
        self.network_manager.upload_score(player_name, score)

    def handle_events(self):
        """
        处理全局事件。
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                # 处理鼠标移动事件，更新悬停的图案
                self.handle_mouse_hover(event.pos)

    def handle_mouse_hover(self, pos):
        """
        处理鼠标悬停事件，检查鼠标是否悬停在某个图案上。
        :param pos: (x, y) 鼠标位置
        """
        if self.game_logic is None:
            return  # 如果游戏逻辑还未初始化，直接返回

        # 清空之前的悬停高亮状态
        self.game_logic.hovered_pattern = None

        # 检查是否悬停在某个图案上
        for pattern in self.game_logic.patterns:
            if pattern.contains_point(pos) and not pattern.is_cleared:
                self.game_logic.hovered_pattern = pattern
                break

    def render_leaderboard(self):
        """
        渲染排行榜界面。
        """
        # 设置背景为游戏背景
        background = self.assets.get_background_image("game_background")
        if background:
            background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(self.settings.settings['bg_color'])

        # 添加半透明覆盖层
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # 黑色半透明
        self.screen.blit(overlay, (0, 0))

        # 获取排行榜数据
        leaderboard = self.game_logic.leaderboard_manager.get_leaderboard()

        # 绘制排行榜标题
        title_font = pygame.font.SysFont("SimHei", int(self.screen_height * 0.08), bold=True)
        title_text = title_font.render("排行榜", True, (255, 215, 0))  # 金色字体
        title_rect = title_text.get_rect(center=(self.screen_width / 2, self.screen_height * 0.1))
        self.screen.blit(title_text, title_rect)

        # 绘制表头
        header_font = pygame.font.SysFont("SimHei", int(self.screen_height * 0.04), bold=True)
        headers = ["排名", "玩家", "分数", "时间(s)"]
        header_colors = (255, 255, 255)
        header_positions = [
            (self.screen_width * 0.15, self.screen_height * 0.2),
            (self.screen_width * 0.4, self.screen_height * 0.2),
            (self.screen_width * 0.6, self.screen_height * 0.2),
            (self.screen_width * 0.85, self.screen_height * 0.2)
        ]

        for header, pos in zip(headers, header_positions):
            header_text = header_font.render(header, True, header_colors)
            header_rect = header_text.get_rect(center=pos)
            self.screen.blit(header_text, header_rect)

        # 绘制分割线
        pygame.draw.line(self.screen, (255, 255, 255), (self.screen_width * 0.1, self.screen_height * 0.25),
                         (self.screen_width * 0.9, self.screen_height * 0.25), 2)

        # 绘制排行榜内容
        entry_font = pygame.font.SysFont("SimHei", int(self.screen_height * 0.035))
        row_height = int(self.screen_height * 0.07)
        start_y = self.screen_height * 0.3

        for index, entry in enumerate(leaderboard, start=1):
            # 计算每一行的Y坐标
            y = start_y + index * row_height

            # 交替行背景色
            if index % 2 == 0:
                row_color = (50, 50, 50, 100)  # 深灰色半透明
            else:
                row_color = (80, 80, 80, 100)  # 灰色半透明

            row_rect = pygame.Rect(self.screen_width * 0.1, y - row_height / 2, self.screen_width * 0.8,
                                   row_height - 10)
            row_surface = pygame.Surface((row_rect.width, row_rect.height), pygame.SRCALPHA)
            row_surface.fill(row_color)
            self.screen.blit(row_surface, (row_rect.x, row_rect.y))

            # 绘制每一列的内容
            entry_data = [
                str(index),
                entry['player'],
                str(entry['score']),
                str(int(entry['time']))
            ]
            column_positions = [
                self.screen_width * 0.15,
                self.screen_width * 0.4,
                self.screen_width * 0.6,
                self.screen_width * 0.85
            ]

            for data, pos in zip(entry_data, column_positions):
                entry_text = entry_font.render(data, True, (255, 255, 255))
                entry_rect = entry_text.get_rect(center=(pos, y))
                self.screen.blit(entry_text, entry_rect)

        # 如果排行榜为空，显示提示信息
        if not leaderboard:
            no_data_font = pygame.font.SysFont("SimHei", int(self.screen_height * 0.04), bold=True)
            no_data_text = no_data_font.render("暂无排行榜数据", True, (255, 255, 255))
            no_data_rect = no_data_text.get_rect(center=(self.screen_width / 2, self.screen_height * 0.5))
            self.screen.blit(no_data_text, no_data_rect)

        # 绘制返回主菜单按钮
        self.main_menu_button.draw()



