#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

def create_3d_surface(data_path="../data/sample_data.csv", output_path="../examples/surface_3d.png"):
    # Read the data
    df = pd.read_csv(data_path)
    
    # Create a mesh grid for 3D surface
    # For demonstration, we'll create a synthetic surface based on the data
    categories = df['category'].unique()
    dates = df['date'].unique()
    
    # Create meshgrid
    X, Y = np.meshgrid(range(len(dates)), range(len(categories)))
    
    # Pivot the data to create Z values
    pivot_data = df.pivot(index='category', columns='date', values='value')
    Z = pivot_data.values
    
    # Create 3D plot
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot surface
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, edgecolor='none')
    
    # Customize the chart
    ax.set_title('3D Surface Plot of Values', fontsize=16, pad=20)
    ax.set_xlabel('Date Index', fontsize=11)
    ax.set_ylabel('Category Index', fontsize=11)
    ax.set_zlabel('Value', fontsize=11)
    
    # Add colorbar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    # Ensure the examples directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"3D surface plot saved to {output_path}")
    
    # Show the chart
    plt.show()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a 3D surface plot from CSV data')
    parser.add_argument('--data', type=str, default='../data/sample_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/surface_3d.png',
                        help='Path to save the output image')
    
    args = parser.parse_args()
    create_3d_surface(args.data, args.output)
