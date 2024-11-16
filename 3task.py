import random
from tabulate import tabulate
import math

# Преобразование бинарной строки в целое число
def binary_to_int(binary_str):
    return int(binary_str, 2)

# Обновленная функция приспособленности для пользовательских функций
def fitness(individual, func):
    x = binary_to_int(individual)
    return func(x)

# Генерация начальной популяции
def generate_population(size, x_min, x_max):
    population = []
    while len(population) < size:
        individual = ''.join(random.choice(['0', '1']) for _ in range(5))
        x = binary_to_int(individual)
        if x_min <= x <= x_max:
            population.append(individual)
    return population

# Функция для ввода функции или выбора стандартной
def input_function():
    choice = input("Введите '1' для использования стандартной функции f(x)=(2*x+3)**2 или '2' для ввода собственной функции: ").strip()
    if choice == '1':
        print("Используется стандартная функция f(x) = (2*x + 3)^2")
        return lambda x: (2 * x + 3) ** 2
    elif choice == '2':
        func_str = input("Введите функцию f(x), используя 'x' для переменной (например, '(2*x + 3)**2'): ")
        def func(x):
            allowed_names = {'x': x, 'math': math}
            return eval(func_str, {"__builtins__": None}, allowed_names)
        return func
    else:
        print("Неверный выбор. Используется стандартная функция f(x) = (2*x + 3)^2")
        return lambda x: (2 * x + 3) ** 2

# Отбор с использованием элитизма
def select_elite(population, func):
    sorted_population = sorted(population, key=lambda ind: fitness(ind, func), reverse=True)
    elite = sorted_population[0]
    return elite, sorted_population[1:]

# Обновленная функция кроссовера с возможностью задания точки кроссовера
def crossover(parent1, parent2, test_point=None):
    if test_point is not None:
        point = test_point
        offspring1 = parent1[:point] + parent2[point:]
        offspring2 = parent2[:point] + parent1[point:]
    else:
        # Поиск возможных точек кроссовера, где потомки будут отличаться от родителей
        possible_points = [i for i in range(1, len(parent1)) if parent1[i:] != parent2[i:]]
        if not possible_points:
            # Нет точек кроссовера, приводящих к изменению потомков
            point = None
            offspring1 = parent1
            offspring2 = parent2
        else:
            point = random.choice(possible_points)
            offspring1 = parent1[:point] + parent2[point:]
            offspring2 = parent2[:point] + parent1[point:]
    return offspring1, offspring2, point

# Функция для отображения точки кроссовера
def display_crossover(parent, point):
    if point is None:
        return parent
    else:
        return parent[:point] + '*' + parent[point:]

# Обновленная функция мутации с возможностью задания индекса бита для мутации
def mutate(individual, test_index=None):
    if test_index is not None:
        index = test_index
    else:
        index = random.randint(0, 4)
    mutated = list(individual)
    mutated[index] = '1' if mutated[index] == '0' else '0'
    return ''.join(mutated), index

# Основная функция генетического алгоритма
def genetic_algorithm():
    func = input_function()
    print("Введите диапазон значений x:")
    x_min = int(input("Минимальное значение x (например, 1): "))
    x_max = int(input("Максимальное значение x (например, 29): "))
    
    population_size = int(input("Введите размер популяции (например, 4): "))
    generations = int(input("Введите количество поколений (например, 30): "))
    
    elitism_input = input("Использовать элитизм? (да/нет): ").strip().lower()
    use_elitism = elitism_input == 'да'
    
    population = generate_population(population_size, x_min, x_max)
    for gen in range(1, generations + 1):
        fitness_values = [fitness(ind, func) for ind in population]
        print(f"\nПоколение {gen}:")
        table = []
        for idx, ind in enumerate(population):
            x_value = binary_to_int(ind)
            table.append([idx + 1, ind, x_value, fitness_values[idx]])
        print(tabulate(table, headers=["№", "Генотип", "Фенотип (x)", "Значение функции"], tablefmt="pretty"))
        
        if use_elitism:
            elite, others = select_elite(population, func)
            parent_pool = others
        else:
            elite = None
            parent_pool = population[:]
        
        # Убедитесь, что родительская популяция достаточно велика для выборки
        if len(parent_pool) < 2:
            print("Недостаточно индивидуумов для кроссовера.")
            break
        
        parent1, parent2 = random.sample(parent_pool, 2)
        offspring1, offspring2, point = crossover(parent1, parent2)
        
        print("\nКроссовер:")
        parent1_display = display_crossover(parent1, point)
        parent2_display = display_crossover(parent2, point)
        print(f"Родитель 1: '{parent1_display}'")
        print(f"Родитель 2: '{parent2_display}'")
        if point is not None:
            print(f"Точка кроссовера: {point}")
            print(f"Потомок 1: '{offspring1}'")
            print(f"Потомок 2: '{offspring2}'")
        else:
            print("Кроссовер не изменил потомков, они идентичны родителям.")
        
        # Мутация происходит один раз для всей популяции
        mutated_offspring = []
        for offspring in [offspring1, offspring2]:
            mutated, index = mutate(offspring)
            print(f"Мутация индивида '{offspring}': '{mutated}' (бит {index})")
            mutated_offspring.append(mutated)
        
        # Фильтрация потомков по диапазону x
        valid_offspring = [ind for ind in mutated_offspring if x_min <= binary_to_int(ind) <= x_max]
        
        if use_elitism and elite:
            population = [elite] + valid_offspring
            # Заполнение оставшихся мест случайными индивидами из остальных
            while len(population) < population_size:
                new_individual = ''.join(random.choice(['0', '1']) for _ in range(5))
                x = binary_to_int(new_individual)
                if x_min <= x <= x_max:
                    population.append(new_individual)
        else:
            population = valid_offspring
            # Заполнение оставшихся мест случайными индивидуумами
            while len(population) < population_size:
                new_individual = ''.join(random.choice(['0', '1']) for _ in range(5))
                x = binary_to_int(new_individual)
                if x_min <= x <= x_max:
                    population.append(new_individual)
    
    best_individual = max(population, key=lambda ind: fitness(ind, func))
    best_fitness = fitness(best_individual, func)
    best_x = binary_to_int(best_individual)
    print("\nФинальное поколение:")
    print(f"Лучшее значение функции: f({best_x}) = {best_fitness} при генотипе '{best_individual}'")

# Обновленная функция тестирования генетического алгоритма с предопределенными данными
def test_genetic_algorithm():
    print("Запуск тестирования генетического алгоритма с предопределенными данными.\n")
    
    # Предопределенные данные, соответствующие ручному решению
    initial_population = ["00100", "01000", "01000", "00001"]
    generations = 1  # Тестируем только одно поколение
    x_min = 0
    x_max = 31  # 5-битовые числа от 0 до 31
    population_size = 4
    use_elitism = True
    
    # Функция приспособленности
    func = lambda x: (2 * x + 3) ** 2
    
    population = initial_population.copy()
    print(f"Начальная популяция: {population}")
    
    for gen in range(1, generations + 1):
        fitness_values = [fitness(ind, func) for ind in population]
        print(f"\nПоколение {gen}:")
        table = []
        for idx, ind in enumerate(population):
            x_value = binary_to_int(ind)
            table.append([idx + 1, ind, x_value, fitness_values[idx]])
        print(tabulate(table, headers=["№", "Генотип", "Фенотип (x)", "Значение функции"], tablefmt="pretty"))
        
        if use_elitism:
            elite, others = select_elite(population, func)
            parent_pool = others
        else:
            elite = None
            parent_pool = population[:]
        
        # Кроссовер между Родителем 1 и Родителем 2
        parent1 = "00100"
        parent2 = "01000"
        test_point1 = 1  # Точка кроссовера после первого бита
        
        offspring1, offspring2, point = crossover(parent1, parent2, test_point1)
        
        print("\nКроссовер между Родителем 1 и Родителем 2:")
        parent1_display = display_crossover(parent1, point)
        parent2_display = display_crossover(parent2, point)
        print(f"Родитель 1: '{parent1_display}'")
        print(f"Родитель 2: '{parent2_display}'")
        print(f"Точка кроссовера: {point}")
        print(f"Потомок 1: '{offspring1}'")
        print(f"Потомок 2: '{offspring2}'")
        
        # Кроссовер между Родителем 3 и Родителем 4
        parent3 = "01000"
        parent4 = "00001"
        test_point2 = 3  # Точка кроссовера после третьего бита
        
        offspring3, offspring4, point = crossover(parent3, parent4, test_point2)
        
        print("\nКроссовер между Родителем 3 и Родителем 4:")
        parent3_display = display_crossover(parent3, point)
        parent4_display = display_crossover(parent4, point)
        print(f"Родитель 3: '{parent3_display}'")
        print(f"Родитель 4: '{parent4_display}'")
        print(f"Точка кроссовера: {point}")
        print(f"Потомок 3: '{offspring3}'")
        print(f"Потомок 4: '{offspring4}'")
        
        # Мутация Потомка 4
        mutated_offspring4, index = mutate(offspring4, test_index=4)  # Мутация последнего бита
        print(f"\nМутация Потомка 4:")
        print(f"Индивид до мутации: '{offspring4}'")
        print(f"Индивид после мутации: '{mutated_offspring4}' (бит {index})")
        
        # Собираем всех потомков
        offspring_list = [offspring1, offspring2, offspring3, mutated_offspring4]
        
        # Вычисляем значения функции для потомков
        print("\nВычисление значений функции для потомков:")
        offspring_table = []
        for idx, ind in enumerate(offspring_list):
            x_value = binary_to_int(ind)
            fitness_value = fitness(ind, func)
            offspring_table.append([idx + 1, ind, x_value, fitness_value])
        print(tabulate(offspring_table, headers=["№", "Генотип", "Фенотип (x)", "Значение функции"], tablefmt="pretty"))
        
        # Отбор лучших особей
        combined_population = offspring_list
        sorted_population = sorted(combined_population, key=lambda ind: fitness(ind, func), reverse=True)
        best_individuals = sorted_population[:population_size]
        
        population = best_individuals  # Обновляем популяцию для следующего поколения
        
        print("\nОтобранные особи для следующего поколения:")
        selection_table = []
        for idx, ind in enumerate(population):
            x_value = binary_to_int(ind)
            fitness_value = fitness(ind, func)
            selection_table.append([idx + 1, ind, x_value, fitness_value])
        print(tabulate(selection_table, headers=["№", "Генотип", "Фенотип (x)", "Значение функции"], tablefmt="pretty"))
        
    # Итоговый результат
    best_individual = population[0]
    best_fitness = fitness(best_individual, func)
    best_x = binary_to_int(best_individual)
    print("\nФинальное поколение:")
    print(f"Лучшее значение функции: f({best_x}) = {best_fitness} при генотипе '{best_individual}'")
    
    # Ожидаемый результат
    expected_best_individual = "01001"
    expected_best_fitness = 441
    assert best_individual == expected_best_individual, f"Ожидалось: {expected_best_individual}, Получено: {best_individual}"
    assert best_fitness == expected_best_fitness, f"Ожидалось: {expected_best_fitness}, Получено: {best_fitness}"
    print("\nТестирование прошло успешно. Результаты совпадают с ожидаемыми.\n")

if __name__ == "__main__":
    choice = input("Вы хотите запустить генетический алгоритм (1) или тестирование (2)? Введите '1' или '2': ").strip()
    if choice == '2':
        test_genetic_algorithm()
    else:
        genetic_algorithm()
