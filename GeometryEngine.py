""" 
Реализация алгоритмов для работы с окружностями зданий
ОЗО + ЗВО + формулы расстояний
"""

from typing import List, Set
from CityMap import CityMap
from Vertex import Vertex
from Point import Point
from ConstOfBuilds import *

class GeometryEngine:
#Реализует алгоритмы ОЗО и ЗВО

  @staticmethod
  def calculate_distance(building1: Point, building2: Point) -> int:
    """
    Вычисляет расстояние между двумя зданиями по формуле
    Dist = |i1 - i2| + |j1 - j2|
    """

    return abs(building1.i - building2.i) + abs(building1.j - building2.j)


  @staticmethod
  def get_buildings_on_circle(center: Point, radius: int, city: CityMap) -> List[Point]:
    """
    ОЗО - находит все здания на расстоянии radius от центра
    Возвращает список точек-зданий
    """

    buildings = set()

    # Если радиус нечётный, делаем четным
    effective_radius = radius if radius % 2 == 0 else radius - 1

    # Обработка особых случае
    if effective_radius == 0:
      # Проверка, является ли центр зданием
      if GeometryEngine._is_valid_building(center.i, center.j, city):
        return [center]
      return []
  #Проверка соседних зданий:
    if effective_radius == 2:
      directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
      for di, dj in directions:
          new_i, new_j = center.i + di, center.j + dj
          if GeometryEngine._is_valid_building(new_i, new_j, city):
            buildings.add(Point(new_i, new_j))
      return list(buildings)
      
   # Общий случай: перебираем все возможные точки на "окружности"
  # Для манхэттенского расстояния |di| + |dj| = effective_radius
    
    # Перебираем все возможные di (только четные)
    for di in range(-effective_radius, effective_radius + 1, 2):
        # Вычисляем соответствующие dj
        dj_positive = effective_radius - abs(di)
        dj_negative = -dj_positive
        
        # Проверяем обе возможные точки для каждого di
        # Используем set для уникальных dj значений
        unique_dj = {dj_positive, dj_negative}  # Автоматически убераем дубликаты
        for dj in unique_dj:
        # проверка точки
            new_i = center.i + di
            new_j = center.j + dj
            
            # Проверяем, что это валидное здание
            if GeometryEngine._is_valid_building(new_i, new_j, city):
                buildings.add(Point(new_i, new_j))
    
    return list(buildings)
      
  @staticmethod
  def get_residential_buildings_in_circle(center: Point, radius: int, city: CityMap) -> List[Point]:
    #ЗВО - находит все жилые здания на расстоянии <= radius от центра.
    buildings_set = set()  # Используем set для уникальности
    for r in range(0, radius + 1, 2):
        buildings_on_radius = GeometryEngine.get_buildings_on_circle(center, r, city)
        for point in buildings_on_radius:
            buildings_set.add((point.i, point.j))  # Храним как кортеж для уникальности
    
    # Преобразуем обратно в список Point
    return [Point(i, j) for i, j in buildings_set]

  @staticmethod
  def _is_valid_building(i: int, j: int, city: CityMap) -> bool:
      """
      Проверяет, что координаты в пределах карты и это жилое здание
      """
      # Проверка границ массива
      if i < 0 or i >= len(city.map) or j < 0 or j >= len(city.map[0]):
        return False

      # Проверка, что это жилое здание (код константы)
      return city.map[i][j] == RES_BUILD
    
  @staticmethod
  def count_covered_buildings(center: Point, radius: int, city: CityMap) -> int:
      """
      Быстрый подсчёт количества покрываемых зданий (для жадного алгоритма)
      """
      return sum(city.getBuild(point) == RES_BUILD for point in GeometryEngine.get_residential_buildings_in_circle(center, radius, city))
    
  @staticmethod
  def get_coverage_score(center: Point, radius: int, city: CityMap, uncovered_buildings: set) -> int:
      """
      Оценка полезности точки как центра покрытия
      Возвращает количество ЕЩЁ НЕПОКРЫТЫХ зданий, которые покроет этот центр
      """
      all_covered = set(GeometryEngine.get_residential_buildings_in_circle(center, radius, city))
    
      # Преобразуем Point в кортежи для сравнения
      covered_tuples = {(p.i, p.j) for p in all_covered}
    
      return len(covered_tuples.intersection(uncovered_buildings))

  @staticmethod
  def get_all_residential_buildings(city: CityMap) -> List[Point]:
      """
      Вспомогательный метод: получить все жилые здания на карте
      """
      buildings = []
      for i in range(len(city.map)):
        for j in range(len(city.map[0])):
          if city.map[i][j] == RES_BUILD: #Константа
            buildings.append(Point(i, j))
      return buildings
    
  @staticmethod
  def find_best_coverage_center(candidates: List[Point], radius: int, city: CityMap, uncovered_buildings: set) -> Point:
      """
      Находит лучшую точку из кандидатов для размещения инфраструктуры
      Возвращает точку с максимальным coverage_score
      """
      best_center = None
      best_score = -1

      for candidate in candidates:
        score = GeometryEngine.get_coverage_score(candidate, radius, city, uncovered_buildings)
        if score > best_score:
          best_score = score
          best_center = candidate

      return best_center

# Тестовые функции
def test_geometry_engine():
  """
  Тестирование основных функций GeometryEngine
  """
  print("Testing GeometryEngine...")

  # Тест расстояния
  p1 = Point(2, 3)
  p2 = Point(5, 7)
  distance = GeometryEngine.calculate_distance(p1, p2)
  print(f"Distance between {p1} and {p2}: {distance}")
  assert distance == 7, f"Expected 7, got {distance}"

  # Тест с одинаковыми точками
  p3 = Point(4, 4)
  distance_same = GeometryEngine.calculate_distance(p3, p3)
  print(f"Distance between same point: {distance_same}")
  assert distance_same == 0, f"Expected 0, got {distance_same}"
  
  print("All geometry tests passed")


if __name__ == "__main__":
    test_geometry_engine()
