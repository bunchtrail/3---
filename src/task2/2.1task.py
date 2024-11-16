from fractions import Fraction
from tabulate import tabulate
import pickle  # Добавлено для загрузки матрицы

# Удаляем функцию read_matrix(), так как матрица будет загружаться из файла
# def read_matrix():
#     # ...existing code...

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

def main():
    # Загружаем матрицу переходов из файла
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
    P2 = multiply_matrices(P, P)

    # Проверка суммы строк P^2
    check_row_sums(P2, "P^2")

    # Вывод матрицы P^2 с использованием tabulate
    print_matrix(P2, "P^2")

    # Вычисление P^3
    print("\n" + "=" * 50)
    print("Вычисление матрицы P^3:")
    print("=" * 50)
    P3 = multiply_matrices(P2, P)

    # Проверка суммы строк P^3
    check_row_sums(P3, "P^3")

    # Вывод матрицы P^3 с использованием tabulate
    print_matrix(P3, "P^3")

if __name__ == "__main__":
    main()
