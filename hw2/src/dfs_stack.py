import csv
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    '''
    At first, we store the graph info by dictionary again.
    Then we search end point by dfs.
    Whenever we find a new vertex, we push its neighbors into stack.
    Every time we pop the back of stack to get a new vertex; in other words, last in first out.
    This way turns out that we expand our route in only one route.
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
        stack = []
        stack.append((start, None, 0))
        visited = set()
        visited.add(start)
        times = 0
        
        while(stack):

            flg = False
            #cur:current, prev:previous, dist:dist
            (cur, prev, dist) = stack.pop()
            goback[cur] = (prev, dist)
            adj = road.get(cur, [])
            for n, d, _ in adj:
                if n not in visited:
                    stack.append((n, cur, d))
                    visited.add(n)
                    times += 1
                if n == end:
                    goback[n] = (cur, d)
                    flg = True
                    break
            if flg:
                break

        path = [end]
        node = end
        dist = 0

        while node != start:
            dist += goback[node][1]
            node = goback[node][0]
            path.append(node)

        path.reverse()
    
        return path, dist, times
    except:
        raise NotImplementedError("To be implemented")
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
