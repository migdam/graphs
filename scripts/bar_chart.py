#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the style
sns.set_theme(style="whitegrid")

def create_bar_chart(data_path="../data/sample_data.csv", output_path="../examples/bar_chart.png"):
    # Read the data
    df = pd.read_csv(data_path)
    
    # Aggregate data by category (sum of values)
    category_data = df.groupby('category')['value'].sum().reset_index()
    
    # Create the bar chart
    plt.figure(figsize=(10, 6))
    chart = sns.barplot(x='category', y='value', data=category_data, palette='viridis')
    
    # Customize the chart
    plt.title('Total Value by Category', fontsize=16)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Total Value', fontsize=12)
    
    # Add value labels on top of the bars
    for i, value in enumerate(category_data['value']):
        chart.text(i, value + 1, f'{value:.0f}', ha='center', fontsize=11)
    
    # Ensure the examples directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Bar chart saved to {output_path}")
    
    # Show the chart
    plt.show()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a bar chart from CSV data')
    parser.add_argument('--data', type=str, default='../data/sample_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/bar_chart.png',
                        help='Path to save the output image')
    
    args = parser.parse_args()
    create_bar_chart(args.data, args.output)