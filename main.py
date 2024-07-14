import pygame
import random
import sys
from pygame import mixer    #sound

# Initialize Pygame
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

# Set the width and height of the screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Set the title of the window
pygame.display.set_caption("Sorting Visualization")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (0, 0, 255)

#sound load
beep_fx = pygame.mixer.Sound('beep.mp3')
beep_fx.set_volume(0.3) #vol times the original

#bg load
# bg_img = pygame.image.load('bg.jpg')


# Set the number of elements
# n = 50
# array = list(range(1, n + 1))
# random.shuffle(array)


# Function to draw the menu
def draw_menu():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    options = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Quick Sort"]
    y = 150
    for i, option in enumerate(options):
        text = font.render(option, True, BLACK)
        pygame.draw.rect(screen, BLACK, [150, y, 500, 50], 2)
        screen.blit(text, (175, y + 10))
        y += 60
    pygame.display.flip()

# Function to check menu click
def check_menu_click(pos):
    x, y = pos
    if 150 <= x <= 650:
        if 150 <= y <= 200:
            return bubble_sort_visualized(array)
        elif 210 <= y <= 260:
            return selection_sort_visualized(array)
        elif 270 <= y <= 320:
            return insertion_sort_visualized(array)
        elif 330 <= y <= 380:
            return quicksort_visualized(array, 0, len(array) - 1)
    return None

def get_input_n():
    input_box = pygame.Rect(180, 200, 100, 50)
    font = pygame.font.Font(None, 36)
    input_text = ''
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        n = int(input_text)
                        if n > 0:
                            return n
                        else:
                            input_text = ''
                    except ValueError:
                        input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        screen.fill(WHITE)
        text = font.render("Enter a positive integer n: ", True, BLACK)
        screen.blit(text, (175, 160))
        pygame.draw.rect(screen, BLACK, input_box, 2)
        text_surface = font.render(input_text, True, BLACK)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()



# Get user input for n
n = get_input_n()
array = list(range(1, n + 1))
random.shuffle(array)

# Function to draw the array
def draw_array(arr, color_positions={}):
    screen.fill(BLACK)
    bar_width = width // n
    max_height = max(arr)
    for i, val in enumerate(arr):
        # color = color_positions.get(i, BLACK)
        pygame.draw.rect(screen, GREEN, [i * bar_width, height - val * (height // max_height), bar_width, val * (height // max_height)])
        #border for rect bars
        pygame.draw.rect(screen, BLACK, [i * bar_width, height - val * (height // max_height), bar_width, val * (height // max_height)], 1)
    pygame.display.flip()

# algo sort visualization
def bubble_sort_visualized(arr):
    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1 - i):
            color_positions = {j: RED, j + 1: RED}
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                beep_fx.play()
            
            draw_array(arr, color_positions)
            yield True

def selection_sort_visualized(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            color_positions = {j: RED, min_idx: RED}
            if arr[j] < arr[min_idx]:
                min_idx = j
            draw_array(arr, color_positions)
            yield True
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        beep_fx.play()
        draw_array(arr)
        yield True

def insertion_sort_visualized(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            color_positions = {j: RED, j + 1: RED}
            draw_array(arr, color_positions)
            yield True
        arr[j + 1] = key
        beep_fx.play()
        draw_array(arr)
        yield True

def quicksort_visualized(arr, low, high):
    if low < high:
        beep_fx.play()
        pi = yield from partition(arr, low, high)
        yield from quicksort_visualized(arr, low, pi - 1)
        yield from quicksort_visualized(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        color_positions = {j: RED, high: RED}
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
        draw_array(arr, color_positions)
        yield True
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    draw_array(arr)
    yield True
    return i + 1

# show the completion message
def show_completion_message():
    # screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    message_box = pygame.Rect(80, height // 2 - 2, 630, 30)
    pygame.draw.rect(screen, WHITE, message_box)
    message = font.render("Sorting complete! Press any key to return to menu. ", True, YELLOW)
    screen.blit(message, (100, height // 2))
    pygame.display.flip()

# Main loop
running = True
sorting = False
sort_generator = bubble_sort_visualized(array)
clock = pygame.time.Clock()

# Draw the menu
draw_menu()

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not sorting:
                # Generate a new random array
                array = list(range(1, n + 1))
                random.shuffle(array)
                sort_generator = check_menu_click(event.pos)
                if sort_generator:
                    sorting = True
        elif event.type == pygame.KEYDOWN:
            if not sorting:
                # If sorting is not active and a key is pressed, redraw the menu
                n = get_input_n()
                array = list(range(1, n + 1))
                random.shuffle(array)
                draw_menu()

    if sorting:
        try:
            next(sort_generator)
        except StopIteration:
            sorting = False
            show_completion_message()

    clock.tick(60)

pygame.quit()

