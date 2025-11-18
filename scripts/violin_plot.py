#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the style
sns.set_theme(style="whitegrid")

def create_violin_plot(data_path="../data/sample_data.csv", output_path="../examples/violin_plot.png"):
    # Read the data
    df = pd.read_csv(data_path)
    
    # Create the violin plot
    plt.figure(figsize=(10, 6))
    violin_plot = sns.violinplot(x='category', y='value', data=df, palette='muted', inner='box')
    
    # Customize the chart
    plt.title('Violin Plot of Values by Category', fontsize=16)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    
    # Ensure the examples directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Violin plot saved to {output_path}")
    
    # Show the chart
    plt.show()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a violin plot from CSV data')
    parser.add_argument('--data', type=str, default='../data/sample_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/violin_plot.png',
                        help='Path to save the output image')
    
    args = parser.parse_args()
    create_violin_plot(args.data, args.output)
