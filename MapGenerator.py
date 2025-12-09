import math
import random
from ConstOfBuilds import *
from Point import Point
from Vertex import Vertex



class MapGenerator:
    @staticmethod
    def generate_map(city_map) -> list[list[int]]:
        from JarvisAlgorithm import JarvisAlgorithm
        """
        Реализует алгоритм ГВМ:
        1. Расчет размеров по формуле из ТЗ.
        2. Метод окружности.
        3. Джарвис (существующий).
        4. Сканирующая строка.
        """


        if city_map.infrastructureCount > 0 and city_map.radii:
            avg_radius = sum(city_map.radii) / city_map.infrastructureCount
        else:
            avg_radius = 5  # Значение по умолчанию, если радиусов нет

        mapRadius = int(city_map.vertCount * avg_radius)
        sizeOfMatrix = mapRadius * 2

        # Создаем пустую матрицу
        city_map.map = [[VOID for _ in range(sizeOfMatrix)] for _ in range(sizeOfMatrix)]

        # --- 2. Метод окружности ---
        center_i = sizeOfMatrix // 2
        center_j = sizeOfMatrix // 2
        R = mapRadius - 2

        candidate_points = []
        for k in range(R):
            offset_primary = k
            offset_secondary = int(math.sqrt(R * R - k * k))

            signs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for si, sj in signs:

                p1 = Point(center_i + si * offset_primary, center_j + sj * offset_secondary)
                candidate_points.append(p1)

                p2 = Point(center_i + si * offset_secondary, center_j + sj * offset_primary)
                candidate_points.append(p2)

        unique_cords = list({(p.i, p.j) for p in candidate_points})
        count_to_pick = min(len(unique_cords), city_map.vertCount)
        selected_cords = random.sample(unique_cords, count_to_pick)


        for i, j in selected_cords:
            if 0 <= i < sizeOfMatrix and 0 <= j < sizeOfMatrix:
                city_map.map[i][j] = RES_BUILD


        JarvisAlgorithm.jarvis_algorithm(city_map)


        city_map.map = [[VOID for _ in range(sizeOfMatrix)] for _ in range(sizeOfMatrix)]


        raw_points = city_map.vertexes
        if not raw_points:
            return city_map.map

        hull_vertices = [Vertex(p.i, p.j) for p in raw_points]
        n = len(hull_vertices)

        for k in range(n):
            curr = hull_vertices[k]
            prev = hull_vertices[k - 1]
            nxt = hull_vertices[(k + 1) % n]

            curr.leftNeighborVert = nxt
            curr.rightNeighborVert = prev

        city_map.vertexes = hull_vertices

        imin = min(v.i for v in hull_vertices)
        imax = max(v.i for v in hull_vertices)

        for i in range(imin, imax + 1):
            intersections = []

            for k in range(n):
                v1 = hull_vertices[k]
                v2 = hull_vertices[(k + 1) % n]

                if min(v1.i, v2.i) <= i <= max(v1.i, v2.i) and v1.i != v2.i:

                    j = v1.j + (v2.j - v1.j) * (i - v1.i) / (v2.i - v1.i)
                    intersections.append(j)

            if intersections:
                j_start = math.ceil(min(intersections))
                j_end = math.floor(max(intersections))

                for j in range(j_start, j_end + 1):
                    if 0 <= i < sizeOfMatrix and 0 <= j < sizeOfMatrix:
                        # Четные - здания, остальные - дороги
                        if i % 2 == 0 and j % 2 == 0:
                            city_map.map[i][j] = RES_BUILD
                        else:
                            city_map.map[i][j] = ROAD

        return city_map.map