from gui import *
from enum import Enum


class Map:
    def __init__(self):
        pass

    def can_move(self, point1, point2):
        raise NotImplementedError("This must be implemented")

    def copy(self, copy):
        raise NotImplementedError("This must be implemented")


class PointStatus(Enum):
    empty = 0
    player_1 = 1
    player_2 = -1


point_size = 2
piece_size = 7


class Point:
    def get_color(self):
        if self.status == PointStatus.player_1:
            return Color.red
        elif self.status == PointStatus.player_2:
            return Color.blue
        else:
            return Color.black

    def get_size(self):
        if self.status == PointStatus.empty:
            return point_size
        else:
            return piece_size

    def __init__(self, x, y, status):
        self.status = status
        color = self.get_color()
        size = self.get_size()
        self.renderer = PointRenderer(x, y, size, color)

    def update(self, status):
        self.status = status
        color = self.get_color()
        size = self.get_size()
        self.renderer.radius = size
        self.renderer.color = color

    def render(self, surface):
        self.renderer.render(surface)

    def is_empty(self):
        return self.status == PointStatus.empty


class OriginalMap(Map):
    def __init__(self, x, y, width, height, rows, columns):
        super().__init__()
        self.rows, self.columns = rows, columns

        self.points = []
        row_step_size = height / rows
        column_step_size = width / columns
        for i in range(self.rows + 1):
            for j in range(self.columns + 1):
                self.points.append(Point(x + j * column_step_size, y + i * row_step_size, PointStatus.empty))

        self.connections = [[] for _ in range((self.rows + 1) * (self.columns + 1))]
        self.init_connections()

        self.renderer = MapRenderer(x, y, width, height, self)

    def is_point_valid(self, row, column):
        return 0 <= row <= self.rows and 0 <= column <= self.columns

    def point_to_id(self, row, column):
        return (self.columns + 1) * row + column

    def id_to_point(self, point_id):
        row = int(point_id / (self.columns + 1))
        column = point_id % (self.columns + 1)
        return row, column

    def assign_point(self, point_id, status):
        self.points[point_id].update(status)

    def connect_two_points(self, point1_id, point2_id):
        self.connections[point1_id].append(point2_id)
        self.connections[point2_id].append(point1_id)

    def init_connections(self):
        # vertical neighbours
        for i in range(self.rows):
            for j in range(self.columns + 1):
                point1 = self.point_to_id(i, j)
                point2 = self.point_to_id(i + 1, j)
                self.connect_two_points(point1, point2)

        # horizontal neighbours
        for j in range(self.columns):
            for i in range(self.rows + 1):
                point1 = self.point_to_id(i, j)
                point2 = self.point_to_id(i, j + 1)
                self.connect_two_points(point1, point2)

        # diagonal neighbours
        for i in range(0, self.rows + 1):
            for j in range(0, self.columns + 1):
                point1 = self.point_to_id(i, j)
                if (i + j) % 2 == 0:
                    if self.is_point_valid(i + 1, j + 1):
                        point2 = self.point_to_id(i + 1, j + 1)
                        self.connect_two_points(point1, point2)

                    if self.is_point_valid(i + 1, j - 1):
                        point2 = self.point_to_id(i + 1, j - 1)
                        self.connect_two_points(point1, point2)

    # point1 and point2 are point ids
    def is_connected(self, point1_id, point2_id):
        if point2_id in self.connections[point1_id]:
            assert point1_id in self.connections[point2_id]
            return True
        return False

    @staticmethod
    def distance(point1, point2):
        return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))

    def can_move(self, point1_id, point2_id):
        if not self.points[point2_id].is_empty() or self.points[point1_id].is_empty():
            return False

        point1 = self.id_to_point(point1_id)
        point2 = self.id_to_point(point2_id)
        distance = self.distance(point1, point2)

        if distance == 1:
            return self.is_connected(point1_id, point2_id)

        if distance == 2:
            if (point1[0] + point2[0]) % 2 == 0 and (point1[1] + point2[1]) % 2 == 0:
                middle_id = self.point_to_id(int((point1[0] + point2[0]) / 2), int((point1[1] + point2[1]) / 2))
                if self.is_connected(point1_id, middle_id) and self.is_connected(point2_id, middle_id):
                    if not self.points[point1_id].is_empty() and not self.points[middle_id].is_empty():
                        if self.points[point1_id].status != self.points[middle_id].status:
                            return True

        return False

    def apply_move(self, move):
        outcomes = []
        if self.can_move(move[0], move[1]):
            start_id = move[0]
            end_id = move[1]

            status = self.points[start_id].status

            self.points[start_id].update(PointStatus.empty)
            self.points[end_id].update(status)

            outcomes.append((start_id, end_id))

            point1 = self.id_to_point(start_id)
            point2 = self.id_to_point(end_id)
            distance = self.distance(point1, point2)

            if distance == 2:
                middle_id = self.point_to_id(int((point1[0] + point2[0]) / 2), int((point1[1] + point2[1]) / 2))
                self.points[middle_id].update(PointStatus.empty)
                outcomes.append((middle_id, -1))
        return outcomes

    def render(self, surface):
        self.renderer.render(surface)
        for point in self.points:
            point.render(surface)

    def copy(self, copy):
        counter = 0
        for i in range(self.rows + 1):
            for j in range(self.columns + 1):
                copy.points[counter].update(self.points[counter].status)
                counter += 1


