import pygame
import random

pygame.init()

class DrawingInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GRAY = 128, 128, 128
    BG_COLOR = BLACK

    HOR_PADDING = 100
    VER_PADDING = 100

    def __init__(self, width, height, list):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")

        self.set_list(list)

    def set_list(self, list):
        self.list = list
        self.min_val = min(list)
        self.max_val = max(list)

        self.bar_width = round((self.width - self.HOR_PADDING) / len(list))
        self.bar_height = round((self.height - self.VER_PADDING) / (self.max_val - self.min_val))

        self.start_x = self.HOR_PADDING // 2
        
def gen_list(n, min_val, max_val):
    list = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        list.append(val)

    return list

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    list = gen_list(n, min_val, max_val)
    draw_info = DrawingInfo(800, 600, list)

    while run:
        clock.tick(60)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
    pygame.quit()


if __name__ == "__main__":
    main()