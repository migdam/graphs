#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the style
sns.set_theme(style="whitegrid")

def create_pie_chart(data_path="../data/sample_data.csv", output_path="../examples/pie_chart.png"):
    # Read the data
    df = pd.read_csv(data_path)
    
    # Aggregate data by category (sum of values)
    category_data = df.groupby('category')['value'].sum()
    
    # Create the pie chart
    plt.figure(figsize=(10, 8))
    colors = sns.color_palette('pastel')[0:len(category_data)]
    
    wedges, texts, autotexts = plt.pie(category_data, 
                                        labels=[f'Category {cat}' for cat in category_data.index],
                                        autopct='%1.1f%%',
                                        colors=colors,
                                        startangle=90,
                                        explode=[0.05] * len(category_data))
    
    # Customize the chart
    plt.title('Distribution by Category', fontsize=16, pad=20)
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    # Ensure the examples directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Pie chart saved to {output_path}")
    
    # Show the chart
    plt.show()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a pie chart from CSV data')
    parser.add_argument('--data', type=str, default='../data/sample_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/pie_chart.png',
                        help='Path to save the output image')
    
    args = parser.parse_args()
    create_pie_chart(args.data, args.output)
