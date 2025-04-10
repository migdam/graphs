#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the style
sns.set_theme(style="whitegrid")

def create_line_chart(data_path="../data/sample_data.csv", output_path="../examples/line_chart.png"):
    # Read the data
    df = pd.read_csv(data_path)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot lines for each category
    for category, group in df.groupby('category'):
        group.plot(x='date', y='value', ax=ax, label=f'Category {category}', marker='o')
    
    # Customize the chart
    plt.title('Sample Line Chart', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.legend(title='Category')
    plt.grid(True, alpha=0.3)
    
    # Ensure the examples directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Line chart saved to {output_path}")
    
    # Show the chart
    plt.show()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a line chart from CSV data')
    parser.add_argument('--data', type=str, default='../data/sample_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/line_chart.png',
                        help='Path to save the output image')
    
    args = parser.parse_args()
    create_line_chart(args.data, args.output)