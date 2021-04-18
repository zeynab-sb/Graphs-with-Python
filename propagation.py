import pandas as pd
import plotly.graph_objects as go
import networkx
import numpy as np
import random


# Load data
data = pd.read_csv('./soc-sign-bitcoinotc.csv',
                   names=['Source', 'Destination', 'Weight', 'Time'], usecols=[0, 1, 2])
print("######### Loaded Data #########")
print(data)
print("###############################")

edgeList = data.values.tolist()
Graph = networkx.DiGraph()

for i in range(len(edgeList)):
    Graph.add_edge(edgeList[i][0], edgeList[i][1], weight=edgeList[i][2])


s = set()
iteration_x = []
per_y = []


def propagate(node, iteration):
    ready_to_color = set()
    ready_to_color.add(node)

    old_per = 0
    while len(s) < len(list(Graph.nodes())):
        neighbors = np.array([])
        for current_node in ready_to_color:
            s.add(current_node)
            current_neighbors = Graph.neighbors(current_node)
            neighbors = np.concatenate(
                (neighbors, list(current_neighbors)), axis=0)

        ready_to_color.clear()
        ready_to_color = set(neighbors)

        new_per = (len(s)/(Graph.number_of_nodes())) * 100
        if(old_per == new_per):
            start_node = random.sample(set(list(Graph.nodes())) - s, 1)[0]
            propagate(start_node, iteration)
        else:
            print("***************************************************************************************")
            print(f'Iteration {iteration} -- Percentage of colored nodes: {new_per}')
            iteration_x.append(iteration)
            per_y.append(new_per)
            if(new_per == 100.0):
                print(
                    f'After k = {iteration} iterations all the nodes are red.')
                break    
            iteration = iteration + 1
            old_per = new_per


start_node = random.sample(set(list(Graph.nodes())), 1)[0]
propagate(start_node, 0)
fig = go.Figure()
fig.add_trace(go.Scatter(x=iteration_x, y=per_y))

v = sorted(Graph.degree, key=lambda x: x[1], reverse=True)
print(f'The node with maximum degree is: {v[0][0]}')
s.clear()
iteration_x.clear()
per_y.clear()
propagate(v[0][0], 0)
fig.add_trace(go.Scatter(x=iteration_x, y=per_y))
fig.show()
