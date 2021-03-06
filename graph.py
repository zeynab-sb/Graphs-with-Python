from random import sample
import sys
import pandas as pd
import plotly.graph_objects as go
import networkx
import numpy as np
inf = float("inf")


# Load data
data = pd.read_csv('./soc-sign-bitcoinotc.csv',
                   names=['Source', 'Destination', 'Weight', 'Time'], usecols=[0, 1, 2])
print("######### Loaded Data #########")
print(data)
print("###############################")

# Adjency matrix
name_to_node = {name: i for i, name in enumerate(
    np.unique(data[["Source", "Destination"]].values))}
n_nodes = len(name_to_node)
A = np.zeros((n_nodes, n_nodes))
for row in data.itertuples():
    n1 = name_to_node[row.Source]
    n2 = name_to_node[row.Destination]
    A[n1, n2] += row.Weight
    A[n2, n1] += row.Weight

print("######### Adjency Matrix #########")
print(A)
print("##################################")

# Degrees
print("######### Degrees #########")

nodes_y = []
degrees_x = []
i = 0
for node in A:
    nodes_y.append(i)
    i = i + 1
    degree = 0
    for val in node:
        if val != 0:
            degree = degree+1
    print("Node " + str(i) + " - Degree: " + str(degree))
    degrees_x.append(degree)
print("###########################")

# Degree chart
np_array_degree = np.array(degrees_x)
uniqueDegree, count = np.unique(np_array_degree, return_counts=True)
fig = go.Figure()
fig.add_trace(go.Scatter(x=uniqueDegree, y=count))

fig.show()

# Avg of neighbours degrees
avg_degree_y = []
avg_node_x = []
i = 0
print("######### Avg degrees of neighbours #########")
for node in A:
    sumOfDegree = 0
    numberOfNeighbours = 0
    avgDegreeNeighbour = 0
    avg_node_x.append(i)
    i = i + 1
    col = 0
    for y in node:
        if(y != 0):
            sumOfDegree = sumOfDegree + degrees_x[col]
            numberOfNeighbours = numberOfNeighbours + 1
        col = col + 1
    if(numberOfNeighbours != 0):
        avgDegreeNeighbour = sumOfDegree / numberOfNeighbours
        avg_degree_y.append(avgDegreeNeighbour)
    print(f'Node {i} - Avg Degrees of neighbours: {avgDegreeNeighbour}')
print("#############################################")

# Avg of neighbours degrees chart
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=avg_node_x, y=avg_degree_y))

fig2.show()

# Avg of shortest paths
print("######### Avg of shortest paths #########")


def minDistance(dist, sptSet, V):
    V = len(nodes_y)
    min = sys.maxsize
    min_index = 0
    for v in range(V):
        if dist[v] < min and sptSet[v] == False:
            min = dist[v]
            min_index = v

    return min_index


def dijkstra(src, graph, V):

    dist = [sys.maxsize] * V
    dist[src] = 0
    sptSet = [False] * V

    for cout in range(V):

        u = minDistance(dist, sptSet, V)

        sptSet[u] = True

        for v in range(V):
            if graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + graph[u][v]:
                dist[v] = dist[u] + graph[u][v]

    return dist


#####
number_of_nodes = int(len(nodes_y)*(1/1000))
random_nodes = sample((list(nodes_y)), number_of_nodes)

avgPath = 0
total_avg = []
for node in random_nodes:
    dist = dijkstra(node, A, len(nodes_y))
    for d in dist:
        avgPath = avgPath + d
    total_avg.append(avgPath/len(dist))
    print(f'Node {node} - Avg of paths: {avgPath/len(dist)}')

# Avg of shortest paths chart
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=random_nodes, y=total_avg))

fig3.show()

# Avg of common neighbours


def findNeighbour(node, A):
    i = 0
    neighbours = []
    for col in A[node]:
        if(col != 0):
            neighbours.append(i)
        i = i + 1
    return neighbours


print("######### Avg of common neighbours #########")


def findAvgOfCommonNeighbours(x, A):

    x_neighbours = findNeighbour(x, A)
    sum_common = 0
    number = 0
    avg = 0
    for neighbour in x_neighbours:
        n_neighbours = findNeighbour(neighbour, A)
        common = np.intersect1d(x_neighbours, n_neighbours)
        sum_common = sum_common + len(common)
        number = number + 1
        print(
            f'Node {x} - Common neighbours with - {neighbour}: Size: {len(common)} and {common}')

    if(number != 0):
        avg = sum_common/number
    return avg


avg_common_node_x = []
avg_common_y = []
k = 0
for node in nodes_y:
    avg_common_node_x.append(k)
    avg = findAvgOfCommonNeighbours(node, A)
    avg_common_y.append(avg)
    print(f'Node {k} - Avg common neighbours is: {avg}')
    k = k + 1
print("############################################")


# Avg of common neighbours chart
fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=avg_common_node_x, y=avg_common_y))

fig4.show()
