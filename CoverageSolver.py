import copy

from CityMap import CityMap
from GeometryEngine import GeometryEngine


class CoverageSolver:

    COVERED = -3

    @staticmethod
    def iterationSolution(city: CityMap, indOfInfrastructure:int) -> CityMap:
        #TODO переделать правильно алгоритм
        currentCity = copy.deepcopy(city)
        listOfCenters = []
        for vertex in currentCity.vertexes:
            for center in GeometryEngine.get_buildings_on_circle(vertex, currentCity.radii[indOfInfrastructure], currentCity):
                listOfCenters.append((center,
                                      len(GeometryEngine.get_residential_buildings_in_circle(center, currentCity.radii[indOfInfrastructure], currentCity))))
        betterCenter = max(listOfCenters, key=lambda x: x[1])[0]
        pass