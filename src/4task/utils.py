import random

def calculate_route_cost(route, distance_matrix, city_indices):
    cost = 0
    detailed_calculation = ""
    num_cities = len(route)
    for i in range(num_cities):
        from_city = route[i]
        to_city = route[(i + 1) % num_cities]
        dist = distance_matrix[city_indices[from_city]][city_indices[to_city]]
        cost += dist
        detailed_calculation += f"{dist}"
        if i < num_cities - 1:
            detailed_calculation += " + "
    detailed_calculation += f" = {cost}"
    return cost, detailed_calculation

def initialize_parents(num_parents, cities):
    parents = []
    generated = set()
    while len(parents) < num_parents:
        parent = cities[:]
        random.shuffle(parent)
        parent_tuple = tuple(parent)
        if parent_tuple not in generated:
            generated.add(parent_tuple)
            parents.append(parent)
    return parents

def advanced_crossover(parent1, parent2):
    """
    Performs an advanced crossover (Order Crossover - OX) between two parents and returns two offspring along with crossover points.
    """
    size = len(parent1)
    cp1, cp2 = sorted(random.sample(range(size), 2))
    
    def ox_crossover(p1, p2, cp1, cp2):
        child = [None]*size
        # Copy the segment from p1 to child
        child[cp1:cp2+1] = p1[cp1:cp2+1]
        # Fill the rest from p2 in order
        p2_idx = (cp2 + 1) % size
        c_idx = (cp2 + 1) % size
        while None in child:
            if p2[p2_idx] not in child:
                child[c_idx] = p2[p2_idx]
                c_idx = (c_idx + 1) % size
            p2_idx = (p2_idx + 1) % size
        return child

    offspring1 = ox_crossover(parent1, parent2, cp1, cp2)
    offspring2 = ox_crossover(parent2, parent1, cp1, cp2)

    return offspring1, offspring2, cp1, cp2