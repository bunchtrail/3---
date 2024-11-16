import matplotlib.pyplot as plt
import networkx as nx
from fractions import Fraction
from itertools import count

# Задание переходной матрицы P с использованием дробей
P = [
    [Fraction(0), Fraction(1), Fraction(0)],
    [Fraction(0), Fraction(1, 2), Fraction(1, 2)],
    [Fraction(1, 3), Fraction(0), Fraction(2, 3)]
]

states = ['a1', 'a2', 'a3']

def plot_state_diagram(P_float, states):
    """
    Построение диаграммы состояний Марковской цепи.
    """
    G = nx.DiGraph()
    for i, state_from in enumerate(states):
        for j, state_to in enumerate(states):
            prob = P_float[i][j]
            if prob > 0:
                G.add_edge(state_from, state_to, weight=f"{prob:.2f}")

    pos = nx.circular_layout(G)
    plt.figure(figsize=(8,6))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', arrowsize=20)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

    plt.title("Диаграмма состояний Марковской цепи")
    plt.show()

def multiply_matrices(A, B):
    """
    Умножение двух матриц A и B, содержащих объекты Fraction.
    """
    result = [[Fraction(0) for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def display_matrix_calculation(P_current, P, power):
    """
    Отображение пошаговых вычислений для матрицы P^power.
    """
    print(f"\nВычисление P^{power}:")
    P_next = [[Fraction(0) for _ in range(len(P[0]))] for _ in range(len(P))]
    for i in range(len(P_current)):
        for j in range(len(P_current[0])):
            terms = []
            for k in range(len(P)):
                term = f"{P_current[i][k]} * {P[k][j]}"
                terms.append(term)
                P_next[i][j] += P_current[i][k] * P[k][j]
            expression = " + ".join(terms)
            print(f"P^{power}[{i+1}][{j+1}] = {expression} = {P_next[i][j]}")
    return P_next

def build_transition_tree(P, states, steps, start_state):
    """
    Построение всех возможных путей переходов за заданное количество шагов.
    """
    paths = [ ([start_state], Fraction(1,1)) ]
    for step in range(steps):
        new_paths = []
        for path, prob in paths:
            current_state = path[-1]
            current_index = states.index(current_state)
            for next_state in states:
                transition_prob = P[current_index][states.index(next_state)]
                if transition_prob > 0:
                    new_paths.append( (path + [next_state], prob * transition_prob) )
        paths = new_paths
    return paths

def display_transition_tree(paths, steps, start_state):
    """
    Отображение дерева переходов и построение графа для визуализации.
    """
    print(f"\nДерево переходов за {steps} шага(ов), начиная из состояния {start_state}:")
    final_probs = {state:Fraction(0,1) for state in states}
    for path, prob in paths:
        path_str = " -> ".join(path)
        print(f"{path_str} : {prob}")
        final_state = path[-1]
        final_probs[final_state] += prob

    print(f"\nВероятности нахождения в состояниях через {steps} шага(ов) из состояния {start_state}:")
    for state in states:
        print(f"P_{{{start_state}}}{state}^{steps} = {final_probs[state]}")

    # Построение графа дерева переходов
    G = nx.DiGraph()
    label_pos = {}
    node_labels = {}
    pos = {}
    layer_nodes = {}
    node_counter = count()

    for path, prob in paths:
        for step in range(len(path)):
            state = path[step]
            node_id = f"{state}_{step}"
            if node_id not in G:
                G.add_node(node_id)
                node_labels[node_id] = f"{state}\n(step {step})"
                layer_nodes.setdefault(step, []).append(node_id)
        # Добавление рёбер с вероятностями
        for step in range(len(path)-1):
            from_node = f"{path[step]}_{step}"
            to_node = f"{path[step+1]}_{step+1}"
            G.add_edge(from_node, to_node, label=str(prob))

    # Определение позиций узлов
    pos = {}
    for step in range(steps+1):
        nodes = layer_nodes.get(step, [])
        y = steps - step
        if nodes:
            x_gap = 1 / (len(nodes)+1)
            for idx, node in enumerate(nodes, 1):
                pos[node] = (idx * x_gap, y)

    # Определение меток для рёбер
    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=False, node_size=2000, node_color='lightgreen', arrows=True, arrowstyle='-|>', arrowsize=20)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=9)
    plt.title(f"Дерево переходов за {steps} шага(ов) из состояния {start_state}")
    plt.axis('off')
    plt.show()

    return final_probs

def verify_row_sums(matrix, name):
    """
    Проверка, что сумма вероятностей в каждой строке матрицы равна единице.
    """
    print(f"\nПроверка суммы вероятностей для {name}:")
    for i, row in enumerate(matrix):
        row_sum = sum(row)
        print(f"Сумма строки {i+1}: {row_sum} {'(Верно)' if row_sum == Fraction(1,1) else '(Ошибка)'}")

def matrix_to_float(matrix):
    """
    Преобразование матрицы из объектов Fraction в числа с плавающей точкой.
    """
    return [[float(entry) for entry in row] for row in matrix]

def main():
    # 1. Построение диаграммы состояний
    P_float = matrix_to_float(P)
    plot_state_diagram(P_float, states)

    # 2. Вывод исходной матрицы P и проверка суммы строк
    print("Исходная матрица переходов P:")
    for row in P:
        print([f"{elem}" for elem in row])

    verify_row_sums(P, "P")

    # 3. Вычисление P^2 с отображением шагов
    P2 = display_matrix_calculation(P, P, 2)
    print("\nМатрица P^2:")
    for row in P2:
        print([f"{elem}" for elem in row])

    verify_row_sums(P2, "P^2")

    # 4. Вычисление P^3 с отображением шагов
    P3 = display_matrix_calculation(P2, P, 3)
    print("\nМатрица P^3:")
    for row in P3:
        print([f"{elem}" for elem in row])

    verify_row_sums(P3, "P^3")

    # 5. Построение дерева переходов для трех шагов из каждого состояния
    steps = 3
    for start_state in states:
        paths = build_transition_tree(P, states, steps, start_state)
        final_probs = display_transition_tree(paths, steps, start_state)

    # 6. Вывод итоговых матриц и результатов
    print("\nИтоговые матрицы:")
    print("P^2:")
    for row in P2:
        print([f"{elem}" for elem in row])

    print("\nP^3:")
    for row in P3:
        print([f"{elem}" for elem in row])

    # Вывод вероятностей через три шага для каждого начального состояния
    print(f"\nВероятности через {steps} шага(ов) для каждого начального состояния:")
    for start_state in states:
        print(f"\nДля начального состояния {start_state}:")
        print(f"P_{{{start_state}}}{states[0]}^{steps} = {P3[states.index(start_state)][0]}")
        print(f"P_{{{start_state}}}{states[1]}^{steps} = {P3[states.index(start_state)][1]}")
        print(f"P_{{{start_state}}}{states[2]}^{steps} = {P3[states.index(start_state)][2]}")

if __name__ == "__main__":
    main()
