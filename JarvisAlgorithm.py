from CityMap import CityMap
from ConstOfBuilds import *
from Point import Point

# Тестовые данные
# class _CityMapTest:
#     def __init__(self):
#         self.map = [
#             [-2 , -2 , -2 , -2 , -2 , -2 ],
#             [-2 ,  0,  -2,   0 , -2 , -2 ],
#             [-2 ,  0,   1 ,  0 , -2 , -2 ],
#             [-2 , -3 , -3,   0 , -2,  -2 ],
#             [-2 ,  0 ,  0,   0,  -2,  -2 ],
#             [-2 , -2,  -2,  -2,  -2,  -2 ]
#         ]
#
#         self.vertexes = None

class JarvisAlgorithm:
    @staticmethod
    def jarvis_algorithm(self, city_map: CityMap):
        points = JarvisAlgorithm._get_res_points(city_map)
        points_amount = len(points)

        if points_amount < 3:
            city_map.vertexes = points
            return

        start_point = sorted(points, key=lambda point: (point.j, -point.i))[0]

        vertexes = []
        current_point: Point = start_point

        while True:
            vertexes.append(current_point)

            next_candidate: Point = points[0]

            for point in points:
                if point == current_point:
                    continue

                vector_multiplication_res = JarvisAlgorithm._rotate(current_point.get_tuple(), next_candidate.get_tuple(), point.get_tuple())

                if next_candidate == current_point or vector_multiplication_res > 0:
                    next_candidate = point

            current_point = next_candidate

            if current_point == start_point:
                break

        city_map.vertexes = vertexes

    @staticmethod
    def _get_res_points(city_map: CityMap):
        """
        Возвращает список точек (объекты Point), на которых располагаются жилые здания (RES_BUILD)
        """
        points = []
        for i in range(len(city_map.map)):
            for j in range(len(city_map.map[i])):
                if city_map.map[i][j] == RES_BUILD:
                    points.append(Point(i, j))
        return points

    @staticmethod
    def _rotate(A, B, C):
        """
        A, B, C - точки в виде кортежа (x,y)

        Возвращает:
        Что-то типа векторного произведения. Результат необходим для расчета, в какой стороне находится вектор
        (-n - слева, 0 - коллинеарны, n - справа)
        """
        return (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])
