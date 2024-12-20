from deap import base, tools, creator, algorithms
from flags import FLAGS
import subprocess
import os
import random 
import numpy as np
import functools

def verify_source_file(filename):
    """Verify that the source file exists and is accessible."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Source file '{filename}' not found!")
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"'{filename}' is not a regular file!")
    if not os.access(filename, os.R_OK):
        raise FileNotFoundError(f"Source file '{filename}' is not readable!")
    
    # Check if it's a C source file
    if not filename.endswith(('.c', '.cpp')):
        raise FileNotFoundError(f"File '{filename}' does not appear to be a C/C++ source file!")

def compile_and_measure(flags, source_file):
    """Compile the source file with given flags and return file size."""
    try:
        # Create compilation command
        cmd = ['gcc'] + flags + ['-o', 'output', source_file]
        
        # Run compilation
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            # Keep track of failed compilations but don't raise an error
            print(f"Warning: Compilation failed with flags {' '.join(flags)}")
            print(f"Error message: {result.stderr}")
            return float('inf')
        
        # Get file size
        size = os.path.getsize('output')
        
        # Clean up
        if os.path.exists('output'):
            os.remove('output')
        
        return size
    except Exception as e:
        print(f"Error during compilation: {e}")
        return float('inf')

def eval_flags(individual, source_file):
    """Evaluate the fitness of an individual (set of flags)."""
    # Convert boolean values to actual flags
    active_flags = [flag for flag, active in zip(FLAGS, individual) if active]
    
    # If no flags are selected, return worst fitness
    if not active_flags:
        return float('inf'),
    
    # Measure file size with these flags
    size = compile_and_measure(active_flags, source_file)
    penalty = len(active_flags)*0.01
    return size + penalty,

def create_toolbox(source_file):
    toolbox = base.Toolbox()
    
    # Attribute generator: each flag is either used (1) or not (0)
    toolbox.register("attr_bool", random.randint, 0, 1)
    
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, 
                     toolbox.attr_bool, n=len(FLAGS))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    # Genetic operators
    partial = lambda y: eval_flags(y, source_file)
    toolbox.register("evaluate", partial)
    toolbox.register("mate", tools.cxUniform, indpb=0.5)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.3)
    toolbox.register("select", tools.selTournament, tournsize=5)
    
    return toolbox

def optimize_flags(
        source_file, 
        population_size=80, 
        generations=10, 
        stagnation_limit=5, 
        diversity_threshold=0.4,  
        plot_file="file_size_plot.png"):
    """Main optimization function."""
    toolbox = create_toolbox(source_file)
    
    # Create initial population
    pop = hybrid_population(toolbox, population_size, source_file)
    hof = tools.HallOfFame(3)
    
    # Statistics setup
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)

    best_fitness = float('inf')
    stagnation_counter = 0

    for gen in range(generations):
        pop, _ = algorithms.eaSimple(pop, toolbox, 
                                    cxpb=0.8, 
                                    mutpb=0.4,
                                    ngen=1, stats=stats, halloffame=hof, verbose=True)

        current_best = hof[random.randint(0,2)].fitness.values[0]
        print(hof)
        if current_best < best_fitness:
            best_fitness = current_best
            stagnation_counter = 0
        else: 
            stagnation_counter += 1

        if stagnation_counter >= stagnation_limit: 
            print(f"Stagnation detected at generation {gen}. Reinitializing population")
            pop = hybrid_population(toolbox, population_size, source_file) 
            stagnation_counter = 0

        # Calculate diversity
        active_flags = [[flag for flag, active in zip(FLAGS, ind) if active] for ind in pop]
        diversity = len(set(tuple(sorted(flags)) for flags in active_flags)) / population_size

        print(f"diversity: {diversity:.2f}")
        if diversity < diversity_threshold:
            print(f"Low diversity detected: {diversity:.2f}. Adding random individuals.")
            new_individuals = toolbox.population(n=int(0.2 * population_size))
            pop.extend(new_individuals)

    
    # # Plot file size reduction 
    # plt.figure(figsize=(10,6))
    # plt.plot(range(1, generations + 1), file_sizes_per_generation, marker='o', label='Min Size per Generation')
    # plt.xlabel("Generation")
    # plt.ylabel("Compiled File Size (bytes)")
    # plt.title("Average File Size Across Generations")
    # plt.legend()
    # plt.grid()
    #
    # # Save plot file
    # plt.savefig(plot_file)
    # print(f"Plot saved as {plot_file}")

    # Get best flags
    best_individual = hof[0]
    best_flags = [flag for flag, active in zip(FLAGS, best_individual) if active]
    
    return best_flags, best_individual.fitness.values[0]

def hybrid_population(toolbox, population_size, source_file):
    """Create a hybrid population with seeded and random individuals"""
    seeded_flags = [
        ['-O0'],
        ['-O1'],
        ['-O2'],
        ['-O3'],
        ['-Os'],
        ['-Ofast']
    ]

    seeded_individuals = []

    for flags in seeded_flags: 
        individual = [1 if flags in flags else 0 for flag in FLAGS]
        ind = creator.Individual(individual)
        ind.fitness.values = eval_flags(ind, source_file)
        seeded_individuals.append(ind)

    random_population = toolbox.population(n=population_size - len(seeded_individuals))
    return seeded_individuals + random_population

