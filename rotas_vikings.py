import sys
import heapq

DIRECTIONS = [
    (0, 1, 'E'),   # East
    (0, -1, 'W'),  # West
    (1, 0, 'S'),   # South
    (-1, 0, 'N'),  # North
]

def read_map():
    n, m = map(int, sys.stdin.readline().split())
    mapa = [sys.stdin.readline().strip() for _ in range(n)]
    return n, m, mapa

def find_ports(mapa):
    ports = {}
    for i, row in enumerate(mapa):
        for j, cell in enumerate(row):
            if cell in '123456789':
                ports[int(cell)] = (i, j)
    return ports

def in_bounds(x, y, n, m):
    return 0 <= x < n and 0 <= y < m

def dijkstra(mapa, start, end):
    n, m = len(mapa), len(mapa[0])
    heap = []
    visited = dict()
    # (cost, x, y, direction)
    for dx, dy, d in DIRECTIONS:
        heapq.heappush(heap, (0, start[0], start[1], d))
        visited[(start[0], start[1], d)] = 0

    while heap:
        cost, x, y, dir_prev = heapq.heappop(heap)
        if (x, y) == end:
            return cost
        for dx, dy, dir_new in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if not in_bounds(nx, ny, n, m):
                continue
            if mapa[nx][ny] == '*':
                continue
            # Calculate cost
            if dir_new == dir_prev:
                new_cost = cost + 1
            else:
                new_cost = cost + 3
            state = (nx, ny, dir_new)
            if state not in visited or new_cost < visited[state]:
                visited[state] = new_cost
                heapq.heappush(heap, (new_cost, nx, ny, dir_new))
    return None  # unreachable

def main():
    n, m, mapa = read_map()
    ports = find_ports(mapa)
    order = [i for i in range(1, 10)]
    # Remove missing ports
    order = [p for p in order if p in ports]
    if not order:
        print("0")
        return
    total_cost = 0
    for i in range(len(order)):
        src = ports[order[i]]
        dst = ports[order[(i+1)%len(order)]] if i+1 < len(order) else ports[order[0]]
        if i+1 < len(order):
            dst = ports[order[i+1]]
        else:
            dst = ports[order[0]]
        if src == dst:
            continue
        cost = dijkstra(mapa, src, dst)
        if cost is None:
            continue  # skip unreachable
        total_cost += cost
    print(total_cost)

if __name__ == "__main__":
    main()
