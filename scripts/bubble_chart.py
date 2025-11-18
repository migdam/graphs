#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set the style
sns.set_theme(style="whitegrid")

def create_bubble_chart(data_path="../data/sample_data.csv", output_path="../examples/bubble_chart.png"):
    # Read the data
    df = pd.read_csv(data_path)
    
    # Add a size dimension based on value
    df['size'] = df['value'] * 10
    
    # Create the bubble chart
    plt.figure(figsize=(12, 8))
    
    # Plot bubbles for each category
    categories = df['category'].unique()
    colors = sns.color_palette('husl', len(categories))
    
    for idx, category in enumerate(categories):
        category_data = df[df['category'] == category]
        plt.scatter(category_data.index, 
                   category_data['value'],
                   s=category_data['size'],
                   c=[colors[idx]],
                   alpha=0.6,
                   label=f'Category {category}',
                   edgecolors='black',
                   linewidth=1)
    
    # Customize the chart
    plt.title('Bubble Chart - Size Represents Value Magnitude', fontsize=16)
    plt.xlabel('Data Point Index', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.legend(title='Category', loc='best')
    plt.grid(True, alpha=0.3)
    
    # Ensure the examples directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Bubble chart saved to {output_path}")
    
    # Show the chart
    plt.show()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a bubble chart from CSV data')
    parser.add_argument('--data', type=str, default='../data/sample_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/bubble_chart.png',
                        help='Path to save the output image')
    
    args = parser.parse_args()
    create_bubble_chart(args.data, args.output)
