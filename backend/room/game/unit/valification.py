@staticmethod
def dfs(node, target, graph, visited=set()):
    visited.add(node)
    if node == target:
        return True
    for child in graph[node]:
        if child not in visited:  # Check whether the node is visited or not
            result = dfs(child, target, graph, visited)  # Call the dfs recursively
            
            if result is True:
                return True

@staticmethod
def isConnect(node, target, graph):
    if dfs(node, target, graph):
        return True
    else:
        return False


if __name__ == "__main__":

    # Graph of nodes
    graph = {
    '1':['2','3','4','5'],
    '2':['1'],
    '3':['1','6','7','8'],
    '4':['1'],
    '5':['1'],
    '6':['3'],
    '7':['3'],
    '8':['9','10','11'],
    '9':['8'],
    '10':['8'],
    '11':['10']
    }

    print(isConnect('1', '11', graph))  # Traverse to each node of a graph

