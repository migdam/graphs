#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the style
sns.set_theme(style="whitegrid")

def create_scatter_plot(data_path="../data/sample_data.csv", output_path="../examples/scatter_plot.png"):
    # Read the data
    df = pd.read_csv(data_path)
    
    # Create figure and axis
    plt.figure(figsize=(10, 6))
    
    # Create scatter plot with different colors for each category
    for category in df['category'].unique():
        category_data = df[df['category'] == category]
        plt.scatter(category_data.index, category_data['value'], 
                   label=f'Category {category}', s=100, alpha=0.6)
    
    # Customize the chart
    plt.title('Scatter Plot of Values', fontsize=16)
    plt.xlabel('Data Point Index', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.legend(title='Category')
    plt.grid(True, alpha=0.3)
    
    # Ensure the examples directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Scatter plot saved to {output_path}")
    
    # Show the chart
    plt.show()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a scatter plot from CSV data')
    parser.add_argument('--data', type=str, default='../data/sample_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/scatter_plot.png',
                        help='Path to save the output image')
    
    args = parser.parse_args()
    create_scatter_plot(args.data, args.output)
