import pygame
import sys
import random
from pygame.math import Vector2

# Initialization
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Screen Creation
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
background = pygame.image.load('Images/background.png').convert_alpha()

# Framerate cap
clock = pygame.time.Clock()

# Score
font = pygame.font.Font('freesansbold.ttf', 32)


# Snake Creation
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.crunch_sound = pygame.mixer.Sound('Sounds/crunch.wav')
        self.crunch_sound.set_volume(0.1)

        self.head_down = pygame.image.load('Images/head_down.png').convert_alpha()
        self.head_up = pygame.image.load('Images/head_up.png').convert_alpha()
        self.head_right = pygame.image.load('Images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Images/head_left.png').convert_alpha()

        self.tail_down = pygame.image.load('Images/tail_down.png').convert_alpha()
        self.tail_up = pygame.image.load('Images/tail_up.png').convert_alpha()
        self.tail_right = pygame.image.load('Images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Images/tail_left.png').convert_alpha()

        self.vertical_body = pygame.image.load('Images/vertical_body.png').convert_alpha()
        self.horizontal_body = pygame.image.load('Images/horizontal_body.png').convert_alpha()

        self.top_left_body = pygame.image.load('Images/top_left_body.png').convert_alpha()
        self.top_right_body = pygame.image.load('Images/top_right_body.png').convert_alpha()
        self.down_left_body = pygame.image.load('Images/down_left_body.png').convert_alpha()
        self.down_right_body = pygame.image.load('Images/down_right_body.png').convert_alpha()

    def draw_snake(self):
        self.update_head()
        self.update_tail()

        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x and previous_block.y != next_block.y:
                    screen.blit(self.vertical_body, block_rect)
                elif previous_block.y == next_block.y and previous_block.x != next_block.x:
                    screen.blit(self.horizontal_body, block_rect)
                else:
                    if previous_block.x == next_block.y == -1 or previous_block.y == next_block.x == -1:
                        screen.blit(self.top_left_body, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.down_left_body, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.top_right_body, block_rect)
                    elif previous_block.x == next_block.y == 1 or previous_block.y == next_block.x == 1:
                        screen.blit(self.down_right_body, block_rect)

    def update_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]

        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_sound(self):
        self.crunch_sound.play()

    def snake_reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


# Fruit Creation
apple = pygame.image.load('Images/apple.png').convert_alpha()


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


# Main Game Class
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = font.render(score_text, True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(50, 20))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))

        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)

    def game_over(self):
        self.snake.snake_reset()


# Timer
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 80)

# Main Game Object
main_game = MAIN()

# Game Loop
while True:
    screen.fill((100, 100, 100))
    screen.blit(background, (0, 0))
    # Draw elements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
