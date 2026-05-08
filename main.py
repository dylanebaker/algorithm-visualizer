import pygame
import random
import math
import numpy as np

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

SAMPLE_RATE = 44100
VOLUME = 0.0005

def _make_sound_array(wave):
    _, _, channels = pygame.mixer.get_init()
    if channels == 1:
        return wave
    return np.column_stack([wave] * channels).astype(np.int16)

def play_tone(value, min_val, max_val, duration_ms=40):
    freq = 200 + (value - min_val) / (max_val - min_val) * 600
    num_samples = int(SAMPLE_RATE * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, num_samples, endpoint=False)
    wave = (np.sin(2 * np.pi * freq * t) * 32767 * VOLUME).astype(np.int16)
    sound = pygame.sndarray.make_sound(_make_sound_array(wave))
    sound.play()

def play_complete():
    notes = [523, 659, 784, 1047]
    for freq in notes:
        num_samples = int(SAMPLE_RATE * 0.1)
        t = np.linspace(0, 0.1, num_samples, endpoint=False)
        wave = (np.sin(2 * np.pi * freq * t) * 32767 * VOLUME).astype(np.int16)
        sound = pygame.sndarray.make_sound(_make_sound_array(wave))
        sound.play()
        pygame.time.wait(100)

class DrawingInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 100, 220, 100
    RED = 220, 80, 80
    GRAY = 128, 128, 128
    BG_COLOR = (18, 18, 18)

    GRADIENTS = [
        (74, 117, 176),
        (99, 155, 215),
        (124, 179, 234)
    ]

    FONT = pygame.font.Font('QuinqueFiveFont.ttf', 16)
    LARGE_FONT = pygame.font.Font('QuinqueFiveFont.ttf', 24)
    SMALL_FONT = pygame.font.Font('QuinqueFiveFont.ttf', 12)
    MUTED = (160, 160, 160)
    HOR_PADDING = 200
    VER_PADDING = 200

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
        self.bar_height = math.floor((self.height - self.VER_PADDING) / (self.max_val - self.min_val))

        self.start_x = self.HOR_PADDING // 2
        
def gen_list(n, min_val, max_val):
    list = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        list.append(val)

    return list

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BG_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.WHITE)
    controls = draw_info.SMALL_FONT.render("R - Reset     SPACE - Sort     A - Ascending     D - Descending", 1, draw_info.MUTED)
    algorithms = draw_info.SMALL_FONT.render("I - Insertion     B - Bubble     Q - Quick     M - Merge     H - Heap     S - Selection", 1, draw_info.MUTED)

    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 10))
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 50))
    draw_info.window.blit(algorithms, (draw_info.width/2 - algorithms.get_width()/2, 70))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    list = draw_info.list

    if clear_bg:
        clear_rect = (draw_info.HOR_PADDING//2, draw_info.VER_PADDING, draw_info.width - draw_info.HOR_PADDING, 
                      draw_info.height - draw_info.VER_PADDING)
        pygame.draw.rect(draw_info.window, draw_info.BG_COLOR, clear_rect)

    for i, val in enumerate(list):
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.bar_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.bar_width - 1, draw_info.height))

    if color_positions and clear_bg:
        top_pos = next(iter(color_positions))
        play_tone(list[top_pos], draw_info.min_val, draw_info.max_val)
    
    if clear_bg:
        pygame.display.update()

def bubble_sort(draw_info, ascending=True):
    list = draw_info.list

    for i in range(len(list) - 1):
        for j in range(len(list) - 1 - i):
            num1 = list[j]
            num2 = list[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                list[j], list[j + 1] = list[j + 1], list[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return list

def selection_sort(draw_info, ascending=True):
    list = draw_info.list

    for i in range(len(list)):
        target = i
        for j in range(i + 1, len(list)):
            if (list[j] < list[target] and ascending) or (list[j] > list[target] and not ascending):
                target = j
            draw_list(draw_info, {j: draw_info.RED, target: draw_info.GREEN, i: draw_info.GRAY}, True)
            yield True

        list[i], list[target] = list[target], list[i]
        draw_list(draw_info, {i: draw_info.GREEN, target: draw_info.RED}, True)
        yield True

    return list

def insertion_sort(draw_info, ascending=True):
    list = draw_info.list

    for i in range(1, len(list)):
        current = list[i]
        j = i - 1

        while j >= 0 and ((list[j] > current and ascending) or (list[j] < current and not ascending)):
            list[j + 1] = list[j]
            j -= 1
            draw_list(draw_info, {j + 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

        list[j + 1] = current
        draw_list(draw_info, {j + 1: draw_info.GREEN, i: draw_info.RED}, True)
        yield True

    return list

def merge_sort(draw_info, ascending=True):
    list = draw_info.list
    yield from _merge_sort_helper(draw_info, list, 0, len(list) - 1, ascending)
    return list

def _merge_sort_helper(draw_info, list, left, right, ascending):
    if left < right:
        mid = (left + right) // 2
        yield from _merge_sort_helper(draw_info, list, left, mid, ascending)
        yield from _merge_sort_helper(draw_info, list, mid + 1, right, ascending)
        yield from _merge(draw_info, list, left, mid, right, ascending)

def _merge(draw_info, list, left, mid, right, ascending):
    left_part = list[left:mid + 1]
    right_part = list[mid + 1:right + 1]

    i = j = 0
    k = left

    while i < len(left_part) and j < len(right_part):
        if (left_part[i] <= right_part[j] and ascending) or (left_part[i] >= right_part[j] and not ascending):
            list[k] = left_part[i]
            i += 1
        else:
            list[k] = right_part[j]
            j += 1
        draw_list(draw_info, {k: draw_info.GREEN}, True)
        yield True
        k += 1

    while i < len(left_part):
        list[k] = left_part[i]
        draw_list(draw_info, {k: draw_info.GREEN}, True)
        yield True
        i += 1
        k += 1

    while j < len(right_part):
        list[k] = right_part[j]
        draw_list(draw_info, {k: draw_info.GREEN}, True)
        yield True
        j += 1
        k += 1

def heap_sort(draw_info, ascending=True):
    list = draw_info.list
    n = len(list)

    for i in range(n // 2 - 1, -1, -1):
        yield from _heapify(draw_info, list, n, i, ascending)

    for i in range(n - 1, 0, -1):
        list[0], list[i] = list[i], list[0]
        draw_list(draw_info, {0: draw_info.RED, i: draw_info.GREEN}, True)
        yield True
        yield from _heapify(draw_info, list, i, 0, ascending)

    return list

def _heapify(draw_info, list, n, i, ascending):
    target = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and ((list[left] > list[target] and ascending) or (list[left] < list[target] and not ascending)):
        target = left

    if right < n and ((list[right] > list[target] and ascending) or (list[right] < list[target] and not ascending)):
        target = right

    if target != i:
        list[i], list[target] = list[target], list[i]
        draw_list(draw_info, {i: draw_info.GREEN, target: draw_info.RED}, True)
        yield True
        yield from _heapify(draw_info, list, n, target, ascending)

def quick_sort(draw_info, ascending=True):
    list = draw_info.list
    yield from _quick_sort_helper(draw_info, list, 0, len(list) - 1, ascending)
    return list

def _quick_sort_helper(draw_info, list, low, high, ascending):
    if low < high:
        pivot_index = yield from _partition(draw_info, list, low, high, ascending)
        yield from _quick_sort_helper(draw_info, list, low, pivot_index - 1, ascending)
        yield from _quick_sort_helper(draw_info, list, pivot_index + 1, high, ascending)

def _partition(draw_info, list, low, high, ascending):
    pivot = list[high]
    i = low - 1

    for j in range(low, high):
        if (list[j] <= pivot and ascending) or (list[j] >= pivot and not ascending):
            i += 1
            list[i], list[j] = list[j], list[i]
            draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED, high: draw_info.GRAY}, True)
            yield True

    list[i + 1], list[high] = list[high], list[i + 1]
    draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.RED}, True)
    yield True
    return i + 1

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    list = gen_list(n, min_val, max_val)
    draw_info = DrawingInfo(1200, 800, list)

    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    while run:
        clock.tick(45)

        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
                play_complete()
        else:
            draw(draw_info, sorting_algo_name, ascending)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                list = gen_list(n, min_val, max_val)
                draw_info.set_list(list)
                sorting = False

            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"

            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"

            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"

            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algo_name = "Heap Sort"

            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"

    pygame.quit()

if __name__ == "__main__":
    main()