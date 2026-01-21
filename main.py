import pygame
import time
import random

pygame.init()

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Screen Dimensions
GAME_WIDTH = 300
GAME_HEIGHT = 200
STATS_HEIGHT = 50
DIS_WIDTH = GAME_WIDTH
DIS_HEIGHT = GAME_HEIGHT + STATS_HEIGHT

from collections import deque

dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game by Antigravity')

clock = pygame.time.Clock()

SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# Load Assets
try:
    img = pygame.image.load('snakeantigravity/snake_head.png')
    snake_head_img = pygame.transform.scale(img, (SNAKE_BLOCK, SNAKE_BLOCK))
    
    apple = pygame.image.load('snakeantigravity/apple.png')
    apple_img = pygame.transform.scale(apple, (SNAKE_BLOCK, SNAKE_BLOCK))
except pygame.error:
    snake_head_img = None
    apple_img = None

font_style = pygame.font.SysFont("bahnschrift", 20)
score_font = pygame.font.SysFont("comicsansms", 20)

def your_score(score):
    value = score_font.render("Score: " + str(score), True, YELLOW)
    dis.blit(value, [5, GAME_HEIGHT + 10])

def our_snake(snake_block, snake_list):
    # Draw body
    for x in snake_list[:-1]:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], snake_block, snake_block])
    
    # Draw head
    head = snake_list[-1]
    if snake_head_img:
        dis.blit(snake_head_img, (head[0], head[1]))
    else:
        pygame.draw.rect(dis, GREEN, [head[0], head[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    # Center the message in the game area, not the whole screen
    text_rect = mesg.get_rect(center=(GAME_WIDTH/2, GAME_HEIGHT/2))
    dis.blit(mesg, text_rect)

def get_auto_move(snake_list, food_pos, snake_block):
    head = snake_list[-1]
    head_x, head_y = head[0], head[1]
    food_x, food_y = food_pos[0], food_pos[1]
    
    queue = deque([(head_x, head_y, [])])
    visited = set()
    visited.add((head_x, head_y))
    
    obstacles = set()
    for segment in snake_list[:-1]:
        obstacles.add((segment[0], segment[1]))
        
    while queue:
        x, y, path = queue.popleft()
        
        if x == food_x and y == food_y:
            if path:
                return path[0]
            return None
            
        directions = [
            (-snake_block, 0), # Left
            (snake_block, 0),  # Right
            (0, -snake_block), # Up
            (0, snake_block)   # Down
        ]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if nx < 0 or nx >= GAME_WIDTH or ny < 0 or ny >= GAME_HEIGHT:
                continue
                
            if (nx, ny) in obstacles:
                continue
                
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                new_path = list(path)
                new_path.append((dx, dy))
                queue.append((nx, ny, new_path))
                
    directions = [
         (-snake_block, 0), (snake_block, 0), (0, -snake_block), (0, snake_block)
    ]
    random.shuffle(directions)
    
    for dx, dy in directions:
        nx, ny = head_x + dx, head_y + dy
        if 0 <= nx < GAME_WIDTH and 0 <= ny < GAME_HEIGHT and (nx, ny) not in obstacles:
             return (dx, dy)
             
    return None

def generate_food(snake_list):
    while True:
        foodx = round(random.randrange(0, GAME_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
        foody = round(random.randrange(0, GAME_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
        
        is_on_snake = False
        for segment in snake_list:
            if segment[0] == foodx and segment[1] == foody:
                is_on_snake = True
                break
        
        if not is_on_snake:
            return foodx, foody

def gameLoop():
    game_over = False
    game_close = False

    x1 = GAME_WIDTH / 2
    y1 = GAME_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    
    # Initialize snake head just to pass to generate_food, though empty list works too as logic checks iterations
    snake_Head = [x1, y1]
    snake_List.append(snake_Head)

    foodx, foody = generate_food(snake_List)

    auto_play = False

    while not game_over:

        while game_close == True:
            dis.fill(BLACK)
            message("You Lost! Press C-Play Again or Q-Quit", RED)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    auto_play = not auto_play
                if not auto_play:
                    if event.key == pygame.K_LEFT:
                        x1_change = -SNAKE_BLOCK
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = SNAKE_BLOCK
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -SNAKE_BLOCK
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = SNAKE_BLOCK
                        x1_change = 0
        
        if auto_play:
            move = get_auto_move(snake_List, (foodx, foody), SNAKE_BLOCK)
            if move:
                x1_change, y1_change = move

        if x1 >= GAME_WIDTH or x1 < 0 or y1 >= GAME_HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)
        
        # Draw stats area background/separator
        pygame.draw.rect(dis, (50, 50, 50), [0, GAME_HEIGHT, DIS_WIDTH, STATS_HEIGHT])
        pygame.draw.line(dis, WHITE, (0, GAME_HEIGHT), (DIS_WIDTH, GAME_HEIGHT), 2)

        if apple_img:
            dis.blit(apple_img, (foodx, foody))
        else:
            pygame.draw.rect(dis, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(SNAKE_BLOCK, snake_List)
        your_score(Length_of_snake - 1)
        
        # Draw Auto-Play indicator
        if auto_play:
             auto_msg = score_font.render("Auto-Play: ON", True, GREEN)
             dis.blit(auto_msg, [DIS_WIDTH - 140, GAME_HEIGHT + 10])
        else:
             auto_msg = score_font.render("Auto-Play: OFF", True, RED)
             dis.blit(auto_msg, [DIS_WIDTH - 140, GAME_HEIGHT + 10])

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_List)
            Length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()
