import pygame
import random
import numpy as np
from collections import namedtuple
from enum import Enum

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# --- CẤU HÌNH ---
BLOCK_SIZE = 20
SPEED = 60 # Tốc độ game
# Màu sắc
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

WINDOW_W = 640
WINDOW_H = 480

# --- HÀM TẠO TƯỜNG RANDOM ---
def get_random_walls(w, h, num_blocks=40):
    walls = []
    # Loop để tạo đủ số lượng tường mong muốn
    for _ in range(num_blocks):
        while True:
            # Random tọa độ x, y
            x = random.randint(0, (w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            pt = Point(x, y)
            
            # ĐIỀU KIỆN AN TOÀN:
            # 1. Không trùng với các tường đã tạo
            # 2. Không nằm ở giữa màn hình (nơi Rắn xuất hiện) để tránh rắn chết ngay khi start
            # Khu vực an toàn là khoảng cách 4 block tính từ tâm
            center_x, center_y = w // 2, h // 2
            safe_distance = 4 * BLOCK_SIZE
            
            if pt not in walls and (abs(x - center_x) > safe_distance or abs(y - center_y) > safe_distance):
                walls.append(pt)
                break
    return walls

# Danh sách Map
MAPS = {
    "classic": [],
    "maze": get_random_walls(WINDOW_W, WINDOW_H, num_blocks=50) # Tạo 50 cục tường random
}

class SnakeGame:
    def __init__(self, map_name="classic", w=WINDOW_W, h=WINDOW_H):
        self.w = w
        self.h = h
        self.map_name = map_name
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption(f'Snake AI - Map: {map_name.upper()}')
        self.clock = pygame.time.Clock()
        
        # Load tường từ danh sách
        self.walls = MAPS.get(map_name, [])
        # Nếu muốn mỗi lần chơi Random lại vị trí tường mới thì bỏ comment dòng dưới:
        if map_name == "maze": self.walls = get_random_walls(self.w, self.h, 50)
            
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        
        # Đảm bảo đầu rắn không spawn trúng tường
        while self.head in self.walls:
             self.head = Point(random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE,
                               random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE)

        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        while True:
            x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
            y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
            self.food = Point(x, y)
            if self.food not in self.snake and self.food not in self.walls:
                break

    def play_step(self, action):
        self.frame_iteration += 1
        
        # --- SỬA LỖI NOT RESPONDING TẠI ĐÂY ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # --------------------------------------

        self._move(action) 
        
        game_over = False
        reward = 0
        
        # Check va chạm hoặc hết thời gian (để tránh rắn đi lòng vòng)
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        self._update_ui()
        self.clock.tick(SPEED)
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # Va chạm biên
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # Va chạm thân
        if pt in self.snake[1:]:
            return True
        # Va chạm tường
        if pt in self.walls:
            return True
        return False

    def get_grid_state(self):
        grid_h = int(self.h / BLOCK_SIZE)
        grid_w = int(self.w / BLOCK_SIZE)
        grid = np.zeros((grid_h, grid_w), dtype=np.float32)

        for wall in self.walls:
            wx = int(wall.x / BLOCK_SIZE)
            wy = int(wall.y / BLOCK_SIZE)
            if 0 <= wy < grid_h and 0 <= wx < grid_w:
                grid[wy][wx] = 3.0

        for pt in self.snake:
            px = int(pt.x / BLOCK_SIZE)
            py = int(pt.y / BLOCK_SIZE)
            if 0 <= py < grid_h and 0 <= px < grid_w:
                grid[py][px] = 1.0

        hx = int(self.head.x / BLOCK_SIZE)
        hy = int(self.head.y / BLOCK_SIZE)
        if 0 <= hy < grid_h and 0 <= hx < grid_w:
            grid[hy][hx] = 4.0

        fx = int(self.food.x / BLOCK_SIZE)
        fy = int(self.food.y / BLOCK_SIZE)
        if 0 <= fy < grid_h and 0 <= fx < grid_w:
            grid[fy][fx] = 2.0
            
        return grid

    def _update_ui(self):
        self.display.fill(BLACK)
        # Vẽ tường màu Xám
        for pt in self.walls:
            pygame.draw.rect(self.display, GREY, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            
        # Vẽ rắn
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        # Vẽ thức ăn
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = pygame.font.Font(None, 25).render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        
        if np_array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np_array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir
        
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT: x += BLOCK_SIZE
        elif self.direction == Direction.LEFT: x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN: y += BLOCK_SIZE
        elif self.direction == Direction.UP: y -= BLOCK_SIZE
        
        self.head = Point(x, y)
        self.snake.insert(0, self.head)

def np_array_equal(a, b):
    return a == b