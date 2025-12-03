#!/usr/bin/env python3
"""
Examples of Embedding Charts in Excel Files
"""

import sys
import os
sys.path.insert(0, '../scripts')

from embed_in_excel import (
    embed_chart_in_excel,
    embed_multiple_charts,
    create_report_with_charts
)
import pandas as pd


# Example 1: Embed a single chart
def example_single_chart():
    """Embed one chart into an existing Excel file."""
    print("Example 1: Embedding single chart...")
    
    embed_chart_in_excel(
        excel_path='../data/sample_data.xlsx',
        output_path='report_with_single_chart.xlsx',
        sheet_name='Sales',
        chart_type='line',
        position='H2'
    )
    print("✓ Created: report_with_single_chart.xlsx\n")


# Example 2: Embed multiple charts in same file
def example_multiple_charts():
    """Embed multiple charts into different positions."""
    print("Example 2: Embedding multiple charts...")
    
    charts_config = [
        {'sheet': 'Sales', 'chart_type': 'line', 'position': 'H2'},
        {'sheet': 'Sales', 'chart_type': 'bar', 'position': 'H20'},
        {'sheet': 'Costs', 'chart_type': 'pie', 'position': 'H2'},
    ]
    
    embed_multiple_charts(
        excel_path='../data/sample_data.xlsx',
        output_path='report_with_multiple_charts.xlsx',
        charts_config=charts_config
    )
    print("✓ Created: report_with_multiple_charts.xlsx\n")


# Example 3: Create new report with data and charts
def example_create_report():
    """Create a complete report from scratch with data and charts."""
    print("Example 3: Creating complete report...")
    
    # Prepare data
    sales_df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=6, freq='M'),
        'category': ['A', 'A', 'A', 'B', 'B', 'B'],
        'value': [100, 120, 115, 150, 165, 170]
    })
    
    costs_df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=6, freq='M'),
        'category': ['A', 'A', 'A', 'B', 'B', 'B'],
        'value': [60, 70, 65, 85, 90, 95]
    })
    
    data_dict = {
        'Sales': sales_df,
        'Costs': costs_df
    }
    
    chart_positions = {
        'Sales': {'chart_type': 'line', 'position': 'F2'},
        'Costs': {'chart_type': 'bar', 'position': 'F2'}
    }
    
    create_report_with_charts(
        data_dict=data_dict,
        output_path='complete_report.xlsx',
        chart_positions=chart_positions
    )
    print("✓ Created: complete_report.xlsx\n")


# Example 4: Embed chart at specific position
def example_custom_position():
    """Embed chart at a custom cell position."""
    print("Example 4: Custom chart position...")
    
    embed_chart_in_excel(
        excel_path='../data/quarterly_report.xlsx',
        output_path='report_custom_position.xlsx',
        sheet_name='Q1',
        chart_type='bar',
        position='M5'  # Column M, Row 5
    )
    print("✓ Created: report_custom_position.xlsx\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Excel Chart Embedding Examples")
    print("=" * 60 + "\n")
    
    # Run all examples
    example_single_chart()
    example_multiple_charts()
    example_create_report()
    example_custom_position()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
