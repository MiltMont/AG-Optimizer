import random
import subprocess
import os
from deap import base, creator, tools, algorithms
import numpy as np
import sys
from flags import FLAGS
from utils import verify_source_file

def compile_and_measure(flags):
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

def eval_flags(individual):
    """Evaluate the fitness of an individual (set of flags)."""
    # Convert boolean values to actual flags
    active_flags = [flag for flag, active in zip(FLAGS, individual) if active]
    
    # If no flags are selected, return worst fitness
    if not active_flags:
        return float('inf'),
    
    # Measure file size with these flags
    size = compile_and_measure(active_flags)
    return size,

def create_toolbox(source_file):
    toolbox = base.Toolbox()
    
    # Attribute generator: each flag is either used (1) or not (0)
    toolbox.register("attr_bool", random.randint, 0, 1)
    
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, 
                     toolbox.attr_bool, n=len(FLAGS))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    # Genetic operators
    toolbox.register("evaluate", eval_flags)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    return toolbox

def optimize_flags(source_file, population_size=50, generations=5):
    """Main optimization function."""
    toolbox = create_toolbox(source_file)
    
    # Create initial population
    pop = toolbox.population(n=population_size)
    hof = tools.HallOfFame(1)
    
    # Statistics setup
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    # Run the evolution
    pop, _ = algorithms.eaSimple(pop, toolbox,
                                     cxpb=0.7,  # crossover probability
                                     mutpb=0.2,  # mutation probability
                                     ngen=generations,
                                     stats=stats,
                                     halloffame=hof,
                                     verbose=True)
    
    # Get best flags
    best_individual = hof[0]
    best_flags = [flag for flag, active in zip(FLAGS, best_individual) if active]
    
    return best_flags, best_individual.fitness.values[0]

def main():
    # Check if source file is provided as command line argument
    if len(sys.argv) != 2:
        print("Usage: python gcc_flag_optimizer.py <source_file>")
        sys.exit(1)
    
    global source_file
    source_file = sys.argv[1]
    
    # Create fitness and individual classes
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    try:
        # Verify source file exists and is accessible
        verify_source_file(source_file)
        
        print("Starting GCC flag optimization...")
        print(f"Source file: {source_file}")
        print(f"Available flags: {', '.join(FLAGS)}")
        
        # Run optimization
        best_flags, best_size = optimize_flags(source_file)
        
        print("\nOptimization complete!")
        print(f"Best flags found: {' '.join(best_flags)}")
        print(f"Resulting file size: {best_size} bytes")
        
        # Compare with standard optimization levels
        print("\nComparison with standard optimization levels:")
        for opt in ['-O0', '-O1', '-O2', '-O3', '-Os']:
            size = compile_and_measure([opt])
            print(f"{opt}: {size} bytes")
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Clean up any remaining output files
        if os.path.exists('output'):
            os.remove('output')

if __name__ == "__main__":
    main()
