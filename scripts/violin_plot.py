#!/usr/bin/env python3
"""
Violin Plot Generator
Creates violin plots for statistical distribution visualization.
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


def create_violin_plot(data_path="../data/statistical_data.csv", 
                       output_path="../examples/violin_plot.png",
                       x_col='category',
                       y_col='value',
                       hue_col=None,
                       split=False,
                       output_format='png'):
    """
    Create a violin plot from CSV data.
    
    Args:
        data_path: Path to input CSV file
        output_path: Path to save output image
        x_col: Column name for x-axis (categories)
        y_col: Column name for y-axis (values)
        hue_col: Optional column for color grouping
        split: Whether to split violins when using hue
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
        if hue_col:
            required_cols.append(hue_col)
            
        if not validate_data(df, required_cols):
            return False
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create violin plot
        if hue_col:
            sns.violinplot(data=df, x=x_col, y=y_col, hue=hue_col, 
                          split=split, palette='Set2', inner='box', ax=ax)
        else:
            sns.violinplot(data=df, x=x_col, y=y_col, 
                          palette='muted', inner='box', ax=ax)
        
        # Add strip plot for individual points
        if not split:
            sns.stripplot(data=df, x=x_col, y=y_col, 
                         color='black', alpha=0.3, size=3, ax=ax)
        
        # Customize the chart
        plt.title(f'Distribution of {y_col.capitalize()} by {x_col.capitalize()}', 
                 fontsize=16, fontweight='bold')
        plt.xlabel(x_col.capitalize(), fontsize=12)
        plt.ylabel(y_col.capitalize(), fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        
        # Rotate x-axis labels if needed
        if len(df[x_col].unique()) > 5:
            plt.xticks(rotation=45, ha='right')
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Adjust output path extension
        output_path = output_path.rsplit('.', 1)[0] + f'.{output_format}'
        
        # Save the chart
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, format=output_format)
        logger.info(f"Violin plot saved to {output_path}")
        
        # Show the chart
        plt.show()
        return True
        
    except Exception as e:
        logger.error(f"Error creating violin plot: {str(e)}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate a violin plot from CSV data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--data', type=str, default='../data/statistical_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/violin_plot.png',
                        help='Path to save the output image')
    parser.add_argument('--x', type=str, default='category',
                        help='Column name for x-axis (categories)')
    parser.add_argument('--y', type=str, default='value',
                        help='Column name for y-axis (values)')
    parser.add_argument('--hue', type=str, default=None,
                        help='Column name for color grouping (optional)')
    parser.add_argument('--split', action='store_true',
                        help='Split violins when using hue')
    parser.add_argument('--format', type=str, default='png', choices=['png', 'svg', 'pdf'],
                        help='Output format')
    
    args = parser.parse_args()
    
    success = create_violin_plot(
        args.data,
        args.output,
        args.x,
        args.y,
        args.hue,
        args.split,
        args.format
    )
    
    sys.exit(0 if success else 1)
