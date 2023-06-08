
g = {
     0: (1,),
     1: (0,2,3), 
     2: (1,3,4),
     3: (1,2),
     4: (2,6),
     5: (6,),
     6: (5,4)
    }

# A recursive function that uses visited[] and parent
# to detect cycle in subgraph reachable from vertext v
def isCyclicUtil(v, visited, parent):
    # Mark the current node as visited
    visited[v] = True

    # Recur for all the vertices adjacent to this node
    for neighbor in g[v]:
        # If the node is not visited, then recurse on it
        if visited[neighbor] == False:
            if (isCyclicUtil(neighbor, visited, v)):
                return True

        # If the node is visited and is not a parent 
        # then there is a cycle
        elif neighbor != parent:
            return True

    return False

def isCyclic():
    # Mark all nodes as not visited
    visited = {v: False for v in g}

    # Call the recursive helper on all the vertices
    # - skip if already visited.
    for v in g:
        if visited[v] == False:
            if (isCyclicUtil(v, visited, -1)) == True:
                return True

    return False

print(f'Is the graph {g} cyclic:  {isCyclic()}')
