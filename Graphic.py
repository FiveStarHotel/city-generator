import pygame
import colorsys
from CityMap import CityMap
from ConstOfBuilds import *
from CoverageSolver import CoverageSolver

def paint_city(city: CityMap):
    textures ={
        VOID: {"type" : "color", "value" : (255, 255, 255)},
        ROAD: {"type" : "image", "value" :  "icons/road.png"},
        RES_BUILD: {"type" : "image", "value" :  "icons/res_build.png"}
    }
    textures.update(_generate_color(city.infrastructureCount))

    size = len(city.map)
    CELL = 1060 // (size*1.3)
    pygame.init()

    screen = pygame.display.set_mode((size * CELL, size * CELL))
    pygame.display.set_caption("Генерация города")

    _load_assets(textures, CELL)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- рисуем карту ---
        for y in range(size):
            for x in range(size):
                cell_value = city.map[y][x]
                obj = textures[cell_value]

                if obj["type"] == "color":
                    pygame.draw.rect(
                        screen, obj["value"],
                        (x * CELL, y * CELL, CELL, CELL)
                    )
                elif obj["type"] == "image":
                    pygame.draw.rect(
                        screen, VOID,
                        (x * CELL, y * CELL, CELL, CELL)
                    )
                    screen.blit(
                        obj["image"],
                        (x * CELL, y * CELL)
                    )

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def _load_assets(types_dict, cell_size):
    for key, obj in types_dict.items():
        if obj["type"] == "image":
            img = pygame.image.load(obj["value"]).convert_alpha()
            obj["image"] = pygame.transform.scale(img, (cell_size, cell_size))

def _generate_color(count: int):
    colors = {}
    for i in range(1, count+1):
        hue = i/count
        r, g, b = colorsys.hsv_to_rgb(hue, 0.6, 0.95)
        colors[i] = {
            "type": "color",
            "value" : (int(r * 255),int(g * 255),int(b * 255))
        }
    return colors

if __name__ == '__main__':
    city = CityMap(5, 1, [4])
    CoverageSolver.solverMethod(city)
    paint_city(city)