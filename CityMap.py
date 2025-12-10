from contextlib import nullcontext
from typing import List

from Vertex import Vertex
from Point import Point
from ConstOfBuilds import *


class CityMap:
    """
    Объект CityMap включает в себя следующие поля:
    int vertCount - количество вершин многоугольника
    int infrastructureCount - количество различных видов инфраструктур
    int radii[infrastructureCount] - массив радиусов, каждой инфраструктуры
    int map[][] - матрица города. Договоримся о таких её элементах:
        -2 - ничего
        -1 - дорога
        0 - жилое здание
        1, 2, ..., infrastructureCount - соответствующий вид инфраструктуры
    """


    def __init__(self, vertCount: int, infrastructureCount: int, radii: List[int], fixed_size = False):
        from MapGenerator import MapGenerator
        self.vertCount = vertCount
        self.infrastructureCount = infrastructureCount
        self.radii = radii
        self.vertexes = None
        self.map = MapGenerator.generate_map(self, fixed_size)


    def setPoint(self, point: Point, value: int) -> None:
        """
        Данная функция меняет значение конкретной точки на карте на значение value
        """
        self.map[point.i][point.j] = value

    def getBuild(self, point: Point) -> int:
        """
        Данный метод возвращает тип здания
        """
        return self.map[point.i][point.j]