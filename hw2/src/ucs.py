import csv
from heapq import heappop, heappush
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
    '''
    At first, we store the graph info as usual.
    We push the start vertex into heap which can maintain the smallest distance from the start at top.
    Then, we get a new vertex from the top of heap which means the nearest vertex that doesn't be visited
    from the start vertex.
    Whenever we get a new vertex, we push its neighbors into heap with weight h+d.
    h: the distance from current to start.
    d: the distance between current and its neighbor.
    When we find the end vertex, we break the loop.
    '''
    try:
        road = dict()
        
        with open(edgeFile) as f:
            rows = csv.reader(f)

            for row in rows:
                if row[0] == 'start':
                    continue
                road[int(row[0])] = road.get(int(row[0]), [])
                road[int(row[0])].append((int(row[1]), float(row[2]), float(row[3])))
        
        goback = dict()
        heap = []
        heappush(heap, (0, start, None))
        visited, nums = set(), set()
        num, ddist = 0, 0

        while(heap):
            dist, node, baba = heappop(heap)
            if node in visited:
                continue
            visited.add(node)
            goback[node] = baba
            if node == end:
                ddist = dist
                break
            adj = road.get(node, [])
            for v, d, _ in adj:
                nums.add(v)
                if v not in visited:
                    heappush(heap, (d+dist, v, node))

        path = [end]
        node = end
        num = len(nums)

        while node != start:
            node = goback[node]
            path.append(node)

        path.reverse()

        return path, ddist, num


    except:
        raise NotImplementedError("To be implemented")
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
