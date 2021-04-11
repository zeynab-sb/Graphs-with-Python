import pandas as pd
import plotly.graph_objects as go
import networkx

#Load data
data = pd.read_csv('./soc-sign-bitcoinotc.csv', names=['Source','Destination','Weight', 'Time'], usecols=[0,1,2])
print("######### Loaded Data #########")
print(data)
print("###############################")

#Adjency matrix
edgeList = data.values.tolist()
G = networkx.DiGraph()

for i in range(len(edgeList)):
    G.add_edge(edgeList[i][0], edgeList[i][1], weight=edgeList[i][2])

A = networkx.adjacency_matrix(G).A

print("######### Adjency Matrix #########")
print(A)
print("##################################")



nodes = sorted(list(G.nodes))

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

fig = go.Figure()
fig.add_trace(go.Scatter(x=degree_x, y=node_y))

fig.show()