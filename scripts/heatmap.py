#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the style
sns.set_theme(style="white")

def create_heatmap(data_path="../data/sample_data.csv", output_path="../examples/heatmap.png"):
    # Read the data
    df = pd.read_csv(data_path)
    
    # Pivot the data to create a matrix for the heatmap
    # For this example, we'll use date and category as dimensions
    pivot_data = df.pivot(index='date', columns='category', values='value')
    
    # Create the heatmap
    plt.figure(figsize=(10, 8))
    heatmap = sns.heatmap(pivot_data, annot=True, cmap="YlGnBu", fmt=".0f", linewidths=.5)
    
    # Customize the chart
    plt.title('Value Heatmap by Date and Category', fontsize=16)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Date', fontsize=12)
    
    # Ensure the examples directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Heatmap saved to {output_path}")
    
    # Show the chart
    plt.show()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a heatmap from CSV data')
    parser.add_argument('--data', type=str, default='../data/sample_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/heatmap.png',
                        help='Path to save the output image')
    
    args = parser.parse_args()
    create_heatmap(args.data, args.output)