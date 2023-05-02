import csv
from heapq import *
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)
    '''
    To find the fastest route, we first change the weight to time consumption.
    This way, we can get the route with the least time.
    To reduce visited nodes, we use heuristic function that estimate the time
    it takes to get the end vertex.
    heuristic function = 
    distance from the end vertex / the average speed from the start vertex to current one.
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
        heappush(heap, (0, 0, 0, start, None))
        visited, nums = set(), set()
        num, time = 0, 0

        while(heap):
            _, sec, dist, node, baba = heappop(heap)
            if node in visited:
                continue
            visited.add(node)
            goback[node] = baba
            if node == end:
                time = sec
                break
            adj = road.get(node, [])
            for v, d, sp in adj:
                nums.add(v)
                if v not in visited:
                    t = sec + (d/sp)*3.6
                    avgs = (dist+d)/t
                    s = heur[v][ind]/avgs
                    heappush(heap, (t+s*0.8, t, dist+d, v, node))

        path = [end]
        node = end
        num = len(nums)

        while node != start:
            node = goback[node]
            path.append(node)

        path.reverse()

        return path, time, num
                
    except:
        raise NotImplementedError("To be implemented")
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
