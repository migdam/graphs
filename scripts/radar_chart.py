#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def create_radar_chart(data_path="../data/sample_data.csv", output_path="../examples/radar_chart.png"):
    # Read the data
    df = pd.read_csv(data_path)
    
    # Calculate mean values for each category
    category_means = df.groupby('category')['value'].mean()
    
    # Number of variables
    categories = list(category_means.index)
    N = len(categories)
    
    # Compute angle for each axis
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    values = list(category_means.values)
    
    # Complete the circle
    angles += angles[:1]
    values += values[:1]
    
    # Create the radar chart
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Plot data
    ax.plot(angles, values, 'o-', linewidth=2, label='Average Value')
    ax.fill(angles, values, alpha=0.25)
    
    # Fix axis to go in the right order
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw axis labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([f'Category {cat}' for cat in categories])
    
    # Customize the chart
    ax.set_ylim(0, max(values) * 1.2)
    ax.set_title('Radar Chart - Average Values by Category', size=16, pad=20)
    ax.grid(True)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    # Ensure the examples directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Radar chart saved to {output_path}")
    
    # Show the chart
    plt.show()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a radar chart from CSV data')
    parser.add_argument('--data', type=str, default='../data/sample_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/radar_chart.png',
                        help='Path to save the output image')
    
    args = parser.parse_args()
    create_radar_chart(args.data, args.output)
