#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the style
sns.set_theme(style="whitegrid")

def create_area_chart(data_path="../data/sample_data.csv", output_path="../examples/area_chart.png"):
    # Read the data
    df = pd.read_csv(data_path)
    
    # Pivot data to get categories as columns
    pivot_df = df.pivot(index='date', columns='category', values='value')
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create area chart
    pivot_df.plot.area(ax=ax, alpha=0.7, stacked=True)
    
    # Customize the chart
    plt.title('Stacked Area Chart by Category', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.legend(title='Category', loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Ensure the examples directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Area chart saved to {output_path}")
    
    # Show the chart
    plt.show()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate an area chart from CSV data')
    parser.add_argument('--data', type=str, default='../data/sample_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/area_chart.png',
                        help='Path to save the output image')
    
    args = parser.parse_args()
    create_area_chart(args.data, args.output)
