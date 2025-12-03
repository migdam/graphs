#!/usr/bin/env python3
"""
Universal Chart Generator from Excel Files
Generate any chart type directly from Excel files (.xlsx, .xls).
"""

import sys
import os
import argparse
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

from excel_utils import read_excel, list_sheets
import pandas as pd


def main():
    parser = argparse.ArgumentParser(
        description='Generate charts from Excel files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument('chart_type', 
                       choices=['line', 'bar', 'scatter', 'pie', 'heatmap', 
                               'area', 'violin', 'network', 'gantt', 'milestone'],
                       help='Type of chart to generate')
    parser.add_argument('excel_file', help='Path to Excel file')
    parser.add_argument('--sheet', help='Sheet name (default: first sheet)')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--format', default='png', choices=['png', 'svg', 'pdf'],
                       help='Output format')
    parser.add_argument('--list-sheets', action='store_true',
                       help='List all sheets in the Excel file and exit')
    
    # Chart-specific options
    parser.add_argument('--x', help='X-axis column (for scatter plot)')
    parser.add_argument('--y', help='Y-axis column (for scatter plot)')
    parser.add_argument('--color', help='Color column (for scatter plot)')
    parser.add_argument('--category', help='Category column (for pie chart)')
    parser.add_argument('--value', help='Value column (for pie chart)')
    parser.add_argument('--donut', action='store_true', help='Create donut chart')
    
    args = parser.parse_args()
    
    # List sheets if requested
    if args.list_sheets:
        sheets = list_sheets(args.excel_file)
        if sheets:
            print(f"\nSheets in {args.excel_file}:")
            for i, sheet in enumerate(sheets, 1):
                print(f"  {i}. {sheet}")
        return
    
    # Read Excel file
    print(f"Reading Excel file: {args.excel_file}")
    df = read_excel(args.excel_file, sheet_name=args.sheet)
    
    if df is None:
        print("Error: Could not read Excel file")
        sys.exit(1)
    
    # Save as temporary CSV
    temp_csv = f"/tmp/temp_chart_data_{os.getpid()}.csv"
    df.to_csv(temp_csv, index=False)
    print(f"Converted to temporary CSV: {temp_csv}")
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        base_name = Path(args.excel_file).stem
        output_path = f"examples/{base_name}_{args.chart_type}.{args.format}"
    
    # Import and call appropriate chart script
    chart_modules = {
        'line': 'line_chart',
        'bar': 'bar_chart',
        'scatter': 'scatter_plot',
        'pie': 'pie_chart',
        'heatmap': 'heatmap',
        'area': 'area_chart',
        'violin': 'violin_plot',
        'network': 'network_graph',
        'gantt': 'gantt_chart',
        'milestone': 'milestone_chart'
    }
    
    module_name = chart_modules[args.chart_type]
    
    try:
        # Build command to run the chart script
        cmd_parts = [
            'python3',
            f'scripts/{module_name}.py',
            '--data', temp_csv,
            '--output', output_path,
            '--format', args.format
        ]
        
        # Add chart-specific arguments
        if args.chart_type == 'scatter':
            if args.x:
                cmd_parts.extend(['--x', args.x])
            if args.y:
                cmd_parts.extend(['--y', args.y])
            if args.color:
                cmd_parts.extend(['--color', args.color])
        elif args.chart_type == 'pie':
            if args.category:
                cmd_parts.extend(['--category', args.category])
            if args.value:
                cmd_parts.extend(['--value', args.value])
            if args.donut:
                cmd_parts.append('--donut')
        
        # Execute the chart generation
        import subprocess
        result = subprocess.run(cmd_parts, capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        if result.returncode == 0:
            print(f"\n✅ Chart saved to: {output_path}")
        else:
            print(f"\n❌ Error generating chart (exit code: {result.returncode})")
        
        # Clean up temporary file
        if os.path.exists(temp_csv):
            os.remove(temp_csv)
        
        sys.exit(result.returncode)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        # Clean up temporary file
        if os.path.exists(temp_csv):
            os.remove(temp_csv)
        sys.exit(1)


if __name__ == "__main__":
    main()
