#!/usr/bin/env python3
"""
Gantt Chart Generator
Creates Gantt charts for project timeline visualization with task dependencies.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import numpy as np
from datetime import datetime, timedelta
import os
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def validate_data(df, required_columns):
    """Validate that the DataFrame contains required columns."""
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing required columns: {missing_cols}")
        logger.info(f"Available columns: {list(df.columns)}")
        return False
    return True


def create_gantt_chart(data_path="../data/project_timeline.csv", 
                       output_path="../examples/gantt_chart.png",
                       output_format='png'):
    """
    Create a Gantt chart from CSV data.
    
    Args:
        data_path: Path to input CSV file
        output_path: Path to save output image
        output_format: Output format (png, svg, pdf)
        
    Expected CSV format:
        task,start_date,end_date,progress,owner
        Planning,2024-01-01,2024-01-15,100,Team A
        Development,2024-01-10,2024-03-15,75,Team B
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
        if not validate_data(df, ['task', 'start_date', 'end_date']):
            return False
        
        # Convert date columns to datetime
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])
        df['duration'] = (df['end_date'] - df['start_date']).dt.days
        
        # Add progress column if not present (default 0)
        if 'progress' not in df.columns:
            df['progress'] = 0
        
        # Create figure
        fig, ax = plt.subplots(figsize=(14, max(6, len(df) * 0.5)))
        
        # Color palette
        colors = plt.cm.Set3(np.linspace(0, 1, len(df)))
        
        # Plot bars
        for idx, row in df.iterrows():
            # Calculate position
            y_pos = len(df) - idx - 1
            
            # Full task bar (light color)
            ax.barh(y_pos, row['duration'], left=mdates.date2num(row['start_date']),
                   height=0.6, color=colors[idx], alpha=0.3, edgecolor='black', linewidth=1)
            
            # Progress bar (darker color)
            if row['progress'] > 0:
                progress_duration = row['duration'] * (row['progress'] / 100)
                ax.barh(y_pos, progress_duration, left=mdates.date2num(row['start_date']),
                       height=0.6, color=colors[idx], alpha=0.8, edgecolor='black', linewidth=1)
            
            # Add progress percentage label
            mid_date = row['start_date'] + (row['end_date'] - row['start_date']) / 2
            ax.text(mdates.date2num(mid_date), y_pos, f"{row['progress']:.0f}%",
                   ha='center', va='center', fontsize=9, fontweight='bold', color='black')
            
            # Add owner if available
            if 'owner' in df.columns and pd.notna(row['owner']):
                ax.text(mdates.date2num(row['end_date']) + 2, y_pos, f"({row['owner']})",
                       ha='left', va='center', fontsize=8, style='italic', color='gray')
        
        # Format x-axis as dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
        plt.xticks(rotation=45, ha='right')
        
        # Set y-axis labels
        ax.set_yticks(range(len(df)))
        ax.set_yticklabels(df['task'][::-1])
        
        # Add vertical line for today
        today = datetime.now()
        if df['start_date'].min() <= pd.Timestamp(today) <= df['end_date'].max():
            ax.axvline(mdates.date2num(today), color='red', linestyle='--', 
                      linewidth=2, alpha=0.7, label='Today')
            ax.legend()
        
        # Customize chart
        plt.title('Project Timeline - Gantt Chart', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Tasks', fontsize=12)
        plt.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Adjust output path extension
        output_path = output_path.rsplit('.', 1)[0] + f'.{output_format}'
        
        # Save the chart
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, format=output_format, bbox_inches='tight')
        logger.info(f"Gantt chart saved to {output_path}")
        
        # Show the chart
        plt.show()
        return True
        
    except Exception as e:
        logger.error(f"Error creating Gantt chart: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate a Gantt chart from CSV data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--data', type=str, default='../data/project_timeline.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/gantt_chart.png',
                        help='Path to save the output image')
    parser.add_argument('--format', type=str, default='png', choices=['png', 'svg', 'pdf'],
                        help='Output format')
    
    args = parser.parse_args()
    success = create_gantt_chart(args.data, args.output, args.format)
    sys.exit(0 if success else 1)
