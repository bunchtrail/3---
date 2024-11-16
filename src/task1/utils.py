import matplotlib.pyplot as plt
import networkx as nx

def visualize_markov_chain(matrix, states, title="Цепь Маркова"):
    """
    Визуализирует цепь Маркова с использованием networkx и matplotlib.
    """
    G = nx.DiGraph()
    
    # Добавление узлов
    for state in states:
        G.add_node(state)
    
    # Добавление ребер с весами
    for i, row in enumerate(matrix):
        for j, prob in enumerate(row):
            if prob > 0:
                G.add_edge(states[i], states[j], weight=str(prob))
    
    pos = nx.circular_layout(G)
    plt.figure(figsize=(8, 6))
    
    # Рисование узлов
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='lightblue')
    
    # Рисование ребер
    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray')
    
    # Рисование подписей узлов
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Рисование подписей ребер
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    plt.title(title)
    plt.axis('off')
    plt.show()
