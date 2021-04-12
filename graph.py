import pandas as pd
import plotly.graph_objects as go
import networkx
import numpy as np

#Load data
data = pd.read_csv('./soc-sign-bitcoinotc.csv', names=['Source','Destination','Weight', 'Time'], usecols=[0,1,2])
print("######### Loaded Data #########")
print(data)
print("###############################")

#Adjency matrix
name_to_node = {name: i for i, name in enumerate(np.unique(data[["Source", "Destination"]].values))}
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

#Degrees
print("######### Degrees #########")

nodes_y = []  
degrees_x= []
i=0
for node in A:
    nodes_y.append(i)
    i= i +1 
    degree = 0
    for val in node:
        if val!=0 :
            degree = degree+1
    print("Node " + str(i) + " - Degree: " + str(degree)) 
    degrees_x.append(degree)    
print("###########################")

#Degree chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=degrees_x, y=nodes_y))

fig.show()

#Avg of neighbours degrees
avg_degree_x = []
avg_node_y = []
i = 0;
print("######### Avg degrees of neighbours #########")
for node in A:
    sumOfDegree = 0
    numberOfNeighbours = 0
    avgDegreeNeighbour = 0
    avg_node_y.append(i)
    i = i + 1
    col = 0
    for y in node:
        if(y!=0):
            sumOfDegree = sumOfDegree + degrees_x[col]
            numberOfNeighbours = numberOfNeighbours + 1
        col = col + 1    
    if(numberOfNeighbours!=0):
        avgDegreeNeighbour = sumOfDegree / numberOfNeighbours
        avg_degree_x.append(avgDegreeNeighbour)
    print(f'Node {i} - Avg Degrees of neighbours: {avgDegreeNeighbour}')         
print("#############################################")

#Avg of neighbours degrees chart
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=avg_degree_x, y=avg_node_y))

fig2.show()

