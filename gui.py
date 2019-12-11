import pygame
import pygame.gfxdraw


class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)


class Renderer:
    def render(self, surface):
        raise NotImplementedError("This should be implemented")


class MapRenderer(Renderer):
    def __init__(self, x, y, width, height, map, color=Color.black, radius=2):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color

        self.row_step_size = self.height / map.rows
        self.column_step_size = self.width / map.columns

        self.radius = radius
        self.map = map

    def get_intersection_point(self, row, column):
        left = self.x + column * self.column_step_size
        top = self.y + row * self.row_step_size
        return left, top

    def render(self, surface):
        for i in range(len(self.map.connections)):
            for j in self.map.connections[i]:
                start_point = self.map.id_to_point(i)
                end_point = self.map.id_to_point(j)

                start = self.get_intersection_point(start_point[0], start_point[1])
                end = self.get_intersection_point(end_point[0], end_point[1])
                pygame.draw.line(surface, self.color, start, end)

        for i in range(len(self.map.connections)):
            center_point = self.map.id_to_point(i)
            center = self.get_intersection_point(center_point[0], center_point[1])
            center = [int(x) for x in center]
            pygame.gfxdraw.aacircle(surface, center[0], center[1], self.radius, self.color)
            pygame.gfxdraw.filled_circle(surface, center[0], center[1], self.radius, self.color)


class PointRenderer(Renderer):
    def __init__(self, x, y, radius, color=Color.black):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def move(self, point):
        self.x, self.y = point

    def render(self, surface):
        center = (int(self.x), int(self.y))
        pygame.gfxdraw.aacircle(surface, center[0], center[1], self.radius, self.color)
        pygame.gfxdraw.filled_circle(surface, center[0], center[1], self.radius, self.color)
