import pandas as pd
import plotly.graph_objects as go
import networkx

#Load data
data = pd.read_csv('./soc-sign-bitcoinotc.csv', names=['Source','Destination','Weight', 'Time'], usecols=[0,1,2])
print("######### Loaded Data #########")
print(data)
print("###############################")

#Adjency matrix
name_to_node = {name: i for i, name in enumerate(np.unique(data[["Source", "Destination"]].values))}
n_nodes = len(name_to_node)
A = np.zeros((n_nodes, n_nodes))
for row in df.itertuples():
    n1 = name_to_node[row.source]
    n2 = name_to_node[row.destination]
    A[n1, n2] += row.Weight
    A[n2, n1] += row.Weight

print("######### Adjency Matrix #########")
print(A)
print("##################################")