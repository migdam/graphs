#!/usr/bin/env python3
"""
Area Chart Generator
Creates stacked area charts for time series comparison.
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


def create_area_chart(data_path="../data/time_series_data.csv", 
                      output_path="../examples/area_chart.png",
                      time_col='date',
                      value_cols=None,
                      stacked=True,
                      output_format='png'):
    """
    Create an area chart from CSV data.
    
    Args:
        data_path: Path to input CSV file
        output_path: Path to save output image
        time_col: Column name for time/x-axis
        value_cols: List of column names for values (if None, uses all numeric columns)
        stacked: Whether to create a stacked area chart
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
        
        # Convert time column to datetime if needed
        if time_col in df.columns:
            try:
                df[time_col] = pd.to_datetime(df[time_col])
            except:
                logger.warning(f"Could not convert {time_col} to datetime, using as-is")
        
        # Validate time column exists
        if not validate_data(df, [time_col]):
            return False
        
        # Determine value columns
        if value_cols is None:
            value_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            if time_col in value_cols:
                value_cols.remove(time_col)
            logger.info(f"Auto-detected value columns: {value_cols}")
        
        if not value_cols:
            logger.error("No numeric value columns found")
            return False
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create color palette
        colors = sns.color_palette('husl', n_colors=len(value_cols))
        
        # Create area chart
        if stacked:
            ax.stackplot(df[time_col], 
                        *[df[col] for col in value_cols],
                        labels=value_cols,
                        colors=colors,
                        alpha=0.7)
        else:
            for i, col in enumerate(value_cols):
                ax.fill_between(df[time_col], df[col], 
                               alpha=0.5, color=colors[i], label=col)
        
        # Customize the chart
        chart_type = 'Stacked' if stacked else 'Overlapping'
        plt.title(f'{chart_type} Area Chart Over Time', fontsize=16, fontweight='bold')
        plt.xlabel(time_col.capitalize(), fontsize=12)
        plt.ylabel('Value', fontsize=12)
        plt.legend(loc='upper left', framealpha=0.9)
        plt.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Adjust output path extension
        output_path = output_path.rsplit('.', 1)[0] + f'.{output_format}'
        
        # Save the chart
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, format=output_format)
        logger.info(f"Area chart saved to {output_path}")
        
        # Show the chart
        plt.show()
        return True
        
    except Exception as e:
        logger.error(f"Error creating area chart: {str(e)}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate an area chart from CSV data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--data', type=str, default='../data/time_series_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/area_chart.png',
                        help='Path to save the output image')
    parser.add_argument('--time', type=str, default='date',
                        help='Column name for time/x-axis')
    parser.add_argument('--columns', type=str, nargs='+', default=None,
                        help='Specific columns to plot (optional, defaults to all numeric)')
    parser.add_argument('--no-stack', action='store_true',
                        help='Create overlapping instead of stacked areas')
    parser.add_argument('--format', type=str, default='png', choices=['png', 'svg', 'pdf'],
                        help='Output format')
    
    args = parser.parse_args()
    
    success = create_area_chart(
        args.data,
        args.output,
        args.time,
        args.columns,
        not args.no_stack,
        args.format
    )
    
    sys.exit(0 if success else 1)
