import csv
from heapq import *
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar(start, end):
    # Begin your code (Part 4)
    '''
    This time, besides the graph info, we need to read the heuristicFile.
    From heuristicFile, we can get the distance from each vertex to the end vertex.
    Then we do the same thing as what we do in usc.
    However, this time we choose weight to be the distance from the current vertex
    to start vertex + heuristic function.
    heuristic function: the distance between current vertex and the end vertex.
    This weight can ensure us to go in the right direction and a low cost route at
    the same time.
    '''
    try:
        road, heur = dict(), dict()
        ind = 0
        
        with open(edgeFile) as f:
            rows = csv.reader(f)
            for row in rows:
                if row[0] == 'start':
                    continue
                road[int(row[0])] = road.get(int(row[0]), [])
                road[int(row[0])].append((int(row[1]), float(row[2]), float(row[3])))

        with open(heuristicFile) as f:
            rows = csv.reader(f)
            for row in rows:
                if row[0] == 'node':
                    for i in range(1,4):
                        if end == int(row[i]):
                            ind = i-1
                    continue
                heur[int(row[0])] = ((float(row[1]), float(row[2]), float(row[3])))

        goback = dict()
        heap = []
        heappush(heap, (heur[start][ind], start, None))
        visited, nums = set(), set()
        num, ddist = 0, 0

        while(heap):
            dist, node, baba = heappop(heap)
            dist -= heur[node][ind]
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
                    heappush(heap, (d+dist+heur[v][ind], v, node))

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
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
