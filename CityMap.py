from contextlib import nullcontext

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


    def __init__(self, vertCount: int, infrastructureCount: int, radii: int[int]):
        self.vertCount = vertCount
        self.infrastructureCount = infrastructureCount
        self.radii = radii
        self.vertexes = self.getVertexes()
        self.map = self.createMap()


    def createMap(self) -> int[int][int]:
        """
        Данный метод создает квадратную матрицу, которая и будет являться нашей картой.
        Размер матрицы можно определить так: mapRadius * 2, где mapRadius - радиус выпуклого многоугольника
        mapRadius можно определить как vertCount * arithmeticMean(radii), где arithmeticMean - среднее арифметическое
        Центр окружности размещается в центре матрицы. Идём по окружности и случайно выбираем вершины на чётных координатах
        Также сохраняем координаты вершин и их соседей: vertexes[vertCount] = {Vertex vertex1, ...}
        """
        mapRadius = self.vertCount * (sum(self.radii) / self.infrastructureCount)
        sizeOfMatrix = mapRadius * 2
        cityMap = [[VOID for _ in range(0, sizeOfMatrix)] for _ in range(0, sizeOfMatrix)]

        #TODO: Закончить алгоритм ГВМ

        pass

    def getVertexes(self) -> int[int]:
        """
        Здесь будет происходить начальный поиск вершин карты
        """
        pass

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