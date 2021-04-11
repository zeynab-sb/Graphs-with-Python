import pandas as pd
import networkx

data = pd.read_csv('./soc-sign-bitcoinotc.csv', names=['Source','Destination','Weight', 'Time'], usecols=[0,1,2])
print(data)


edgeList = data.values.tolist()
print(edgeList[0][0], edgeList[0][1], edgeList[0][2])
G = networkx.DiGraph()

for i in range(len(edgeList)):
    G.add_edge(edgeList[i][0], edgeList[i][1], weight=edgeList[i][2])

print(G)
A = networkx.adjacency_matrix(G).A

print(A)