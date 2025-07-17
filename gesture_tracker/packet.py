def coord_to_entity(x, y, grid_size=128):
    if x % 2 == 0:
        return x * grid_size + y + 1
    else:
        return x * grid_size + (grid_size - 1 - y) + 1

def grid_to_entities(grid, r=255, g=255, b=0):
    entities = []
    size = len(grid)

    for y in range(size):
        for x in range(size):
            eid = coord_to_entity(x, y, size)
            if grid[y][x]:
                entities.append([eid, r, g, b])
            else:
                entities.append([eid, 0, 0, 0])

    return entities
