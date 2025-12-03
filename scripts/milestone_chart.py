#!/usr/bin/env python3
"""
Milestone Chart Generator
Creates milestone timeline visualizations for project tracking and planning.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np
from datetime import datetime
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


def create_milestone_chart(data_path="../data/milestones.csv", 
                           output_path="../examples/milestone_chart.png",
                           output_format='png'):
    """
    Create a milestone timeline chart from CSV data.
    
    Args:
        data_path: Path to input CSV file
        output_path: Path to save output image
        output_format: Output format (png, svg, pdf)
        
    Expected CSV format:
        milestone,date,status,description
        Project Kickoff,2024-01-01,completed,Initial team meeting
        Design Phase,2024-01-15,completed,UI/UX design finalized
        Development Start,2024-02-01,in_progress,Backend development
        Beta Release,2024-03-15,upcoming,First beta version
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
        if not validate_data(df, ['milestone', 'date']):
            return False
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Add status column if not present
        if 'status' not in df.columns:
            df['status'] = 'upcoming'
        
        # Sort by date
        df = df.sort_values('date')
        
        # Create figure
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Status colors and markers
        status_config = {
            'completed': {'color': '#2ECC71', 'marker': 'o', 'size': 200},
            'in_progress': {'color': '#F39C12', 'marker': 's', 'size': 200},
            'upcoming': {'color': '#3498DB', 'marker': '^', 'size': 200},
            'at_risk': {'color': '#E74C3C', 'marker': 'D', 'size': 200}
        }
        
        # Draw timeline
        timeline_y = 0.5
        date_nums = mdates.date2num(df['date'])
        ax.plot([date_nums.min() - 5, date_nums.max() + 5], [timeline_y, timeline_y],
               'k-', linewidth=3, alpha=0.3, zorder=1)
        
        # Plot milestones
        for idx, row in df.iterrows():
            status = row['status'].lower() if 'status' in df.columns else 'upcoming'
            config = status_config.get(status, status_config['upcoming'])
            
            date_num = mdates.date2num(row['date'])
            
            # Draw milestone marker
            ax.scatter(date_num, timeline_y, 
                      c=config['color'], 
                      marker=config['marker'],
                      s=config['size'],
                      edgecolors='black',
                      linewidths=2,
                      zorder=3,
                      alpha=0.9)
            
            # Alternate text position (above/below timeline)
            y_offset = 0.15 if idx % 2 == 0 else -0.15
            text_y = timeline_y + y_offset
            va = 'bottom' if y_offset > 0 else 'top'
            
            # Draw connector line from marker to text
            ax.plot([date_num, date_num], 
                   [timeline_y, text_y], 
                   'k--', linewidth=1, alpha=0.4, zorder=2)
            
            # Add milestone name
            ax.text(date_num, text_y + (0.03 if y_offset > 0 else -0.03), 
                   row['milestone'],
                   ha='center', va=va, fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor=config['color'], 
                            alpha=0.3, edgecolor='black', linewidth=1))
            
            # Add date label
            date_str = row['date'].strftime('%Y-%m-%d')
            ax.text(date_num, text_y + (0.08 if y_offset > 0 else -0.08), 
                   date_str,
                   ha='center', va=va, fontsize=8, style='italic', color='gray')
            
            # Add description if available
            if 'description' in df.columns and pd.notna(row['description']):
                ax.text(date_num, text_y + (0.12 if y_offset > 0 else -0.12), 
                       row['description'][:30] + ('...' if len(row['description']) > 30 else ''),
                       ha='center', va=va, fontsize=7, color='dimgray',
                       style='italic')
        
        # Add "Today" marker
        today = datetime.now()
        today_num = mdates.date2num(today)
        if date_nums.min() <= today_num <= date_nums.max():
            ax.axvline(today_num, color='red', linestyle='--', linewidth=2, 
                      alpha=0.6, label='Today', zorder=2)
            ax.text(today_num, timeline_y - 0.3, 'TODAY', 
                   ha='center', fontsize=9, fontweight='bold', color='red',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                            edgecolor='red', linewidth=2))
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        plt.xticks(rotation=45, ha='right')
        
        # Set axis limits and remove y-axis
        ax.set_ylim(-0.5, 1.0)
        ax.set_yticks([])
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # Add legend for status
        legend_elements = []
        for status, config in status_config.items():
            legend_elements.append(
                plt.Line2D([0], [0], marker=config['marker'], color='w',
                          markerfacecolor=config['color'], markeredgecolor='black',
                          markersize=10, label=status.replace('_', ' ').title())
            )
        ax.legend(handles=legend_elements, loc='upper left', 
                 framealpha=0.9, fontsize=9)
        
        # Title and labels
        plt.title('Project Milestones Timeline', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Timeline', fontsize=12)
        
        # Grid
        plt.grid(axis='x', alpha=0.2, linestyle='--')
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Adjust output path extension
        output_path = output_path.rsplit('.', 1)[0] + f'.{output_format}'
        
        # Save the chart
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, format=output_format, bbox_inches='tight')
        logger.info(f"Milestone chart saved to {output_path}")
        
        # Show the chart
        plt.show()
        return True
        
    except Exception as e:
        logger.error(f"Error creating milestone chart: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate a milestone timeline chart from CSV data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--data', type=str, default='../data/milestones.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str, default='../examples/milestone_chart.png',
                        help='Path to save the output image')
    parser.add_argument('--format', type=str, default='png', choices=['png', 'svg', 'pdf'],
                        help='Output format')
    
    args = parser.parse_args()
    success = create_milestone_chart(args.data, args.output, args.format)
    sys.exit(0 if success else 1)
