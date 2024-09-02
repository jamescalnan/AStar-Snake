def main():
    from rich.console import Console
    from rich.live import Live
    from random import randint
    from collections import deque
    from heapq import heappush, heappop
    from collections import defaultdict
    import time

    console = Console()

    def make_map(width, height):
        return [[' ' for _ in range(width)] for _ in range(height)]

    def print_map(arr_map):
        border = '░░' * (len(arr_map[0]) + 2)
        lines = [border]
        for row in arr_map:
            lines.append('░░' + ''.join(str(cell) * 2 for cell in row) + '░░')
        lines.append(border)
        return '\n'.join(lines)

    def add_snake(grid):
        snake = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
        for y, x in snake:
            grid[y][x] = '█'
        return snake[::-1]

    def get_head_position(snake):
        return snake[0]

    def place_snake(grid, snake):
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == '█':
                    grid[y][x] = ' '
        for y, x in snake:
            grid[y][x] = '█'
        return grid

    def place_item(grid, snake):
        empty_cells = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == ' ']
        y, x = empty_cells[randint(0, len(empty_cells) - 1)]
        grid[y][x] = '◖'
        return grid, (y, x)

    def get_adjacent(pos, grid):
        y, x = pos
        adj = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        adj = [(y % len(grid), x % len(grid[0])) for y, x in adj]
        return [p for p in adj if grid[p[0]][p[1]] != '█']

    def backtrack_solution(came_from, start, goal):
        path = [goal]
        while path[-1] != start:
            path.append(came_from[path[-1]])
        return path[::-1]

    def astar(grid, start, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = defaultdict(lambda: float('inf'))
        g_score[start] = 0
        f_score = defaultdict(lambda: float('inf'))
        f_score[start] = heuristic(start, goal)

        while open_set:
            _, current = heappop(open_set)

            if current == goal:
                return backtrack_solution(came_from, start, goal)

            for neighbor in get_adjacent(current, grid):
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set]:
                        heappush(open_set, (f_score[neighbor], neighbor))

        return []

    width, height = 30, 30
    grid = make_map(width, height)
    snake = add_snake(grid)
    grid, item_loc = place_item(grid, snake)

    direction = (0, 1)
    score = 0

    with Live(console=console, auto_refresh=False) as live:
        while True:
            head_pos = get_head_position(snake)
            path = astar(grid, head_pos, item_loc)

            if path:
                next_pos = path[1] if len(path) > 1 else path[0]
                direction = (next_pos[0] - head_pos[0], next_pos[1] - head_pos[1])
            else:
                direction = (0, 1) if direction == (0, 1) else (-direction[0], -direction[1])

            new_head = ((head_pos[0] + direction[0]) % height, (head_pos[1] + direction[1]) % width)

            if new_head in snake:
                console.print(f'[red]Game Over! Score: {score}[/red]')
                break

            snake.insert(0, new_head)
            if new_head == item_loc:
                score += 1
                grid, item_loc = place_item(grid, snake)
            else:
                snake.pop()

            grid = place_snake(grid, snake)
            live.update(print_map(grid), refresh=True)
            # time.sleep(0.01)

if __name__ == '__main__':
    main()
