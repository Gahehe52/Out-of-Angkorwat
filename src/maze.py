import random
import pygame
from object import Object

CELL_SIZE = 64

class Maze:
    def __init__(self, cols, rows, tile_size, wall_img):
        self.cols = cols
        self.rows = rows
        self.tile_size = tile_size
        self.wall_img = wall_img

    def generate_maze(self):
        maze = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

        stack = [(1, 1)]
        visited = set(stack)

        while stack:
            x, y = stack[-1]
            maze[y][x] = 0
            neighbors = []
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.cols and 0 < ny < self.rows and (nx, ny) not in visited:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                maze[(y + ny) // 2][(x + nx) // 2] = 0
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()
        return maze

    def create_walls(self):
        walls = pygame.sprite.Group()
        maze = self.generate_maze()
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 1:
                    wall = Object(x * self.tile_size, y * self.tile_size, self.wall_img)
                    walls.add(wall)
        return walls


