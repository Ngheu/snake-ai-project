import heapq
from collections import deque
from game import Direction, Point, BLOCK_SIZE

class LogicAgent:
    def __init__(self, game):
        self.game = game

    def get_action(self, algo_type='bfs'):
        head = self.game.head
        food = self.game.food
        obstacles = set(self.game.snake) | set(self.game.walls)
        
        path = None
        if algo_type == 'bfs':
            path = self.bfs(head, food, obstacles)
        elif algo_type == 'greedy':
            path = self.greedy_bfs(head, food, obstacles)
        
        next_step = None
        if path and len(path) > 1:
            next_step = path[1]
        else:
            next_step = self._find_any_valid_move(head, obstacles)

        if next_step:
            return self._get_action_vector(head, next_step)
        
        return [1, 0, 0]

    def bfs(self, start, target, obstacles):
        queue = deque([[start]])
        visited = set([start])
        
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node == target: return path
            
            for neighbor in self._get_neighbors(node):
                if neighbor not in visited and neighbor not in obstacles:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        return None

    def greedy_bfs(self, start, target, obstacles):
        pq = []
        heapq.heappush(pq, (0, [start]))
        visited = set([start])
        
        while pq:
            _, path = heapq.heappop(pq)
            node = path[-1]
            if node == target: return path
            
            for neighbor in self._get_neighbors(node):
                if neighbor not in visited and neighbor not in obstacles:
                    visited.add(neighbor)
                    priority = abs(neighbor.x - target.x) + abs(neighbor.y - target.y)
                    new_path = list(path)
                    new_path.append(neighbor)
                    heapq.heappush(pq, (priority, new_path))
        return None

    def _get_neighbors(self, node):
        neighbors = []
        directions = [(BLOCK_SIZE, 0), (-BLOCK_SIZE, 0), (0, BLOCK_SIZE), (0, -BLOCK_SIZE)]
        for dx, dy in directions:
            new_pt = Point(node.x + dx, node.y + dy)
            if 0 <= new_pt.x < self.game.w and 0 <= new_pt.y < self.game.h:
                neighbors.append(new_pt)
        return neighbors

    def _find_any_valid_move(self, head, obstacles):
        for neighbor in self._get_neighbors(head):
            if neighbor not in obstacles:
                return neighbor
        return None

    def _get_action_vector(self, head, next_point):
        current_dir = self.game.direction
        dx = next_point.x - head.x
        dy = next_point.y - head.y
        
        target_dir = None
        if dx == BLOCK_SIZE: target_dir = Direction.RIGHT
        elif dx == -BLOCK_SIZE: target_dir = Direction.LEFT
        elif dy == BLOCK_SIZE: target_dir = Direction.DOWN
        elif dy == -BLOCK_SIZE: target_dir = Direction.UP

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(current_dir)
        
        if target_dir == clock_wise[idx]: return [1, 0, 0]
        elif target_dir == clock_wise[(idx + 1) % 4]: return [0, 1, 0]
        else: return [0, 0, 1]