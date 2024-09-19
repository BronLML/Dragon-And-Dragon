# core/player.py

class Player:
    """
    玩家类，管理玩家的选择和存储区。
    """

    def __init__(self, storage_limit):
        """
        初始化玩家。

        :param storage_limit: int，存储区的容量限制
        """
        self.storage_limit = storage_limit
        self.selected_patterns = []  # 已选中的图案列表
        self.storage = []            # 玩家暂存区
        self.score = 0               # 玩家得分

    def select_pattern(self, pattern):
        """
        选择一个图案并添加到暂存区。

        :param pattern: Pattern 对象，玩家选择的图案
        """
        if not self.is_storage_full():
            self.selected_patterns.append(pattern)
            self.storage.append(pattern)
            print(f"选择了图案 ID: {pattern.id}")
        else:
            print("暂存区已满，无法选择更多图案。")

    def check_for_match(self):
        """
        检查暂存区是否有三个相同的图案。

        :return: bool，是否有匹配
        """
        pattern_ids = [p.id for p in self.storage]
        for pid in set(pattern_ids):
            if pattern_ids.count(pid) >= 3:
                return True
        return False

    def remove_matched_patterns(self):
        """
        移除暂存区中匹配的图案。

        :return: list，已移除的图案对象
        """
        pattern_ids = [p.id for p in self.storage]
        matched_id = None
        for pid in set(pattern_ids):
            if pattern_ids.count(pid) >= 3:
                matched_id = pid
                break

        if matched_id is not None:
            matched_patterns = [p for p in self.storage if p.id == matched_id][:3]
            for p in matched_patterns:
                self.storage.remove(p)
                self.selected_patterns.remove(p)
            self.score += 10  # 增加分数，可以根据需要调整
            print(f"消除了图案 ID: {matched_id}，得分增加到 {self.score}")
            return matched_patterns
        return []

    def is_storage_full(self):
        """
        检查暂存区是否已满。

        :return: bool，是否已满
        """
        return len(self.storage) >= self.storage_limit

    def undo(self):
        """
        撤销上一步的图案选择和操作。

        :return: bool，表示是否成功撤销
        """
        if self.selected_patterns:
            last_pattern = self.selected_patterns.pop()
            last_pattern.is_cleared = False  # 恢复图案为未消除状态
            print(f"撤销图案 ID: {last_pattern.id}")
            return True
        else:
            print("没有可撤销的图案。")
            return False