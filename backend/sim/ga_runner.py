def run_ga(config_file):
    with open(config_file) as f:
        cfg = json.load(f)

    base = load_scenario(cfg["scenario_name"])
    pop_size = cfg["population_size"]
    generations = cfg["generations"]
    mutation_rate = cfg["mutation_rate"]
    objective = cfg["objective"]

    base_day = base["base_day"]
    path = f"/opt/ptp-data/live/{base_day}/gnss_samples.json"

    with open(path) as f:
        samples = json.load(f)

    # Initialize population
    population = [json.loads(json.dumps(base)) for _ in range(pop_size)]

    for gen in range(generations):
        scored = []

        for scenario in population:
            results = run_simulation(samples, scenario)
            score = fitness(results, objective)
            scored.append((score, scenario))

        # Sort by score descending (worst-case first)
        scored.sort(key=lambda x: -x[0])

        # Keep top half
        survivors = [s for _, s in scored[:pop_size // 2]]

        # Breed new population
        new_pop = survivors.copy()
        while len(new_pop) < pop_size:
            a, b = random.sample(survivors, 2)
            child = crossover(a, b)
            child = mutate(child, mutation_rate)
            new_pop.append(child)

        population = new_pop

    # Final evaluation
    final = []
    for scenario in population:
        results = run_simulation(samples, scenario)
        score = fitness(results, objective)
        final.append((score, scenario))

    final.sort(key=lambda x: -x[0])
    return final[:10]  # top 10 worst-case scenarios
