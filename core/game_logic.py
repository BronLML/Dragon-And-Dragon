# core/game_logic.py

import random
from core.player import Player
from core.timer import Timer
from data.items import ItemManager
from core.pattern import Pattern  # 确保 Pattern 类存在并正确导入
import copy  # 用于深拷贝
from core.leaderboard_manager import LeaderboardManager

class GameLogic:
    """
    游戏逻辑类，处理图案生成、分层摆放、匹配和消除机制。
    """

    def __init__(self, level_config, screen_width, screen_height):
        """
        初始化游戏逻辑。

        :param level_config: dict，关卡配置参数，包括图案种类、数量、层数等。
        :param screen_width: int，屏幕宽度
        :param screen_height: int，屏幕高度
        """
        self.leaderboard_manager = LeaderboardManager('leaderboard.json')  # 初始化排行榜管理器
        self.hovered_pattern = None  # 用于存储当前鼠标悬停的图案
        self.hint_patterns = []  # 初始化 hint_patterns
        self.level_config = level_config
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pattern_size = (int(screen_width * 0.2), int(screen_width * 0.2))  # 增大图案尺寸为屏幕宽度的20%
        self.patterns = []          # 存储所有图案对象
        self.layers = []            # 存储分层摆放的图案列表
        self.player = Player(level_config['storage_limit'])      # 玩家对象
        self.timer = Timer(level_config['time_limit'])  # 倒计时器
        self.is_game_over = False   # 游戏结束标志
        self.is_victory = False     # 游戏胜利标志

        self.item_manager = ItemManager(
            level_config.get('hint_limit', 5),
            level_config.get('undo_limit', 3)
        )  # 道具管理器

        self.history = []  # 添加历史记录栈

        self.generate_patterns()
        self.arrange_patterns()

    def use_undo(self):
        """
        使用撤销功能，恢复到上一个游戏状态。
        """
        if self.item_manager.can_use_undo():
            success = self.item_manager.use_undo(self.player)
            if success:
                self.restore_state()
                print("撤销成功。")
            else:
                print("无法撤销。")
        else:
            print("撤销次数已用完。")

    def use_hint(self):
        """
        使用提示功能，查找可消除的图案并进行提示。
        """
        hint = self.item_manager.use_hint(self)
        if hint:
            self.hint_patterns = hint
            print("提示已更新，找到可消除的图案。")
        else:
            print("没有可用的提示。")

    def find_hint(self):
        """
        查找可消除的图案组合，用于提示功能。
        优化逻辑：优先查找未被遮挡、位于上层的图案组合。
        :return: list，包含可消除的图案对象
        """
        pattern_counts = {}

        # 统计玩家已经选中的图案数量
        for pattern in self.player.selected_patterns:
            pattern_counts[pattern.id] = pattern_counts.get(pattern.id, 0) + 1

        # 优先提示未被遮挡且位于上层的图案
        for layer_index in reversed(range(len(self.layers))):  # 从顶层开始检查
            layer = self.layers[layer_index]
            for pattern in layer:
                if not pattern.is_cleared and not self.is_pattern_covered(pattern):
                    temp_count = pattern_counts.get(pattern.id, 0) + 1
                    if temp_count >= 3:
                        # 找到一个可消除的组合，确保不被覆盖
                        hint_patterns = [
                            p for p in self.patterns
                            if p.id == pattern.id and not p.is_cleared and not self.is_pattern_covered(p)
                        ]
                        if len(hint_patterns) >= 3:
                            return hint_patterns[:3]
        return None

    def generate_patterns(self):
        """
        根据关卡配置生成图案列表。
        """
        pattern_types = self.level_config['pattern_types']  # 图案种类数
        total_patterns = self.level_config['total_patterns']  # 总图案数量

        # 确保总图案数量是3的倍数，以满足三消规则
        if total_patterns % 3 != 0:
            total_patterns += 3 - (total_patterns % 3)

        pattern_ids = []
        for i in range(total_patterns // 3):
            pattern_id = i % pattern_types
            pattern_ids.extend([pattern_id] * 3)  # 每种图案添加3个

        random.shuffle(pattern_ids)  # 打乱图案顺序

        # 创建图案对象并添加到列表
        self.patterns = [Pattern(id=pid, size=self.pattern_size) for pid in pattern_ids]

    def arrange_patterns(self):
        """
        将图案集中摆放在屏幕中心，允许一定程度的重叠。
        """
        center_x = self.screen_width / 2
        center_y = self.screen_height / 2

        max_offset = self.pattern_size[0] * 2  # 最大偏移量，控制图案分布的范围

        # 根据层数将图案分组
        layer_count = self.level_config['layer_count']
        patterns_per_layer = len(self.patterns) // layer_count

        for layer_index in range(layer_count):
            layer_patterns = self.patterns[layer_index * patterns_per_layer:(layer_index + 1) * patterns_per_layer]
            self.layers.append(layer_patterns)
            for pattern in layer_patterns:
                pattern.layer = layer_index
                # 在中心点附近随机生成偏移量
                offset_x = random.uniform(-max_offset, max_offset)
                offset_y = random.uniform(-max_offset, max_offset)
                pattern.position = (center_x + offset_x, center_y + offset_y)

    def update(self):
        """
        更新游戏逻辑，每帧调用一次。
        """
        # 更新倒计时器
        self.timer.update()

        # 检查倒计时是否结束
        if self.timer.time_up():
            self.is_game_over = True
            self.is_victory = False
            self.end_game()

        # 检查是否所有图案都已消除
        if all(pattern.is_cleared for pattern in self.patterns):
            self.is_game_over = True
            self.is_victory = True
            self.end_game()

    def end_game(self, player_name="Player1"):
        """
        处理游戏结束逻辑，记录分数和时间到排行榜。
        :param player_name: 玩家姓名
        """
        if self.is_game_over:
            score = self.player.score
            time_taken = self.timer.get_time_taken()
            self.leaderboard_manager.add_score(player_name, score, time_taken)
            print(f"游戏结束。得分：{score}，用时：{time_taken}秒。")
            # 可以在这里添加更多的结束游戏逻辑，例如显示结束界面等

    def handle_player_action(self, mouse_pos):
        """
        处理玩家的点击操作。

        :param mouse_pos: (x, y) 鼠标点击位置坐标
        """
        # 保存当前状态到历史记录
        self.save_state()

        # 查找点击位置对应的图案
        clicked_pattern = self.get_pattern_at_position(mouse_pos)
        self.hint_patterns.clear()
        if clicked_pattern:
            if clicked_pattern.is_selectable():
                self.player.select_pattern(clicked_pattern)
                # 将图案标记为已消除
                clicked_pattern.is_cleared = True

                # 检查玩家暂存区是否有三个相同的图案
                if self.player.check_for_match():
                    matched_patterns = self.player.remove_matched_patterns()
                    # 已在 remove_matched_patterns 中处理暂存区的图案

                # 检查暂存区是否已满
                if self.player.is_storage_full():
                    self.is_game_over = True
                    self.is_victory = False
            else:
                print("该图案被覆盖，无法选择。")
        self.hint_patterns.clear()

    def get_pattern_at_position(self, position):
        """
        根据位置获取对应的图案对象。

        :param position: (x, y) 坐标
        :return: Pattern 对象或 None
        """
        for layer in reversed(self.layers):  # 从顶层开始检查
            for pattern in layer:
                if pattern.contains_point(position) and not pattern.is_cleared:
                    # 检查图案是否未被覆盖
                    if not self.is_pattern_covered(pattern):
                        return pattern
        return None

    def is_pattern_covered(self, pattern):
        """
        判断图案是否被其他图案覆盖。

        :param pattern: Pattern 对象
        :return: bool
        """
        for higher_layer_index in range(pattern.layer + 1, len(self.layers)):
            higher_layer = self.layers[higher_layer_index]
            for other_pattern in higher_layer:
                if other_pattern.overlaps(pattern) and not other_pattern.is_cleared:
                    return True
        return False

    def save_state(self):
        """
        保存当前游戏状态到历史记录栈。
        """
        MAX_HISTORY = 10  # 设置最大历史记录数
        state = {
            'patterns': [(p.id, p.position, p.is_cleared) for p in self.patterns],
            'player_selected_patterns': [p.id for p in self.player.selected_patterns],
            'player_score': self.player.score,
            'player_storage': [p.id for p in self.player.storage],  # 修正为保存 storage
            'is_game_over': self.is_game_over,
            'is_victory': self.is_victory,
            'timer_remaining_time': self.timer.remaining_time,
            # 如果有更多需要保存的状态，可以继续添加
        }
        if len(self.history) >= MAX_HISTORY:
            self.history.pop(0)  # 移除最旧的历史记录
        self.history.append(copy.deepcopy(state))
        print("游戏状态已保存。")

    def restore_state(self):
        """
        从历史记录栈中恢复上一个游戏状态。
        """
        if not self.history:
            print("没有可撤销的操作。")
            return False

        state = self.history.pop()
        print("恢复游戏状态。")

        # 恢复图案状态
        for pattern, (pid, pos, is_cleared) in zip(self.patterns, state['patterns']):
            pattern.id = pid
            pattern.position = pos
            pattern.is_cleared = is_cleared

        # 恢复玩家选中的图案
        self.player.selected_patterns = [p for p in self.patterns if p.id in state['player_selected_patterns']]

        # 恢复玩家分数
        self.player.score = state.get('player_score', self.player.score)

        # 恢复玩家暂存区
        self.player.storage = [p for p in self.patterns if p.id in state.get('player_storage', [])]

        # 恢复游戏结束和胜利状态
        self.is_game_over = state['is_game_over']
        self.is_victory = state['is_victory']

        # 恢复倒计时
        self.timer.remaining_time = state['timer_remaining_time']

        return True
