import pandas as pd
import plotly.express as px
import networkx
import numpy as np
import random
import matplotlib

# Load data
data = pd.read_csv('./soc-sign-bitcoinotc.csv',
                   names=['Source', 'Destination', 'Weight', 'Time'], usecols=[0, 1, 2])
print("######### Data Loaded #########")
print("###############################")


def random_node_sampling(graph, k):
    print(graph.nodes)
    sampled_nodes = random.sample(graph.nodes, k)
    print(sampled_nodes)
    sample = graph.subgraph(sampled_nodes)
    return sample


def random_edge_sampling(graph, k):
    V = graph.nodes()
    # Calculate number of nodes in Graph graph
    Vs = []
    # Empty list Vs
    sample = networkx.DiGraph()

    while (len(Vs) <= k):
        # Loops run till sample size * length of V where V is number of nodes in graph as calculated above.
        edges_sample = random.sample(graph.edges(), 1)
        # Randomly samples one edge from a graph at a time
        for a1, a2 in edges_sample:
            # Nodes corresponding to sample edge are retrieved and added in new Graph
            sample.add_edge(a1, a2)
            if (a1 not in Vs):
                Vs.append(a1)
            if (a2 not in Vs):
                Vs.append(a2)
  
    for x in sample.nodes():
        neigh = (set(sample.nodes()) & set(list(graph.neighbors(x))))
        # Check neighbours of sample node and if the nodes are their in sampled set then edge is included between them.
        for y in neigh:
            # Check for every node's neighbour in sample set of nodes
            sample.add_edge(x, y)
            # Add edge between the sampled nodes
    return sample


def random_walk_sampling(complete_graph, nodes_to_sample, T, growth_size):
    complete_graph = networkx.convert_node_labels_to_integers(
        complete_graph, 0, 'default', True)
    # giving unique id to every node same as built-in function id
    for n, data in complete_graph.nodes(data=True):
        complete_graph.nodes[n]['id'] = n

    nr_nodes = len(complete_graph.nodes())
    upper_bound_nr_nodes_to_sample = nodes_to_sample
    index_of_first_random_node = random.randint(0, nr_nodes - 1)
    sampled_graph = networkx.Graph()

    sampled_graph.add_node(
        complete_graph.nodes[index_of_first_random_node]['id'])
    print("====================================")
    print(sampled_graph.nodes)

    iteration = 1
    edges_before_t_iter = 0
    curr_node = index_of_first_random_node

    while sampled_graph.number_of_nodes() != upper_bound_nr_nodes_to_sample:
        edges = [n for n in complete_graph.neighbors(curr_node)]

        index_of_edge = random.randint(0, len(edges) - 1)
        chosen_node = edges[index_of_edge]
        sampled_graph.add_node(chosen_node)
        sampled_graph.add_edge(curr_node, chosen_node)

        curr_node = chosen_node
        iteration = iteration + 1

        if iteration % T == 0:
            if ((sampled_graph.number_of_edges() - edges_before_t_iter) < growth_size):
                curr_node = random.randint(0, nr_nodes - 1)
            edges_before_t_iter = sampled_graph.number_of_edges()

    return sampled_graph


# Create Graph
K = 500

edgeList = data.values.tolist()
Graph = networkx.Graph()
Graph = networkx.from_pandas_edgelist(
    data, source='Source', target='Destination', edge_attr='Weight')


Graph_1 = random_node_sampling(Graph, K)

networkx.draw(Graph_1, with_labels=True)
matplotlib.pyplot.savefig("random_node_graph.png")

Graph_2 = random_edge_sampling(Graph, K)

networkx.draw(Graph_2, with_labels=True)
matplotlib.pyplot.savefig("random_edge_graph.png")

growth_size = 2
T = 100

Graph_3 = random_walk_sampling(Graph, K, T, growth_size)

networkx.draw(Graph_3, with_labels=True)
matplotlib.pyplot.savefig("random_walk_graph.png")


def important_nodes(graph):
    # Degree Centrality
    nodes_1 = networkx.degree_centrality(Graph)
    nodes_degree_centrality = sorted(
        nodes_1, key=nodes_1.get, reverse=True)[:50]
    # print(nodes_degree_centrality)

    # Eigenvector Centrality
    nodes_2 = networkx.eigenvector_centrality(Graph)
    nodes_eigenvector_centrality = sorted(
        nodes_2, key=nodes_2.get, reverse=True)[:50]
    # print(nodes_eigenvector_centrality)

    # Betweenness Centrality
    nodes_3 = networkx.betweenness_centrality(
        Graph, normalized=False, endpoints=True)
    nodes_betweenness_centrality = sorted(
        nodes_3, key=nodes_3.get, reverse=True)[:50]
    # print(nodes_betweenness_centrality)

    nodes = list(set(nodes_degree_centrality) | set(
        nodes_eigenvector_centrality) | set(nodes_betweenness_centrality))

    return nodes


print("###############################")
main_graph_nodes = important_nodes(Graph)
print(f'Main Graph Important Nodes : {main_graph_nodes}')
print("###############################")

node_sample_graph_nodes = important_nodes(Graph_1)
common_node_sample = list(set(main_graph_nodes) & set(node_sample_graph_nodes))
print(f'Node Sample Graph Important Nodes : {node_sample_graph_nodes}')
print(f'Number of Common Nodes: { len(common_node_sample) }')
print("###############################")

edge_sample_graph_nodes = important_nodes(Graph_2)
common_edge_sample = list(set(main_graph_nodes) & set(edge_sample_graph_nodes))
print(f'Edge Sample Graph Important Nodes : {edge_sample_graph_nodes}')
print(f'Number of Common Nodes: { len(common_edge_sample) }')
print("###############################")

random_walk_graph_nodes = important_nodes(Graph_3)
common_random_walk = list(set(main_graph_nodes) & set(random_walk_graph_nodes))
print(f'Random Walk Graph Important Nodes : {random_walk_graph_nodes}')
print(f'Number of Common Nodes: {len(common_random_walk)}')
print("###############################")


y = []
y.append(len(common_random_walk))
y.append(len(common_edge_sample))
y.append(len(common_node_sample))

x = []
x.append('Random Walk')
x.append('Edge Sample')
x.append('Node Sample')

figure = px.bar(x, y=y)

figure.show()
