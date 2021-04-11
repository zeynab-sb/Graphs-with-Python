import pandas as pd
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



degrees = [val for (node, val) in G.degree()]

print("######### Degrees #########")
print(A)
print("###########################")