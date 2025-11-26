import copy

from CityMap import CityMap
from Point import Point
from GeometryEngine import GeometryEngine
from ConstOfBuilds import *


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
            for center in GeometryEngine.get_buildings_on_circle(vertex, currentCity.radii[indOfInfrastructure], currentCity):
                listOfCenters.append((center,
                                      GeometryEngine.count_covered_buildings(center,
                                                                             currentCity.radii[indOfInfrastructure],
                                                                             currentCity)))
        betterCenter = max(listOfCenters, key=lambda x: x[1])[0]
        currentCity.setPoint(betterCenter, indOfInfrastructure)
        CoverageSolver.coverageBuildingsInCircle(betterCenter, currentCity.radii[indOfInfrastructure], currentCity)

    @staticmethod
    def solverMethod(city: CityMap):
        """
        Итоговый метод дял оптимального покрытия
        """

        for infrastructure in range(0, city.infrastructureCount):
            cityCopy = copy.deepcopy(city)
            while RES_BUILD in cityCopy.map:
                CoverageSolver.iterationSolution(cityCopy, infrastructure)
                if RES_BUILD not in cityCopy.map:
                    break
                #TODO Метод Джарвиса
            for i in range(0, len(city.map)):
                for j in range(0, len(city.map[i])):
                    point = Point(i, j)
                    if cityCopy.getBuild(point) == infrastructure:
                        city.setPoint(point, infrastructure)