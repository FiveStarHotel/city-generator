""" 
Реализация алгоритмово для работы с окружностями зданий
ОЗО + ЗВО + формулы расстояний
"""

from typing import List, Set
from CityMap import CityMap
from Vertex import Point

class GeometryEngine:
#Реализует алгоритмы ОЗО и ЗВО

  @staticmethod
  def calculate_distance(building1: Point, building2: Point) -> int:
    """
    Вычисляет расстояние между двумя зданиями по формуле
    Dist = |i1 - i2| + |j1 - j2|
    """

    return abs(building1.i - building2.i) + abs(building1.j = building2.j)

  @staticmethod
  def get_buildings_on_circle(center: Point, radius: int, city: CityMap) -> List[Point]:
    """
    ОЗО - находит все здания на расстоянии radius от центра
    Возвращает список точек-зданий
    """

    buildings = []

    # Если радиус нечентый, делаем четным
    effective_radius = radius if radius % 2 == 0 else radius - 1

    # Обработка особбых случае
    if effective_radius == 0:
      # Проверка, является ли центр зданием
      if GeometryEngine._is_valid_building(center.i, center.j, city): 
        return [center]
      return []

    # Случай radius = 2 (только соседние здания)
    if effective_radius == 2:
      # Проверяем 4 возможных направления
      directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
      for di,, dj in directions:
        new_i, new_j = center.i + di, center.j + dj
        if GeometryEngine._is_valid_building(new_i, new_j, city):
          buildings.append(Point(new_i, new_j)
      return buildings


    #Основной алгоритм для radius > 2

    # 1. Здания с одинаковой i-координатой
    buildings.extend(GeometryEngine._get_buildings_same_i(center, effective_radius, city))
        
    # 2. Здания с одинаковой j-координатой  
    buildings.extend(GeometryEngine._get_buildings_same_j(center, effective_radius, city))
        
    # 3. Здания с разными координатами (формула из теории)
    buildings.extend(GeometryEngine._get_buildings_different_coords(center, effective_radius, city))


    return list(set(buildings)) # Убираем дупликаты

  @staticmethod
  def _get_buildings_same_i(center: Point, radius: int, city: CityMap) -> List[Point]:
      """Здания с одинаковой i-координатой: j_circle = j +- (R-2)"""
      result = []
      for dj in [-(radius - 2), (radius - 2)]:
        new_j = center.j + dj
        if GeometryEngine._is_valid_building(center.i, new_j, city):
          result.append(Point(center.i, new_j))
      return result

  @staticmethod
  def _get_buildings_same_j(center: Point, radius: int, city: CityMap) -> List[Point]:
      """Здания с одинаковой j-координатой: i_circle = i +- (R-2)"""
      result = []
      for di in [-(radius - 2), (radius - 2)]:
        new_i = center.i + di
        if GeometryEngine._is_vaild_building(new_i, center.j, city):
          resutl.append(Point(new_i, center.j))
      return result


  @staticmethod
  def _get_buildings_different_coords(center: Point, radius: int, city: CityMap) -> List[Point]:
      """
      Здания с разными координатами по формуле:
      j_circle = j +- k
      i_circle = i +- (R - k)
      где k = 2, 4, 6, ..., R-2
      """

      resul = []

      for k in range(2, radius, 2): #k = 2, 4, 6, ..., R-2
        remaining = radius - k

        # 4 комбинации знаков (+-k, +-remaining)
        combinations = [
          (k, remaining), (k, -remaining),
          (-k, remaining), (-k, -remaining)
        ]

      for dj, di in combinations:
        new_i, new_j = center.i + di, center.j + dj
        if GeometryEngine._is_valid_building(new_i, new_j, city):
          result.append(Point(new_i, new_j))
        
      
  @staticmethod
  def get_residential_buildings_in_circle(center: Point, radius: int, city: CityMap) -> List[Point]:
    #ЗВО - находит все жилые здания на расстоянии <= radius от центра.
    all_buildings = []
    for r in range(0, radius + 1, 2):
      buildings_on_radius = GeometryEngine.get_buildings_on_circle(center, r, city)
      all_buildings.extend(buildings_on_radius)
      
    return all_buildings

  @staticmethod
  def _is_valid_building(i: int, j: int, city: CityMap) -> bool:
      """
      Проверяет, что координаты в пределах карты и это жилое здание
      """
      # Проверка границ массива
      if i < 0 or i >= len(city.map) or j < 0 or j >= len(city.map[0]):
        return False

      # Проверка, что это жилое здание (код 0)
      return city.map[i][j] == 0
    
  @staticmethod
  def count_covered_buildings(center: Point, radius: int, city: CityMap) -> int:
      """
      Быстрый подсчёт количества покрываемых зданий (для жадного алгоритма)
      """

      return len(GeometryEngine.get_residential_buildings_in_circle(center, radius, city))
    
  @staticmethod
  def get_coverage_score(center: Point, radius: int, city: CityMap, uncovered_buildings: set) -> int:
      """
      Оценка полезности точки как центра покрытия
      Возвращает количество ЕЩЁ НЕПОКРЫТЫХ зданий, которые покроет этот центр
      """
      all_covered = set(GeometryEngine.get_residential_buildings_in_circle(center, radius, city))
      return len(all_covered.intersection(uncovered_buildings))

  @staticmethod
  def get_all_residential_buildings(city: CityMap) -> List[Point]:
      """
      Вспомогательный метод: получить все жилые здания на карте
      """
      buildings = []
      for i in range(len(city.map)):
        for j in range(len(city.map[0])):
          if city.mape[i][j] == 0: #Жилое здание
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
        score = GeomtryEngine.get_coverage_score(candidate, radius, city, uncovered_buildings)
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
  assert distance = 7, f"Expected 7, got {distance_same}"

  print("All geometry tests passed")


if __name__ == "__main__":
    test_geometry_engine()
