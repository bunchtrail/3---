import random

# Функция для перевода 5-битной строки в целое число x (1 <= x < 30)
def binary_to_x(binary_str):
    x = int(binary_str, 2)
    if x == 0:
        x = 1  # Минимальное значение x
    elif x >= 30:
        x = 29  # Максимальное значение x
    return x

# Функция для перевода x обратно в 5-битную строку
def x_to_binary(x):
    return format(x, '05b')

# Целевая функция
def f(x):
    return (2 * x + 3) ** 2

# Инициализация начальной популяции
def initialize_population(initial_genotypes):
    population = []
    for genotype in initial_genotypes:
        x = binary_to_x(genotype)
        fitness = f(x)
        population.append({
            'genotype': genotype,
            'x': x,
            'fitness': fitness
        })
    return population

# Вычисление вероятностей участия
def calculate_probabilities(population):
    total_fitness = sum(individual['fitness'] for individual in population)
    probabilities = []
    for individual in population:
        prob = individual['fitness'] / total_fitness
        probabilities.append(prob)
    return probabilities

# Отбор родителей на основе рулеточного отбора
def select_parents(population, probabilities):
    parents = []
    for _ in range(len(population)):
        r = random.random()
        cumulative = 0
        for individual, prob in zip(population, probabilities):
            cumulative += prob
            if r <= cumulative:
                parents.append(individual)
                break
    return parents

# Одноточечный кроссовер
def crossover(parent1, parent2):
    point = random.randint(1, 4)  # Точка разрыва
    offspring1_genotype = parent1['genotype'][:point] + parent2['genotype'][point:]
    offspring2_genotype = parent2['genotype'][:point] + parent1['genotype'][point:]
    return offspring1_genotype, offspring2_genotype

# Мутация: инверсия одного случайного бита с вероятностью 0.1
def mutate(genotype, mutation_rate=0.1):
    if random.random() < mutation_rate:
        pos = random.randint(0, 4)
        genotype = list(genotype)
        genotype[pos] = '1' if genotype[pos] == '0' else '0'
        genotype = ''.join(genotype)
    return genotype

# Найти лучшую особь в популяции
def get_best_individual(population):
    return max(population, key=lambda ind: ind['fitness'])

# Основной генетический алгоритм
def genetic_algorithm(initial_genotypes, generations=10):
    # Инициализация популяции
    population = initialize_population(initial_genotypes)
    print("Инициализация популяции:")
    for individual in population:
        print(f"Генотип: {individual['genotype']}, x: {individual['x']}, f(x): {individual['fitness']}")
    print("\n")

    best_overall = get_best_individual(population)

    for generation in range(1, generations + 1):
        print(f"Поколение {generation}:")
        # Вычисление вероятностей
        probabilities = calculate_probabilities(population)
        print("Вероятности участия в размножении:")
        for individual, prob in zip(population, probabilities):
            print(f"Генотип: {individual['genotype']}, вероятность: {prob:.4f}")
        
        # Отбор родителей
        parents = select_parents(population, probabilities)
        print("\nОтобранные родители:")
        for parent in parents:
            print(f"Генотип: {parent['genotype']}, x: {parent['x']}, f(x): {parent['fitness']}")
        
        # Скрещивание
        offspring = []
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[i+1] if i+1 < len(parents) else parents[0]
            child1_genotype, child2_genotype = crossover(parent1, parent2)
            offspring.append(child1_genotype)
            offspring.append(child2_genotype)
        print("\nПотомки после скрещивания:")
        for child in offspring:
            print(f"Генотип: {child}")
        
        # Мутация
        mutated_offspring = []
        print("\nПотомки после мутации:")
        for child in offspring:
            mutated_child = mutate(child)
            mutated_offspring.append(mutated_child)
            if mutated_child != child:
                print(f"Генотип изменился: {child} -> {mutated_child}")
            else:
                print(f"Генотип остался без изменений: {child}")
        
        # Создание новой популяции с элитизмом
        new_population = []
        best_individual = get_best_individual(population)
        new_population.append(best_individual)  # Элита
        print(f"\nЭлита (сохраняется без изменений): Генотип: {best_individual['genotype']}, x: {best_individual['x']}, f(x): {best_individual['fitness']}")
        
        # Добавление остальной части популяции
        for child_genotype in mutated_offspring:
            x = binary_to_x(child_genotype)
            fitness = f(x)
            new_population.append({
                'genotype': child_genotype,
                'x': x,
                'fitness': fitness
            })
            print(f"Добавлен потомок: Генотип: {child_genotype}, x: {x}, f(x): {fitness}")
        
        # Ограничение популяции до исходного размера (4 особи)
        population = new_population[:4]
        print("\nНовая популяция:")
        for individual in population:
            print(f"Генотип: {individual['genotype']}, x: {individual['x']}, f(x): {individual['fitness']}")
        print("\n" + "-"*50 + "\n")
        
        # Обновление лучшего общего
        current_best = get_best_individual(population)
        if current_best['fitness'] > best_overall['fitness']:
            best_overall = current_best

    print("Итоговый результат:")
    print(f"Лучший генотип: {best_overall['genotype']}, x: {best_overall['x']}, f(x): {best_overall['fitness']}")

# Начальная популяция
initial_genotypes = [
    '00100',  # x = 4
    '00100',  # x = 4
    '01000',  # x = 8
    '01000',  # x = 8
    '00010',  # x = 2
    '00010',  # x = 2
    '00001',  # x = 1
    '00001'   # x = 1
]

# Для соответствия изначальной популяции размера 4, выбираем первые 4 особи
initial_genotypes = initial_genotypes[:4]

# Запуск генетического алгоритма
genetic_algorithm(initial_genotypes)
