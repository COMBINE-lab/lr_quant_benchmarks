import numpy as np
import argparse

def calculate_statistics(filename):
    # Read lengths from the file
    with open(filename, 'r') as file:
        lengths = [float(line.strip()) for line in file]
    
    # Convert list to a numpy array
    lengths_array = np.array(lengths)
    
    # Calculate mean and standard deviation
    mean_length = np.mean(lengths_array)
    std_length = np.std(lengths_array)
    
    # Print results
    print(f"Mean length: {mean_length:.2f}")
    print(f"Standard deviation: {std_length:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a file to calculate statistics.")
    parser.add_argument('input_file', type=str, help='Path to the input file')
    args = parser.parse_args()
    calculate_statistics(args.input_file)

