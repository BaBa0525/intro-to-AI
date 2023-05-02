import csv
edgeFile = 'edges.csv'


def bfs(start, end):
    # Begin your code (Part 1)
    '''
    At first, I read the graph by using dictionary in the form of {u :[v1, d1, s1], [v2, d2, s2], ...}
    Then, we search the graph using bfs.
    When we find a new vertex u, we push its neighbors into queue.
    Every time we pop a vertex from the queue until we find the end point; in other words, first in first out.
    This way will guarantee that we can expand our route in every direction smoothly.
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
        q = []
        q.append((start, None, 0))
        visited = set()
        visited.add(start)
        times = 0
        
        while(q):

            flg = False
            #cur:current, prev:previous, dist:dist
            (cur, prev, dist) = q.pop(0)
            goback[cur] = (prev, dist)
            adj = road.get(cur, [])
            for n, d, _ in adj:
                if n not in visited:
                    q.append((n, cur, d))
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
    # End your code (Part 1)


if __name__ == '__main__':
    
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
