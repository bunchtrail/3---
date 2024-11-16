from input_output import input_distance_matrix, display_results
from utils import initialize_parents, advanced_crossover, calculate_route_cost

def run_genetic_algorithm(distance_matrix, cities, city_indices):
    num_parents = 4
    parents = initialize_parents(num_parents, cities)

    offspring = []
    crossover_info = []
    for i in range(0, num_parents, 2):
        parent1 = parents[i]
        parent2 = parents[i + 1] if i + 1 < num_parents else parents[0]
        child1, child2, cp1, cp2 = advanced_crossover(parent1, parent2)
        offspring.append(child1)
        offspring.append(child2)
        crossover_info.append((cp1, cp2))

    table_data = []
    for idx in range(num_parents):
        parent = parents[idx]
        child = offspring[idx]
        cp1, cp2 = crossover_info[idx // 2]

        parent_cost, parent_detail = calculate_route_cost(parent, distance_matrix, city_indices)
        child_cost, child_detail = calculate_route_cost(child, distance_matrix, city_indices)

        parent_genotype = ''.join(parent[:cp1]) + '*' + ''.join(parent[cp1:cp2+1]) + '*' + ''.join(parent[cp2+1:])
        child_genotype = ' -> '.join(child) + ' -> ' + child[0]

        table_data.append([
            idx + 1,
            parent_genotype,
            parent_detail,
            f"{parent_cost}",
            child_genotype,
            child_detail,
            f"{child_cost}"
        ])

    display_results(table_data, distance_matrix, offspring, city_indices)

def genetic_algorithm():
    distance_matrix = input_distance_matrix()
    cities = ['1', '2', '3', '4', '5']
    city_indices = {city: idx for idx, city in enumerate(cities)}

    while True:
        run_genetic_algorithm(distance_matrix, cities, city_indices)
        repeat = input("Хотите решить задачу еще раз на тех же входных данных? (+/-): ").strip().lower()
        if repeat != '+':
            break