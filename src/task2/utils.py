import matplotlib.pyplot as plt
import networkx as nx
from fractions import Fraction
from itertools import count
from tabulate import tabulate  # Добавлено для красивого вывода таблиц

def multiply_matrices(A, B):
    # Умножение матриц A и B
    result = []
    for i in range(3):
        result_row = []
        for j in range(3):
            sum_elements = Fraction(0)
            explanation = []
            for m in range(3):
                product = A[i][m] * B[m][j]
                sum_elements += product
                explanation.append(f"{A[i][m]}×{B[m][j]}")
            calculation_str = " + ".join(explanation)
            print(f"\nЭлемент P^{i+2}_{{a{i+1},a{j+1}}} = {calculation_str} = {sum_elements}")
            result_row.append(sum_elements)
        result.append(result_row)
    return result

def check_row_sums(matrix, name):
    # Проверка, что сумма элементов в строках равна 1
    print(f"\nПроверка суммы строк матрицы {name}:")
    for idx, row in enumerate(matrix):
        row_sum = sum(row)
        if row_sum != Fraction(1):
            print(f"  Строка {idx+1}: сумма = {row_sum} (не равна 1)")
        else:
            print(f"  Строка {idx+1}: сумма равна 1")

def print_matrix(matrix, name):
    # Вывод матрицы в табличном формате с помощью библиотеки tabulate
    print(f"\nМатрица {name}:")
    headers = [""] + [f"a{i+1}" for i in range(len(matrix))]
    table = [[f"a{idx+1}"] + [str(elem) for elem in row] for idx, row in enumerate(matrix)]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

def get_transition_matrix():
    """
    Запрашивает у пользователя ввод матрицы переходов 3x3 с элементами в виде дробей или целых чисел.
    После ввода каждой строки сразу проверяет, что сумма элементов равна 1.
    Если проверка не пройдена, предлагает пользователю исправить ввод.
    Возвращает матрицу в виде списка списков объектов Fraction.
    """
    print("\n=== Ввод матрицы переходов 3x3 ===\n")  # Заголовок и отступы
    print("Введите каждую строку матрицы по 3 элемента, разделенных пробелом (например, '1/3 0 2/3').\n")
    matrix = []
    states = ['a1', 'a2', 'a3']
    for i in range(3):
        while True:
            try:
                row_input = input(f"Введите строку {i+1}: ").strip().split()
                if len(row_input) != 3:
                    raise ValueError("Необходимо ввести ровно 3 элемента.")
                row = [Fraction(elem) for elem in row_input]
                row_sum = sum(row)
                if row_sum != Fraction(1):
                    print(f"Сумма элементов строки {i+1} равна {row_sum}, должна быть 1. Пожалуйста, введите строку заново.\n")
                    continue
                matrix.append(row)
                break
            except ValueError as ve:
                print(f"Ошибка ввода: {ve}. Попробуйте снова.\n")
            except ZeroDivisionError:
                print("Ошибка ввода: знаменатель не может быть нулем. Попробуйте снова.\n")
    return matrix

def validate_matrix(matrix):
    """
    Проверяет, что сумма элементов каждой строки матрицы равна 1.
    Возвращает True, если матрица корректна, иначе False.
    """
    print("\n=== Проверка суммы элементов каждой строки матрицы переходов ===\n")
    valid = True
    for idx, row in enumerate(matrix):
        row_sum = sum(row)
        print(f"Сумма элементов строки {idx+1}: {row_sum}")
        if row_sum != Fraction(1,1):
            print(f"Ошибка: Сумма элементов строки {idx+1} не равна 1.\n")
            valid = False
    if valid:
        print("Все строки корректны. Сумма элементов каждой строки равна единице.\n")
    return valid

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

def multiply_matrices(A, B, power):
    """
    Умножение двух матриц A и B, содержащих объекты Fraction, с пояснениями.
    """
    print(f"\n{'='*50}\nВычисление P^{power} = P^{power-1} x P\n{'='*50}\n")  # Добавлены разделители и пояснения
    size = len(A)
    result = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    print(f"\nВычисление P^{power}:")
    for i in range(size):
        for j in range(size):
            terms = []
            for k in range(size):
                term = A[i][k] * B[k][j]
                terms.append(f"{A[i][k]}*{B[k][j]}")
                result[i][j] += term
            expression = " + ".join(terms)
            print(f"P^{power}[{i+1}][{j+1}] = {expression} = {result[i][j]}")
    return result

def build_transition_tree(P, states, steps, start_state):
    """
    Построение всех возможных путей переходов за заданное количество шагов.
    Возвращает список путей и их вероятностей.
    """
    print(f"\n{'-'*50}\nПостроение дерева переходов для состояния {start_state} на {steps} шаг(ов)\n{'-'*50}\n")  # Добавлены разделители
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

def display_transition_tree(paths, steps, start_state, states):
    """
    Отображение дерева переходов и построение графа для визуализации.
    Возвращает вероятности нахождения в каждом состоянии после заданных шагов.
    """
    print(f"\nДерево переходов за {steps} шага(ов), начиная из состояния {start_state}:\n")
    final_probs = {state:Fraction(0,1) for state in states}
    for path, prob in paths:
        path_str = " -> ".join(path)
        print(f"{path_str} : {prob}")
        final_state = path[-1]
        final_probs[final_state] += prob

    print(f"\nВероятности нахождения в состояниях через {steps} шага(ов) из состояния {start_state}:")
    for state in states:
        print(f"P_{{{start_state}}}{state}^{steps} = {final_probs[state]}")
    print()  # Добавлен перенос строки

    # Построение графа дерева переходов
    G = nx.DiGraph()
    label_pos = {}
    node_labels = {}
    pos_nodes = {}
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
    pos_nodes = {}
    for step in range(steps+1):
        nodes = layer_nodes.get(step, [])
        y = steps - step
        if nodes:
            x_gap = 1 / (len(nodes)+1)
            for idx, node in enumerate(nodes, 1):
                pos_nodes[node] = (idx * x_gap, y)

    # Определение меток для рёбер
    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos_nodes, with_labels=False, node_size=2000, node_color='lightgreen', arrows=True, arrowstyle='-|>', arrowsize=20)
    nx.draw_networkx_labels(G, pos_nodes, labels=node_labels, font_size=10)
    nx.draw_networkx_edge_labels(G, pos_nodes, edge_labels=edge_labels, font_color='red', font_size=9)
    plt.title(f"Дерево переходов за {steps} шага(ов) из состояния {start_state}")
    plt.axis('off')
    plt.show()

    return final_probs

def verify_row_sums(matrix, name):
    """
    Проверка, что сумма элементов каждой строки матрицы равна единице.
    """
    print(f"\n=== Проверка суммы элементов строк для {name} ===\n")
    valid = True
    for idx, row in enumerate(matrix):
        row_sum = sum(row)
        status = "(Верно)" if row_sum == Fraction(1,1) else "(Ошибка)"
        print(f"Сумма строки {idx+1}: {row_sum} {status}")
        if row_sum != Fraction(1,1):
            valid = False
    if valid:
        print(f"\nВсе строки матрицы {name} корректны. Сумма элементов каждой строки равна единице.\n")
    else:
        print(f"\nНекоторые строки матрицы {name} имеют суммы, отличные от единицы.\n")

def matrix_to_float(matrix):
    """
    Преобразование матрицы из объектов Fraction в числа с плавающей точкой.
    """
    return [[float(entry) for entry in row] for row in matrix]

# Пример использования функции
if __name__ == "__main__":
    P = get_transition_matrix()
    print_matrix(P, "Переходная матрица")
    # Дополнительные действия, например, проверка или построение диаграмм
