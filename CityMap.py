from Vertex import Vertex

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
        self.map = self.createMap()

    def createMap(self):
        """
        createMap() -> int[n][n]

        Данный метод создает квадратную матрицу, которая и будет являться нашей картой.
        Размер матрицы можно определить так: mapRadius * 2, где mapRadius - радиус выпуклого многоугольника
        mapRadius можно определить как vertCount * arithmeticMean(radii), где arithmeticMean - среднее арифметическое
        Центр окружности размещается в центре матрицы. Идём по окружности и случайно выбираем вершины на чётных координатах
        Также сохраняем координаты вершин и их соседей: vertexes[vertCount] = {Vertex vertex1, ...}
        """
        pass
