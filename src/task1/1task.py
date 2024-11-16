from utils import get_transition_matrix, validate_matrix, build_and_draw_graph, print_transition_matrix, print_dot_product


def main():
    print("Программа для анализа цепи Маркова с матрицей переходов 3x3.")

    states = ['a1', 'a2', 'a3']
    while True:
        # Шаг 1: Ввод матрицы переходов
        matrix = get_transition_matrix()

        # Шаг 2: Проверка корректности матрицы
        if validate_matrix(matrix):
            break
        else:
            print("Матрица переходов некорректна. Пожалуйста, введите матрицу снова.")

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