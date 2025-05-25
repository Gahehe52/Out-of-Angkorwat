import random
import pygame
from object import Object, AnimatedObject

CELL_SIZE = 64

class Maze:
    def __init__(self, cols, rows, tile_size, wall_img):
        self.cols = cols
        self.rows = rows
        self.tile_size = tile_size
        self.wall_img = wall_img

        self.spike_imgs = [
            pygame.transform.scale(pygame.image.load(f"assets/tiles/spike_{i}.png").convert_alpha(), (tile_size, tile_size))
            for i in range(1, 5)
        ]

        self.fire_imgs = [
            pygame.transform.scale(pygame.image.load(f"assets/tiles/fire_{i}.png").convert_alpha(), (tile_size, tile_size))
            for i in range(1, 13)
        ]

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

        maze[1][0] = 0  # Fixed entrance

        # Create an exit on the right wall
        right_edge_options = []
        for y in range(1, self.rows - 1):
            if maze[y][self.cols - 2] == 0 and maze[y][self.cols - 1] == 1:
                right_edge_options.append((y, self.cols - 1))

        if right_edge_options:
            ey, ex = random.choice(right_edge_options)
            maze[ey][ex] = 0  # Open the wall at the right edge
            self.exit_pos = (ex * self.tile_size, ey * self.tile_size)
        else:
            # Fallback if no exit found
            self.exit_pos = (self.tile_size, self.tile_size)

        # Obstacles
        path_cells = [(y, x) for y in range(self.rows) for x in range(self.cols) if maze[y][x] == 0]
        path_cells.remove((1, 0))
        if 'ey' in locals() and (ey, ex) in path_cells:
            path_cells.remove((ey, ex))

        num_spikes = int(len(path_cells) * 0.05)
        for _ in range(num_spikes):
            if path_cells:
                y, x = random.choice(path_cells)
                maze[y][x] = 2
                path_cells.remove((y, x))

        num_fires = int(len(path_cells) * 0.03)
        for _ in range(num_fires):
            if path_cells:
                y, x = random.choice(path_cells)
                maze[y][x] = 3
                path_cells.remove((y, x))

        return maze

    def create_walls(self):
        walls = pygame.sprite.Group()
        spikes = pygame.sprite.Group()
        fires = pygame.sprite.Group()
        maze = self.generate_maze()

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                pos = (x * self.tile_size, y * self.tile_size)
                if cell == 1:
                    wall = Object(*pos, self.wall_img)
                    walls.add(wall)
                elif cell == 2:
                    spike = AnimatedObject(*pos, self.spike_imgs)
                    spikes.add(spike)
                elif cell == 3:
                    fire = AnimatedObject(*pos, self.fire_imgs)
                    fires.add(fire)

        exit_rect = pygame.Rect(self.exit_pos[0], self.exit_pos[1], self.tile_size, self.tile_size)
        return walls, spikes, fires, exit_rect
