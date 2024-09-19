# ui/utils.py

import pygame

class Button:
    """
    按钮类，创建可点击的文字按钮或图形按钮。
    """

    def __init__(self, screen, text='', position=(0, 0), size=(40, 40), font_size=24, font_name="Arial",
                 bg_color=(0, 0, 0), text_color=(255, 255, 255), image=None, shape='rect'):
        """
        初始化按钮。

        :param screen: pygame.Surface，绘制按钮的屏幕
        :param text: str，按钮上显示的文本
        :param position: (x, y)，按钮的中心位置
        :param size: (width, height)，按钮的尺寸
        :param font_size: int，字体大小
        :param font_name: str，字体名称
        :param bg_color: tuple，按钮背景颜色（默认为黑色）
        :param text_color: tuple，按钮文字颜色（默认为白色）
        :param image: pygame.Surface，按钮的背景图片
        :param shape: str，按钮的形状（'rect'、'circle'、'cloud'）
        """
        self.screen = screen
        self.text = text
        self.position = position
        self.size = size
        self.font = pygame.font.SysFont(font_name, font_size, bold=True)  # 使用指定的字体
        self.bg_color = bg_color  # 按钮背景颜色
        self.text_color = text_color  # 按钮文字颜色
        self.image = image  # 按钮背景图片
        self.shape = shape  # 按钮形状

        # 创建按钮的矩形区域
        self.rect = pygame.Rect(0, 0, *self.size)
        self.rect.center = self.position

    def draw(self):
        """
        绘制按钮，包括背景颜色和文字。
        """
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.is_clicked(mouse_pos)

        if self.image:
            # 如果有背景图片，直接绘制图片
            self.screen.blit(self.image, self.rect)
        else:
            if self.shape == 'rect':
                # 根据是否悬停改变背景颜色
                color = self.bg_color
                if is_hovered:
                    color = tuple(min(255, c + 30) for c in self.bg_color)  # 变亮
                pygame.draw.rect(self.screen, color, self.rect)
            elif self.shape == 'circle':
                # 绘制圆形按钮
                color = self.bg_color
                if is_hovered:
                    color = tuple(min(255, c + 30) for c in self.bg_color)
                pygame.draw.circle(self.screen, color, self.position, self.size[0] // 2)
            elif self.shape == 'cloud':
                # 绘制简易云朵形状
                color = self.bg_color
                if is_hovered:
                    color = tuple(min(255, c + 30) for c in self.bg_color)
                x, y = self.position
                w, h = self.size
                radius = h // 2
                # 左圆
                pygame.draw.circle(self.screen, color, (x - w // 4, y), radius)
                # 右圆
                pygame.draw.circle(self.screen, color, (x + w // 4, y), radius)
                # 中间矩形
                pygame.draw.rect(self.screen, color, (x - w // 4, y - h // 2, w // 2, h))
            else:
                # 默认绘制矩形按钮
                color = self.bg_color
                if is_hovered:
                    color = tuple(min(255, c + 30) for c in self.bg_color)
                pygame.draw.rect(self.screen, color, self.rect)

        # 绘制按钮文本
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.position)
            self.screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        """
        判断按钮是否被点击。

        :param mouse_pos: (x, y)，鼠标点击位置
        :return: bool
        """
        if self.shape == 'circle':
            # 检查点击是否在圆形按钮内
            x, y = self.position
            dx = mouse_pos[0] - x
            dy = mouse_pos[1] - y
            distance_squared = dx * dx + dy * dy
            radius = self.size[0] // 2
            return distance_squared <= radius * radius
        else:
            # 检查点击是否在矩形或云朵按钮内
            return self.rect.collidepoint(mouse_pos)
