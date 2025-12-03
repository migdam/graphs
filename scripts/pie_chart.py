#!/usr/bin/env python3
"""
Pie Chart Generator
Creates pie charts and donut charts for categorical distribution visualization.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Set the style
sns.set_theme(style="whitegrid")


def validate_data(df, required_columns):
    """Validate that the DataFrame contains required columns."""
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing required columns: {missing_cols}")
        logger.info(f"Available columns: {list(df.columns)}")
        return False
    return True


def create_pie_chart(data_path="../data/categorical_data.csv", 
                     output_path="../examples/pie_chart.png",
                     category_col='category',
                     value_col='value',
                     donut=False,
                     output_format='png'):
    """
    Create a pie or donut chart from CSV data.
    
    Args:
        data_path: Path to input CSV file
        output_path: Path to save output image
        category_col: Column name for categories
        value_col: Column name for values
        donut: Whether to create a donut chart (hollow center)
        output_format: Output format (png, svg, pdf)
    """
    try:
        # Check if file exists
        if not os.path.exists(data_path):
            logger.error(f"Data file not found: {data_path}")
            return False
        
        # Read the data
        logger.info(f"Reading data from {data_path}")
        df = pd.read_csv(data_path)
        
        # Validate required columns
        if not validate_data(df, [category_col, value_col]):
            return False
        
        # Aggregate data by category
        category_data = df.groupby(category_col)[value_col].sum().reset_index()
        category_data = category_data.sort_values(value_col, ascending=False)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create color palette
        colors = sns.color_palette('Set3', n_colors=len(category_data))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            category_data[value_col],
            labels=category_data[category_col],
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 11}
        )
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Create donut effect if requested
        if donut:
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig.gca().add_artist(centre_circle)
        
        # Customize the chart
        chart_type = 'Donut' if donut else 'Pie'
        plt.title(f'{chart_type} Chart: Distribution by {category_col.capitalize()}', 
                 fontsize=16, fontweight='bold', pad=20)
        
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        
        # Add legend with values
        legend_labels = [f'{cat}: {val:,.0f}' 
                        for cat, val in zip(category_data[category_col], 
                                           category_data[value_col])]
        plt.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Adjust output path extension
        output_path = output_path.rsplit('.', 1)[0] + f'.{output_format}'
        
        # Save the chart
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, format=output_format, bbox_inches='tight')
        logger.info(f"Pie chart saved to {output_path}")
        
        # Show the chart
        plt.show()
        return True
        
    except Exception as e:
        logger.error(f"Error creating pie chart: {str(e)}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate a pie or donut chart from CSV data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--data', type=str, default='../data/categorical_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/pie_chart.png',
                        help='Path to save the output image')
    parser.add_argument('--category', type=str, default='category',
                        help='Column name for categories')
    parser.add_argument('--value', type=str, default='value',
                        help='Column name for values')
    parser.add_argument('--donut', action='store_true',
                        help='Create a donut chart instead of pie chart')
    parser.add_argument('--format', type=str, default='png', choices=['png', 'svg', 'pdf'],
                        help='Output format')
    
    args = parser.parse_args()
    
    success = create_pie_chart(
        args.data,
        args.output,
        args.category,
        args.value,
        args.donut,
        args.format
    )
    
    sys.exit(0 if success else 1)
