import copy

from CityMap import CityMap
from Point import Point
from GeometryEngine import GeometryEngine
from ConstOfBuilds import *
from JarvisAlgorithm import JarvisAlgorithm

class CoverageSolver:

    @staticmethod
    def coverageBuildingsInCircle(center: Point, radius: int, city: CityMap) -> None:
        """
        Метод для покрытия точек внутри круга вокруг центра
        """
        for point in GeometryEngine.get_residential_buildings_in_circle(center, radius, city):
            if city.getBuild(point) == RES_BUILD:
                city.setPoint(point, COVERED)


    @staticmethod
    def iterationSolution(currentCity: CityMap, indOfInfrastructure:int) -> None:
        """
        Метод итерации для покрытия
        """
        listOfCenters = []
        for vertex in currentCity.vertexes:
            for center in GeometryEngine.get_buildings_on_circle(vertex, currentCity.radii[indOfInfrastructure-1], currentCity):
                listOfCenters.append((center,
                                      GeometryEngine.count_covered_buildings(center,
                                                                             currentCity.radii[indOfInfrastructure-1],
                                                                             currentCity)))
        if not listOfCenters:
            for vertex in currentCity.vertexes:
                listOfCenters.append((vertex,
                                      GeometryEngine.count_covered_buildings(vertex,
                                                                             currentCity.radii[indOfInfrastructure-1],
                                                                             currentCity)))
        betterCenter = max(listOfCenters, key=lambda x: x[1])[0]
        currentCity.setPoint(betterCenter, indOfInfrastructure)
        CoverageSolver.coverageBuildingsInCircle(betterCenter, currentCity.radii[indOfInfrastructure-1], currentCity)

    @staticmethod
    def solverMethod(city: CityMap):
        """
        Итоговый метод дял оптимального покрытия
        """

        for infrastructure in range(1, city.infrastructureCount+1):
            cityCopy = copy.deepcopy(city)
            while any(RES_BUILD in row for row in cityCopy.map):
                CoverageSolver.iterationSolution(cityCopy, infrastructure)
                JarvisAlgorithm.jarvis_algorithm(cityCopy)
                if all(RES_BUILD not in row for row in cityCopy.map):
                    break
            for i in range(0, len(city.map)):
                for j in range(0, len(city.map[i])):
                    point = Point(i, j)
                    if cityCopy.getBuild(point) == infrastructure:
                        city.setPoint(point, infrastructure)