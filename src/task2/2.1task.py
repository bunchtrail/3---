import pickle  # Добавлено для загрузки матрицы

from utils import multiply_matrices, check_row_sums, print_matrix

def main():
    # За��ружаем матрицу переходов из файла
    with open('transition_matrix.pkl', 'rb') as f:
        P = pickle.load(f)
    print("Матрица переходов загружена из файла 'transition_matrix.pkl'.")

    # Вычисление P^1
    P1 = P
    print_matrix(P1, "P^1")

    # Вывод исходной матрицы P с использованием tabulate
    print_matrix(P, "P")

    # Вычисление P^2
    print("\n" + "=" * 50)
    print("Вычисление матрицы P^2:")
    print("=" * 50)
    P2 = multiply_matrices(P, P, 2)

    # Проверка суммы строк P^2
    check_row_sums(P2, "P^2")

    # Вывод матрицы P^2 с использованием tabulate
    print_matrix(P2, "P^2")

    # Вычисление P^3
    print("\n" + "=" * 50)
    print("Вычисление матрицы P^3:")
    print("=" * 50)
    P3 = multiply_matrices(P2, P, 3)

    # Проверка суммы строк P^3
    check_row_sums(P3, "P^3")

    # Вывод матрицы P^3 с использованием tabulate
    print_matrix(P3, "P^3")

if __name__ == "__main__":
    main()
