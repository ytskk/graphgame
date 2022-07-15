import base64
import random
from itertools import combinations, groupby

import networkx as nx
from networkx.generators.random_graphs import _random_subset


def CosarajuEndOfGame(
    nodes, edges
):  # Алгоритм выявления компонент связанности Косарайю
    """
    It takes a list of nodes and edges, and returns True if there are more than one connected components
    in the graph, and False otherwise

    :param nodes: a list of nodes, each node is a dictionary with the following keys:
    :param edges: a list of edges, each edge is a dictionary with two keys: "source" and "target", each
    of which is the id of a node
    :return: True if the graph has more than one component, and False otherwise.
    """
    visited = {i["data"]["id"]: False for i in nodes}
    components = []
    for node in nodes:
        if not components:
            comp = dfs(node["data"]["id"], edges, visited, [])
            components.append(comp)
        else:
            isIn = any(node["data"]["id"] in i for i in components)
            if not isIn:
                comp = dfs(node["data"]["id"], edges, visited, [])
                components.append(comp)
    return len(components) > 1


def dfs(node, edges, visited, comp):  # Функция обхода графа в глубину
    """
    It takes a node, a list of edges, a list of visited nodes, and a list of nodes in the current
    component, and returns the list of nodes in the current component

    :param node: the node to start the search from
    :param edges: list of edges
    :param visited: a list of booleans, where visited[i] is True if node i has been visited
    :param comp: a list of nodes in the component
    :return: A list of nodes that are connected to each other.
    """
    visited[node] = True
    comp.append(node)
    adj = []
    for i in edges:
        if i["data"]["source"] == node and i["data"]["target"] != node:
            adj.append(i["data"]["target"])
        elif i["data"]["target"] == node and i["data"]["source"] != node:
            adj.append(i["data"]["source"])
    for w in adj:
        if not visited[w]:
            dfs(w, edges, visited, comp)
    return comp


def CSV_to_NX(content, node_count):  # Транслирует граф, записанный в CSV в граф NX
    """
    It takes a CSV file and converts it into a graph

    :param content: the CSV file
    :param node_count: the number of nodes in the graph
    :return: A tuple of two values.
    """

    content_type, content_string = content.split(",")
    decoded = (
        base64.b64decode(content_string).decode("utf-8").replace("\r", "").split("\n")
    )
    g = nx.Graph()
    for i in decoded:
        node_count = node_count + 1
        line = i.split(";")
        for j in line:
            if line[0] != j:
                g.add_edge(int(line[0]), int(j), attr_dict=None)
    return g, node_count


def find_sharneers(edges):  # Поиск шарниров
    """
    It takes a list of edges and returns a list of articulation points

    :param edges: a list of dictionaries, each dictionary has the following keys:
    :return: A list of lists of articulation points.
    """
    G = nx.Graph()
    for edge in edges:
        G.add_edge(edge["data"]["source"], edge["data"]["target"])
    if not nx.is_connected(G):
        return []
    print(list(nx.articulation_points(G)))
    return list(list(nx.articulation_points(G)))


def check_ways(edges):  # Функция подсчета путей в графе
    """
    It takes a list of edges and returns the number of ways to get from any node to any other node

    :param edges: a list of dictionaries, each dictionary has the following keys:
    :return: The number of paths between all pairs of nodes in the graph.
    """
    start = 0
    G = nx.Graph()
    for edge in edges:
        G.add_edge(edge["data"]["source"], edge["data"]["target"])
    temp = nx.all_pairs_node_connectivity(G)
    for i in temp.keys():
        for k in temp[i]:
            start = start + temp[i][k]
    return start


def check_winning(edges):
    """
    It takes a list of edges, and returns the percentage of nodes that are connected to each other

    :param edges: a list of dictionaries, each dictionary has the following keys:
    :return: the intactness of the graph.
    """
    graph = nx.Graph()
    for edge in edges:
        print(edge)
        graph.add_edge(edge["data"]["source"], edge["data"]["target"])
    graphConnections = list(nx.connected_components(graph))
    intactness = 0
    print(len(graph.nodes()))
    for i in range(len(graphConnections)):
        print(intactness)
        nowGraph = nx.Graph()
        nowGraph.add_edges_from(graph.edges(graphConnections[i]))
        nowGraphNodes = 1 if len(nowGraph.nodes()) == 0 else len(nowGraph.nodes())
        for j in range(i + 1, len(graphConnections)):
            currentGraph = nx.Graph()
            currentGraph.add_edges_from(graph.edges(graphConnections[j]))
            if len(currentGraph.nodes()) == 0:
                currentGraphNodes = 1
            else:
                currentGraphNodes = len(currentGraph.nodes())
            intactness += currentGraphNodes * nowGraphNodes * 2
            print(f"fsdfsdfs{currentGraphNodes}")
        print(nowGraphNodes)
    return 1 - intactness / (len(graph.nodes()) ** 2)


def find_svyazn(edges):
    """
    It takes a list of edges and returns a dictionary of nodes and their degree

    :param edges: a list of dictionaries, each dictionary has a "data" key, which is a dictionary with
    "source" and "target" keys
    :return: A dictionary with the node as the key and the number of neighbors as the value.
    """
    G = nx.Graph()
    for edge in edges:
        G.add_edge(edge["data"]["source"], edge["data"]["target"])
    return {node: len(G.neighbors(node)) for node in G.nodes()}


def find_centr(edges):
    """
    > The function takes a list of edges and returns a dictionary of betweenness centrality scores for
    each node

    :param edges: a list of dictionaries, each dictionary has a key "data" which is a dictionary with
    keys "source" and "target"
    :return: A dictionary with the nodes as keys and the centrality as values.
    """
    centr = {}
    G = nx.Graph()
    for edge in edges:
        G.add_edge(edge["data"]["source"], edge["data"]["target"])
    centr = nx.betweenness_centrality(G)
    return centr


def find_clust(edges):
    """
    It takes a list of edges and returns a dictionary of the clustering coefficient for each node

    :param edges: a list of dictionaries, each dictionary is an edge in the graph
    :return: A dictionary of the clustering coefficient for each node.
    """
    clust = {}
    G = nx.Graph()
    for edge in edges:
        G.add_edge(edge["data"]["source"], edge["data"]["target"])
    clust = nx.clustering(G)
    return clust
