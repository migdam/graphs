#!/usr/bin/env python3
"""
Line Chart Generator
Creates line charts for visualizing trends over time or continuous data.
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


def create_line_chart(data_path="../data/sample_data.csv", 
                      output_path="../examples/line_chart.png",
                      output_format='png'):
    """
    Create a line chart from CSV data.
    
    Args:
        data_path: Path to input CSV file
        output_path: Path to save output image
        output_format: Output format (png, svg, pdf)
        
    Returns:
        bool: True if successful, False otherwise
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
        if not validate_data(df, ['date', 'value', 'category']):
            return False
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot lines for each category
        for category, group in df.groupby('category'):
            group.plot(x='date', y='value', ax=ax, label=f'Category {category}', marker='o')
        
        # Customize the chart
        plt.title('Sample Line Chart', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Value', fontsize=12)
        plt.legend(title='Category')
        plt.grid(True, alpha=0.3)
        
        # Ensure the examples directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Adjust output path extension
        output_path = output_path.rsplit('.', 1)[0] + f'.{output_format}'
        
        # Save the chart
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, format=output_format)
        logger.info(f"Line chart saved to {output_path}")
        
        # Show the chart
        plt.show()
        return True
        
    except Exception as e:
        logger.error(f"Error creating line chart: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate a line chart from CSV data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--data', type=str, default='../data/sample_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/line_chart.png',
                        help='Path to save the output image')
    parser.add_argument('--format', type=str, default='png', choices=['png', 'svg', 'pdf'],
                        help='Output format')
    
    args = parser.parse_args()
    success = create_line_chart(args.data, args.output, args.format)
    sys.exit(0 if success else 1)
