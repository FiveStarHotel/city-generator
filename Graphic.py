import pygame
import colorsys
from CityMap import CityMap
from ConstOfBuilds import *
from CoverageSolver import CoverageSolver

def paint_city(city: CityMap):
    textures ={
        VOID: {"type" : "color", "value" : (255, 255, 255), "text" : ""},
        ROAD: {"type" : "image", "value" :  "icons/road.png", "text" : "Дорога"},
        RES_BUILD: {"type" : "image", "value" :  "icons/res_build.png", "text" : "Жилой дом"}
    }
    textures.update(_generate_color(city.infrastructureCount))

    size = len(city.map)
    CELL = 1060 // (size*1.3)
    legend_size = CELL * 11
    pygame.init()

    screen = pygame.display.set_mode((size * CELL + legend_size, size * CELL))
    pygame.display.set_caption("Генерация города")

    font = pygame.font.SysFont("Arial", int (CELL))

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

        legend_x = size * CELL + 10
        legend_y = 10
        line_h = 30

        pygame.draw.rect(screen, (250, 250, 250), (size * CELL, 0, legend_size, size * CELL))

        for key, obj in textures.items():
            rect = (legend_x, legend_y, 20, 20)

            if obj["type"] == "color":
                pygame.draw.rect(screen, obj["value"], rect)
            else:
                screen.blit(obj["image"], rect)

            text = font.render(obj["text"], True, (0, 0, 0))
            screen.blit(text, (legend_x + 30, legend_y))

            legend_y += line_h

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
            "value" : (int(r * 255),int(g * 255),int(b * 255)),
            "text" : f"{i}-й тип строения"
        }
    return colors

if __name__ == '__main__':
    city = CityMap(5, 1, [4])
    CoverageSolver.solverMethod(city)
    paint_city(city)