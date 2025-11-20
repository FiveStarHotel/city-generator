from Point import Point

class Vertex(Point):
    """
    Объект Vertex содержит следующие поля:
    x, y - координаты вершины   !(i -> y, j -> x)!
    rightNeighborVert, leftNeighborVert - правая и левая соседняя вершина соответственно
        Направление смотрится так, будто вершина смотрит в центр
    """

    def __init__(self, i: int, j: int):
        super().__init__(i, j)
        self.__rightNeighborVert = None
        self.__leftNeighborVert = None

    @property
    def rightNeighborVert(self):
        return self.__rightNeighborVert

    @rightNeighborVert.setter
    def rightNeighborVert(self, vert):
        self.__rightNeighborVert = vert

    @property
    def leftNeighborVert(self):
        return self.__leftNeighborVert

    @leftNeighborVert.setter
    def leftNeighborVert(self, vert):
        self.__leftNeighborVert = vert

    @staticmethod
    def highestVertex(vertexes):
        highVert = vertexes[0]
        for vertex in vertexes:
            if vertex.y >= highVert.y:
                highVert = vertex
        return highVert

    @staticmethod
    def lowestVertex(vertexes):
        lowestVert = vertexes[0]
        for vertex in vertexes:
            if vertex.y <= lowestVert.y:
                lowestVert = vertex
        return lowestVert