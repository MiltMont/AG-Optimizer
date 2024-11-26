import os
import sys
from flags import FLAGS
from utils import verify_source_file
from deap import creator, base
from utils import optimize_flags, verify_source_file, compile_and_measure

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
            size = compile_and_measure([opt], source_file)
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
