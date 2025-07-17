import numpy as np

def path_to_grid(path, size=128, input_width=640, input_height=480):
    grid = np.zeros((size, size), dtype=int)
    for x, y in path:
        gx = int((x / input_width) * size)
        gy = int((y / input_height) * size)
        if 0 <= gx < size and 0 <= gy < size:
            grid[gy][gx] = 1
    return grid.tolist()
