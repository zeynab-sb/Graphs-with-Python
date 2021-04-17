import pandas as pd
import plotly.graph_objects as go
import networkx

# Load data
data = pd.read_csv('./soc-sign-bitcoinotc.csv',
                   names=['Source', 'Destination', 'Weight', 'Time'], usecols=[0, 1, 2])
print("######### Loaded Data #########")
print(data)
print("###############################")

# Adjency matrix
edgeList = data.values.tolist()
G = networkx.DiGraph()

for i in range(len(edgeList)):
    G.add_edge(edgeList[i][0], edgeList[i][1], weight=edgeList[i][2])

A = networkx.adjacency_matrix(G).A

print("######### Adjency Matrix #########")
print(A)
print("##################################")


nodes = sorted(list(G.nodes))

# Degrees
print("######### Degrees #########")
i = 0
degree_x = []
node_y = []
for node in nodes:
    degree_x.append(G.degree[int(node)])
    node_y.append(node)
    print("Node " + str(node_y[i]) + " - Degree: " + str(degree_x[i]))
    i = i + 1
print("###########################")

# Degree chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=degree_x, y=node_y))

fig.show()

# Avg of neighbours degrees
avg_degree_x = []
avg_node_y = []
print("######### Avg degrees of neighbours #########")
for node in list(nodes):
    sumOfDegree = 0
    numberOfNeighbours = 0
    avg_node_y.append(node)

    for neighbour in list(G.neighbors(node)):
        numberOfNeighbours = numberOfNeighbours + 1
        sumOfDegree = sumOfDegree + G.degree(neighbour)
    if(numberOfNeighbours != 0):
        avgDegreeNeighbour = sumOfDegree/numberOfNeighbours
    else:
        avgDegreeNeighbour = 0

    avg_degree_x.append(avgDegreeNeighbour)
    print(f'Node {node} - Avg Degrees of neighbours: {avgDegreeNeighbour}')
print("#############################################")

# Avg of neighbours degrees chart
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=avg_degree_x, y=avg_node_y))

fig2.show()

# Common neighbours of x


def findAvgOfCommonNeighbours(x):
    numberOfCommonNeighbours = 0
    numberOfNeighbours = 0
    for neighbour in list(G.neighbors(x)):
        numberOfNeighbours = numberOfNeighbours + 1
        commonNeighbour = sorted(networkx.common_neighbors(G, x, neighbour))
        print(
            f'Node {x} has {commonNeighbour} in common with neighbour {neighbour}')
        numberOfCommonNeighbours = numberOfCommonNeighbours + \
            len(commonNeighbour)
    if(numberOfNeighbours != 0):
        print(
            f'Avg of common neighbours is {numberOfCommonNeighbours/numberOfNeighbours}')


findAvgOfCommonNeighbours(5995)
