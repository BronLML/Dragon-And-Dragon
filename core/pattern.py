class Pattern:
    """
    图案类，表示游戏中的每一个图案。
    """

    def __init__(self, id, size):
        """
        初始化图案对象。

        :param id: int，图案的标识符
        :param size: (width, height)，图案尺寸
        """
        self.id = id                  # 图案类型ID
        self.layer = 0                # 所在层级
        self.position = (0, 0)        # 位置坐标
        self.size = size              # 图案尺寸
        self.is_cleared = False       # 是否已被消除

    def contains_point(self, pos):
        """
        检查鼠标位置是否在图案范围内。
        :param pos: (x, y) 鼠标坐标
        :return: bool
        """
        x, y = self.position
        width, height = self.size
        rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        return rect.collidepoint(pos)

    def is_selectable(self):
        """
        判断图案是否可被选择（未被覆盖）。

        :return: bool
        """
        return not self.is_cleared

    def contains_point(self, point):
        """
        判断图案是否包含指定的点（用于检测点击）。

        :param point: (x, y) 坐标
        :return: bool
        """
        x, y = self.position
        width, height = self.size
        left = x - width / 2
        right = x + width / 2
        top = y - height / 2
        bottom = y + height / 2
        px, py = point
        return left <= px <= right and top <= py <= bottom

    def overlaps(self, other):
        """
        判断本图案是否与其他图案重叠。

        :param other: Pattern 对象
        :return: bool
        """
        x1, y1 = self.position
        w1, h1 = self.size
        x2, y2 = other.position
        w2, h2 = other.size

        left1 = x1 - w1 / 2
        right1 = x1 + w1 / 2
        top1 = y1 - h1 / 2
        bottom1 = y1 + h1 / 2

        left2 = x2 - w2 / 2
        right2 = x2 + w2 / 2
        top2 = y2 - h2 / 2
        bottom2 = y2 + h2 / 2

        return not (right1 <= left2 or right2 <= left1 or bottom1 <= top2 or bottom2 <= top1)
