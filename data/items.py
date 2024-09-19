# data/items.py

class ItemManager:
    """
    道具管理类，实现道具的功能和使用逻辑。
    """

    def __init__(self, hint_limit, undo_limit):
        """
        初始化道具管理器。

        :param hint_limit: int，提示道具的使用次数限制
        :param undo_limit: int，撤销道具的使用次数限制
        """
        self.hint_limit = hint_limit
        self.undo_limit = undo_limit
        self.hint_used = 0
        self.undo_used = 0
        print(f"ItemManager initialized with hint_limit={hint_limit}, undo_limit={undo_limit}")

    def can_use_hint(self):
        """
        检查是否可以使用提示道具。
        :return: bool
        """
        can_use = self.hint_used < self.hint_limit
        print(f"Checking can_use_hint: {self.hint_used} / {self.hint_limit} -> {can_use}")
        return can_use

    def use_hint(self, game_logic):
        """
        使用提示道具，显示一个可消除的图案组合。

        :param game_logic: GameLogic 对象，游戏逻辑实例
        :return: list，包含提示的图案对象
        """
        if self.can_use_hint():
            hint = game_logic.find_hint()
            if hint:
                self.hint_used += 1
                print(f"使用提示道具，剩余次数：{self.hint_limit - self.hint_used}")
                return hint
            else:
                print("没有可用的提示。")
        else:
            print("提示道具已用完。")
        return None

    def can_use_undo(self):
        """
        检查是否可以使用撤销道具。
        :return: bool
        """
        can_use = self.undo_used < self.undo_limit
        print(f"Checking can_use_undo: {self.undo_used} / {self.undo_limit} -> {can_use}")
        return can_use

    def use_undo(self, player):
        """
        使用撤销道具，撤销上一次的图案选择。

        :param player: Player 对象，玩家实例
        :return: bool，表示是否成功使用撤销道具
        """
        if self.can_use_undo():
            success = player.undo()
            if success:
                self.undo_used += 1
                print(f"使用撤销道具，剩余次数：{self.undo_limit - self.undo_used}")
                return True
            else:
                print("无法撤销。")
        else:
            print("撤销道具已用完。")
        return False

    def reset_items(self):
        """
        重置道具使用次数（例如在新游戏开始时）。
        """
        self.hint_used = 0
        self.undo_used = 0
        print("ItemManager 的道具使用次数已重置。")
