import networkx as nx
import matplotlib.pyplot as plt
from fractions import Fraction

def get_transition_matrix():
    print("Введите матрицу переходов 3x3. Ввод осуществляется построчно, разделяя элементы пробелами.")
    matrix = []
    states = ['a1', 'a2', 'a3']
    for i in range(3):
        while True:
            try:
                row = input(f"Введите строку {i+1} (например, '0 1 0' или '1/2 1/2 0'): ").strip().split()
                if len(row) != 3:
                    raise ValueError("Необходимо ввести ровно 3 элемента.")
                row = [Fraction(x) for x in row]
                matrix.append(row)
                break
            except ValueError as ve:
                print(f"Ошибка ввода: {ve}. Попробуйте снова.")
            except ZeroDivisionError:
                print("Ошибка ввода: знаменатель не может быть нулем. Попробуйте снова.")
    return matrix

def validate_matrix(matrix):
    print("\nПроверка суммы элементов каждой строки матрицы переходов...")
    for idx, row in enumerate(matrix):
        row_sum = sum(row)
        print(f"Сумма элементов строки {idx+1}: {row_sum}")
        if row_sum != Fraction(1,1):
            print(f"Ошибка: Сумма элементов строки {idx+1} не равна 1.")
            return False
    print("Все строки корректны. Сумма элементов каждой строки равна единице.")
    return True

def print_transition_matrix(matrix, states):
    print("\nМатрица переходов:")
    header = "      " + "    ".join(states)
    print(header)
    for state, row in zip(states, matrix):
        row_str = "  ".join(f"{prob}" for prob in row)
        print(f"{state}  {row_str}")

def build_and_draw_graph(matrix, states):
    print("\nПостроение диаграммы состояний...")
    G = nx.DiGraph()

    # Добавляем узлы
    for state in states:
        G.add_node(state)

    # Добавляем ребра с весами
    for i, row in enumerate(matrix):
        for j, prob in enumerate(row):
            if prob > 0:
                G.add_edge(states[i], states[j], weight=str(prob))

    pos = nx.circular_layout(G)
    plt.figure(figsize=(8, 6))
    
    # Рисуем узлы
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='lightblue')

    # Рисуем ребра
    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray')

    # Рисуем подписи узлов
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    # Рисуем подписи ребер с вероятностями
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title("Диаграмма состояний цепи Маркова")
    plt.axis('off')
    plt.show()

def print_dot_product(state, matrix, current_state_index):
    print(f"\nИз состояния {state}:")
    for i, prob in enumerate(matrix[current_state_index]):
        print(f"  Вероятность перейти в {states[i]}: {prob}")

def main():
    print("Программа для анализа цепи Маркова с матрицей переходов 3x3.")

    # Шаг 1: Ввод матрицы переход��в
    matrix = get_transition_matrix()
    states = ['a1', 'a2', 'a3']

    # Шаг 2: Проверка корректности матрицы
    if not validate_matrix(matrix):
        return

    # Шаг 3: Построение и вывод диаграммы состояний
    build_and_draw_graph(matrix, states)

    # Шаг 4: Вывод матрицы переходов
    print_transition_matrix(matrix, states)

    # Шаг 5: Пояснение
    print("\nВ данной матрице сумма элементов каждой строки равна единице, что соответствует требованиям цепей Маркова.")

    # Дополнительно: Пример произведения матрицы на вектор состояния
    # Здесь можно добавить дополнительные вычисления, если необходимо

if __name__ == "__main__":
    main()