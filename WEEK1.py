
import random
traffic = [45, 30, 15, 10]

POP_SIZE = 30
GENERATIONS = 100
MIN_GREEN = 10
MAX_GREEN = 60
CYCLE = 120
CLEARANCE = 20

AVAILABLE_GREEN = CYCLE - CLEARANCE

# Generate feasible timing allocation
def create_solution():
    cuts = sorted(random.sample(
        range(1, AVAILABLE_GREEN),
        3
    ))

    values = [
        cuts[0],
        cuts[1] - cuts[0],
        cuts[2] - cuts[1],
        AVAILABLE_GREEN - cuts[2]
    ]

    return repair(values)

def repair(x):
    x = [max(MIN_GREEN, min(MAX_GREEN, v))
         for v in x]

    remaining = AVAILABLE_GREEN - 4 * MIN_GREEN

    weights = [max(0.01, v - MIN_GREEN) for v in x]
    total = sum(weights)

    result = [
        MIN_GREEN + remaining * w / total
        for w in weights
    ]

    return result

def objective(x):
    total = 0

    for i in range(4):
        waiting = max(0, 60 - x[i])

        total += traffic[i] * waiting

    return total

population = [
    repair([random.uniform(10, 60) for _ in range(4)])
    for _ in range(POP_SIZE)
]

for generation in range(GENERATIONS):

    population.sort(key=objective)

    new_population = [population[0][:]]

    while len(new_population) < POP_SIZE:

        def select():
            candidates = random.sample(population, 3)
            return min(candidates, key=objective)

        p1 = select()
        p2 = select()

        alpha = random.random()

        child = [
            alpha * p1[i] + (1 - alpha) * p2[i]
            for i in range(4)
        ]

        if random.random() < 0.2:
            i = random.randrange(4)
            child[i] += random.uniform(-5, 5)

        child = repair(child)

        new_population.append(child)

    population = new_population

best = min(population, key=objective)

print("Optimal green times:")
directions = ["North", "South", "East", "West"]

for direction, green in zip(directions, best):
    print(direction, round(green, 2), "seconds")

print("Objective value:", round(objective(best), 2))
print("Total cycle:", CYCLE, "seconds")