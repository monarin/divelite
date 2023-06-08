
g = {
     0: (1,),
     1: (0,2,3), 
     2: (1,3,4),
     3: (1,2),
     4: (2,6),
     5: (6,),
     6: (5,4)
    }

def DFSUtil(v, visited):
    # Mark the current node as visited
    visited.add(v)
    print(v, end=' ')

    # Recur for all the vertices adjacent to this vertex
    for neighbor in g[v]:
        if neighbor not in visited:
            DFSUtil(neighbor, visited)

def DFS(v):
    visited = set()
    DFSUtil(v, visited)

v = 2
print(f'Following is DFS starting from vertex {v}')
DFS(v)



