#!/usr/bin/env python3

import argparse
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

# Import all visualization functions
from line_chart import create_line_chart
from bar_chart import create_bar_chart
from heatmap import create_heatmap
from scatter_plot import create_scatter_plot
from pie_chart import create_pie_chart
from area_chart import create_area_chart
from box_plot import create_box_plot
from violin_plot import create_violin_plot
from histogram import create_histogram
from bubble_chart import create_bubble_chart
from radar_chart import create_radar_chart
from surface_3d import create_3d_surface

CHART_TYPES = {
    'line': create_line_chart,
    'bar': create_bar_chart,
    'heatmap': create_heatmap,
    'scatter': create_scatter_plot,
    'pie': create_pie_chart,
    'area': create_area_chart,
    'box': create_box_plot,
    'violin': create_violin_plot,
    'histogram': create_histogram,
    'bubble': create_bubble_chart,
    'radar': create_radar_chart,
    '3d': create_3d_surface
}

def main():
    parser = argparse.ArgumentParser(
        description='Generate various types of data visualizations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Available chart types:
  {', '.join(CHART_TYPES.keys())}

Examples:
  python visualize.py --type line --data data/sample_data.csv
  python visualize.py --type bar --data data/sample_data.csv --output examples/my_bar.png
  python visualize.py --all --data data/sample_data.csv
        """
    )
    
    parser.add_argument('--type', type=str, choices=list(CHART_TYPES.keys()),
                        help='Type of chart to generate')
    parser.add_argument('--data', type=str, default='data/sample_data.csv',
                        help='Path to the CSV data file')
    parser.add_argument('--output', type=str,
                        help='Path to save the output image (default: examples/<type>.png)')
    parser.add_argument('--all', action='store_true',
                        help='Generate all chart types')
    
    args = parser.parse_args()
    
    if not args.type and not args.all:
        parser.error('Either --type or --all must be specified')
    
    if args.all:
        print("Generating all chart types...")
        for chart_type, chart_func in CHART_TYPES.items():
            output_path = f'examples/{chart_type}_chart.png'
            try:
                print(f"\nGenerating {chart_type} chart...")
                chart_func(args.data, output_path)
            except Exception as e:
                print(f"Error generating {chart_type} chart: {e}")
        print("\nAll charts generated successfully!")
    else:
        output_path = args.output or f'examples/{args.type}_chart.png'
        try:
            print(f"Generating {args.type} chart...")
            CHART_TYPES[args.type](args.data, output_path)
            print(f"\nChart generated successfully at {output_path}")
        except Exception as e:
            print(f"Error generating chart: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
