from tabulate import tabulate
from utils import calculate_route_cost

def input_distance_matrix():
    print("Введите матрицу расстояний между городами построчно, разделяя числа пробелами (5 строк по 5 чисел):")
    cities = ['1', '2', '3', '4', '5']
    matrix = []
    for i in range(5):
        while True:
            try:
                row_input = input(f"Строка {i + 1}: ")
                row = list(map(int, row_input.strip().split()))
                if len(row) != 5:
                    print("Пожалуйста, введите ровно 5 чисел.")
                    continue
                if row[i] != 0:
                    print("Расстояние от города до самого себя должно быть 0.")
                    continue
                matrix.append(row)
                break
            except ValueError:
                print("Пожалуйста, введите целые числа.")
    print("\nМатрица расстояний:")
    headers = [''] + cities
    table = [[cities[i]] + matrix[i] for i in range(5)]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
    return matrix

def display_results(table_data, distance_matrix, offspring, city_indices):
    headers = [
        "№",
        "Родитель (генотип)",
        "Расчет родителя",
        "Значение родителя",
        "Потомок",
        "Расчет потомка",
        "Значение потомка"
    ]

    print("Полный расчет задачи коммивояжера в виде таблицы")
    print("Инициализация и расчет потомков после кроссинговера")
    print("В этой таблице отображается полный процесс — от выбора родительских маршрутов, их значений, получения потомков после кроссинговера и значений маршрутов этих потомков по матрице смежности.\n")
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", stralign='center'))

    # Вывод ответа
    best_offspring = min(offspring, key=lambda route: calculate_route_cost(route, distance_matrix, city_indices)[0])
    best_cost, _ = calculate_route_cost(best_offspring, distance_matrix, city_indices)
    print("\nЛучший найденный маршрут среди потомков:")
    print(f"Маршрут: {' -> '.join(best_offspring)} -> {best_offspring[0]}")
    print(f"Стоимость маршрута: {best_cost}")