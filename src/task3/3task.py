import random
from tabulate import tabulate

def get_function_choice():
    while True:
        choice = input("Введите '1' для использования стандартной функции f(x)=(2*x+3)**2 или '2' для ввода собственной функции: ")
        if choice == '1':
            return lambda x: (2 * x + 3) ** 2
        elif choice == '2':
            func_input = input("Введите функцию от x (например, 'x**2 + 2*x + 1'): ")
            try:
                return lambda x: eval(func_input)
            except Exception as e:
                print(f"Ошибка в функции: {e}. Попробуйте снова.")
        else:
            print("Некорректный ввод. Пожалуйста, введите '1' или '2'.")

def get_range():
    while True:
        try:
            x_min = int(input("Минимальное значение x (например, 1): "))
            x_max = int(input("Максимальное значение x (например, 29): "))
            if x_min >= x_max:
                print("Минимальное значение должно быть меньше максимального. Попробуйте снова.")
                continue
            return x_min, x_max
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите целые числа.")

def get_population_size():
    while True:
        try:
            size = int(input("Введите размер популяции (например, 4): "))
            if size <= 0:
                print("Размер популяции должен быть положительным числом.")
                continue
            return size
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите целое число.")

def get_generation_count():
    while True:
        try:
            count = int(input("Введите количество поколений (например, 30): "))
            if count <= 0:
                print("Количество поколений должно быть положительным числом.")
                continue
            return count
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите целое число.")

def get_elitism_choice():
    while True:
        choice = input("Использовать элитизм? (+/-): ").lower()
        if choice in ['+', '-']:
            return choice == '+'
        else:
            print("Некорректный ввод. Пожалуйста, введите '+' или '-'.")

def initialize_population(size, bit_length):
    population = [''.join(random.choice('01') for _ in range(bit_length)) for _ in range(size)]
    print(f"Начальная популяция: {population}")
    return population

def genotype_to_phenotype(genotype, x_min, x_max, bit_length):
    max_int = 2 ** bit_length - 1
    int_value = int(genotype, 2)
    x = x_min + (x_max - x_min) * int_value / max_int
    return round(x)

def evaluate_population(population, fitness_func, x_min, x_max, bit_length):
    table = []
    for idx, genotype in enumerate(population):
        x = genotype_to_phenotype(genotype, x_min, x_max, bit_length)
        fitness = fitness_func(x)
        table.append([idx + 1, genotype, x, fitness])
    headers = ["№", "Генотип", "Фенотип (x)", "Значение функции"]
    print(f"\nПоколение:")
    print(tabulate(table, headers=headers, tablefmt="fancy_grid", numalign="center", stralign="center"))
    return table

def select_parents(population, fitness_values):
    total_fitness = sum(fitness_values)
    selection_probs = [f / total_fitness for f in fitness_values]
    parents = random.choices(population, weights=selection_probs, k=len(population))
    return parents

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    offspring1 = parent1[:point] + parent2[point:]
    offspring2 = parent2[:point] + parent1[point:]
    return offspring1, offspring2, point

def mutate(genotype):
    index = random.randint(0, len(genotype) - 1)
    mutated = list(genotype)
    mutated[index] = '1' if genotype[index] == '0' else '0'
    return ''.join(mutated)

def apply_elitism(population, fitness_values, elite_size):
    elite_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i], reverse=True)[:elite_size]
    elite = [population[i] for i in elite_indices]
    return elite

def display_crossover(parent, point):
    return parent[:point] + '*' + parent[point:]

def genetic_algorithm():
    # Этап 1: Ввод параметров пользователем
    fitness_func = get_function_choice()
    x_min, x_max = get_range()
    population_size = get_population_size()
    generation_count = get_generation_count()
    use_elitism = get_elitism_choice()
    bit_length = 5  # Длина генотипа в битах

    # Этап 2: Инициализация и первое поколение
    population = initialize_population(population_size, bit_length)
    for generation in range(generation_count):
        # Вычисление значений функции для текущей популяции
        evaluation = evaluate_population(population, fitness_func, x_min, x_max, bit_length)
        fitness_values = [row[3] for row in evaluation]

        # Этап 3: Кроссовер и мутация
        parents = select_parents(population, fitness_values)
        offspring = []
        print("\nКроссовер и мутация:")
        crossover_table = []
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[(i + 1) % len(parents)]
            child1, child2, point = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            x1 = genotype_to_phenotype(child1, x_min, x_max, bit_length)
            x2 = genotype_to_phenotype(child2, x_min, x_max, bit_length)
            f1 = fitness_func(x1)
            f2 = fitness_func(x2)
            offspring.extend([child1, child2])

            # Добавление звездочки в родительские генотипы
            marked_parent1 = display_crossover(parent1, point)
            marked_parent2 = display_crossover(parent2, point)

            crossover_table.append([marked_parent1, child1, f1])
            crossover_table.append([marked_parent2, child2, f2])

        headers = ["Родитель", "Потомок", "Значение функции"]
        print(tabulate(crossover_table, headers=headers, tablefmt="fancy_grid", numalign="center", stralign="center"))

        # Этап 4: Элитизм и отбор особей
        combined_population = population + offspring
        combined_fitness = fitness_values + [row[2] for row in crossover_table]
        if use_elitism:
            elite_size = population_size // 2
            population = apply_elitism(combined_population, combined_fitness, elite_size)
            while len(population) < population_size:
                population.append(random.choice(combined_population))
        else:
            population = random.sample(combined_population, population_size)

        # Итоговая таблица
        final_table = []
        for idx, indiv in enumerate(combined_population):
            x = genotype_to_phenotype(indiv, x_min, x_max, bit_length)
            fitness = fitness_func(x)
            status = "" if indiv in population else "Зачеркнут"
            final_table.append([indiv, fitness, status])

        headers = ["Индивид", "Значение функции", "Статус"]
        print("\nИтоговая таблица родителей и значений:")
        print(tabulate(final_table, headers=headers, tablefmt="fancy_grid", numalign="center", stralign="center"))

    # Этап 5: Финальное поколение и результат
    best_individual = max(population, key=lambda indiv: fitness_func(genotype_to_phenotype(indiv, x_min, x_max, bit_length)))
    best_x = genotype_to_phenotype(best_individual, x_min, x_max, bit_length)
    best_fitness = fitness_func(best_x)
    print("\nФинальное поколение:")
    print(f"Лучшее значение функции: f({best_x}) = {best_fitness} при генотипе '{best_individual}'")

if __name__ == "__main__":
    genetic_algorithm()
