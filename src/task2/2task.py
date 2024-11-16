import pickle  # Добавлено для сохранения матрицы
import subprocess  # Добавлено для запуска 2.1task.py
from utils import (
    get_transition_matrix,
    validate_matrix,
    print_matrix,
    plot_state_diagram,
    multiply_matrices,
    build_transition_tree,
    display_transition_tree,
    verify_row_sums,
    matrix_to_float
)

def main():
    print("\n=== Программа для анализа цепи Маркова с матрицей переходов 3x3 ===\n")
    states = ['a1', 'a2', 'a3']

    # Шаг 1: Ввод матрицы переходов
    matrix = get_transition_matrix()
    
    # Шаг 2: Проверка корректности матрицы
    if not validate_matrix(matrix):
        print("Программа завершена из-за некорректной матрицы переходов.\n")
        return

    # Шаг 3: Построение и вывод диаграммы состояний
    print_matrix(matrix, "Исходная матрица переходов P")
    P_float = matrix_to_float(matrix)
    plot_state_diagram(P_float, states)

    # Шаг 4: Проверка суммы элементов строк начальной матрицы
    verify_row_sums(matrix, "P")

    # Шаг 5: Пояснение
    print("В данной матрице сумма элементов каждой строки равна единице, что соответствует требованиям цепей Маркова.\n")

    # Шаг 6: Вычисление P^2 = P x P с отображением шагов
    P2 = multiply_matrices(matrix, matrix, 2)
    print_matrix(P2, "Матрица P^2")
    verify_row_sums(P2, "P^2")

    # Шаг 7: Вычисление P^3 = P^2 x P с отображением шагов
    P3 = multiply_matrices(P2, matrix, 3)
    print_matrix(P3, "Матрица P^3")
    verify_row_sums(P3, "P^3")

    # Шаг 8: Построение дерева переходов для трех шагов из каждого состояния
    steps = 3
    for start_state in states:
        paths = build_transition_tree(matrix, states, steps, start_state)
        final_probs = display_transition_tree(paths, steps, start_state, states)

    # Шаг 9: Вывод итоговых матриц и результатов
    print("\n=== Итоговые матрицы ===\n")
    print("P^2:")
    for row in P2:
        print([f"{elem}" for elem in row])
    print("\nP^3:")
    for row in P3:
        print([f"{elem}" for elem in row])

    # Вывод вероятностей через три шага для каждого начального состоя��ия
    print(f"\n=== Вероятности через {steps} шага(ов) для каждого начального состояния ===")
    for start_state in states:
        idx = states.index(start_state)
        print(f"\nДля начального состояния {start_state}:")
        for j, state in enumerate(states):
            prob = P3[idx][j]
            print(f"P_{{{start_state}}}{state}^{steps} = {prob}")

      # Сохранение матрицы переходов в файл
    with open('transition_matrix.pkl', 'wb') as f:
        pickle.dump(matrix, f)
    print("\nМатрица переходов сохранена в файл 'transition_matrix.pkl'.\n")
    
    # Предложение запустить 2.1task.py
    choice = input("Введите '+' чтобы запустить последующий анализ (2.1task.py), или любую другую клавишу для выхода: ")
    if choice.strip() == '+':
        print("\nЗапуск анализа 2.1task.py...\n")
        subprocess.run(["python", "src/task2/2.1task.py"])
    else:
        print("\nРабота программы завершена.\n")
    
if __name__ == "__main__":
    main()