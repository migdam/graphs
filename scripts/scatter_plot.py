#!/usr/bin/env python3
"""
Scatter Plot Generator
Creates scatter plots with optional trend lines and color coding.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Set the style
sns.set_theme(style="whitegrid")


def validate_data(df, required_columns):
    """
    Validate that the DataFrame contains required columns.
    
    Args:
        df: pandas DataFrame
        required_columns: list of required column names
        
    Returns:
        bool: True if valid, False otherwise
    """
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing required columns: {missing_cols}")
        logger.info(f"Available columns: {list(df.columns)}")
        return False
    return True


def create_scatter_plot(data_path="../data/correlation_data.csv", 
                       output_path="../examples/scatter_plot.png",
                       x_col='x',
                       y_col='y',
                       color_col=None,
                       add_trend=True,
                       output_format='png'):
    """
    Create a scatter plot from CSV data.
    
    Args:
        data_path: Path to input CSV file
        output_path: Path to save output image
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        color_col: Optional column name for color coding
        add_trend: Whether to add a trend line
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
        required_cols = [x_col, y_col]
        if color_col:
            required_cols.append(color_col)
            
        if not validate_data(df, required_cols):
            return False
        
        # Create figure and axis
        plt.figure(figsize=(10, 6))
        
        # Create scatter plot
        if color_col:
            scatter = sns.scatterplot(data=df, x=x_col, y=y_col, hue=color_col, 
                                     palette='viridis', s=100, alpha=0.7)
        else:
            scatter = sns.scatterplot(data=df, x=x_col, y=y_col, 
                                     color='steelblue', s=100, alpha=0.7)
        
        # Add trend line if requested
        if add_trend:
            # Calculate linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(df[x_col], df[y_col])
            line = slope * df[x_col] + intercept
            plt.plot(df[x_col], line, 'r--', alpha=0.8, linewidth=2, 
                    label=f'Trend (R² = {r_value**2:.3f})')
            plt.legend()
        
        # Customize the chart
        plt.title(f'Scatter Plot: {y_col} vs {x_col}', fontsize=16, fontweight='bold')
        plt.xlabel(x_col.capitalize(), fontsize=12)
        plt.ylabel(y_col.capitalize(), fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Adjust output path extension
        output_path = output_path.rsplit('.', 1)[0] + f'.{output_format}'
        
        # Save the chart
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, format=output_format)
        logger.info(f"Scatter plot saved to {output_path}")
        
        # Show the chart
        plt.show()
        return True
        
    except Exception as e:
        logger.error(f"Error creating scatter plot: {str(e)}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate a scatter plot from CSV data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--data', type=str, default='../data/correlation_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/scatter_plot.png',
                        help='Path to save the output image')
    parser.add_argument('--x', type=str, default='x',
                        help='Column name for x-axis')
    parser.add_argument('--y', type=str, default='y',
                        help='Column name for y-axis')
    parser.add_argument('--color', type=str, default=None,
                        help='Column name for color coding (optional)')
    parser.add_argument('--no-trend', action='store_true',
                        help='Disable trend line')
    parser.add_argument('--format', type=str, default='png', choices=['png', 'svg', 'pdf'],
                        help='Output format')
    
    args = parser.parse_args()
    
    success = create_scatter_plot(
        args.data, 
        args.output,
        args.x,
        args.y,
        args.color,
        not args.no_trend,
        args.format
    )
    
    sys.exit(0 if success else 1)
