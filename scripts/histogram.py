#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the style
sns.set_theme(style="whitegrid")

def create_histogram(data_path="../data/sample_data.csv", output_path="../examples/histogram.png"):
    # Read the data
    df = pd.read_csv(data_path)
    
    # Create the histogram
    plt.figure(figsize=(12, 6))
    
    # Create histogram for each category
    for category in df['category'].unique():
        category_data = df[df['category'] == category]['value']
        plt.hist(category_data, alpha=0.6, label=f'Category {category}', bins=10, edgecolor='black')
    
    # Customize the chart
    plt.title('Distribution of Values (Histogram)', fontsize=16)
    plt.xlabel('Value', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.legend(title='Category')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Ensure the examples directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Histogram saved to {output_path}")
    
    # Show the chart
    plt.show()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a histogram from CSV data')
    parser.add_argument('--data', type=str, default='../data/sample_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/histogram.png',
                        help='Path to save the output image')
    
    args = parser.parse_args()
    create_histogram(args.data, args.output)
