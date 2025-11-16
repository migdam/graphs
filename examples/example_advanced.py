#!/usr/bin/env python3
"""
Advanced Example: Full Control Over the Autonomous System

This example demonstrates advanced features:
- Analyzing data before visualization
- Controlling visualization types
- Batch processing
- Custom parameters
"""

from agentic_graphs import AutonomousGraphSystem, analyze_data

# Initialize the system
system = AutonomousGraphSystem(verbose=True)

# Example 1: Analyze data before visualizing
print("="*60)
print("Example 1: Data Analysis")
print("="*60)
profile = analyze_data('data/3d_scatter_sample.csv')
print(f"\nData has {profile.num_rows} rows and {profile.num_columns} columns")
print(f"Suggested visualizations: {profile.suggested_visualizations}")

# Example 2: Get visualization suggestions
print("\n\n" + "="*60)
print("Example 2: Visualization Suggestions")
print("="*60)
suggestions = system.suggest_visualizations('data/network_sample.csv')

# Example 3: Force a specific visualization type
print("\n\n" + "="*60)
print("Example 3: Force Specific Visualization")
print("="*60)
system.generate(
    'data/3d_scatter_sample.csv',
    viz_type='3d_scatter',
    output_path='examples/forced_scatter.html',
    title='Custom 3D Scatter Plot',
    show=False
)

# Example 4: Custom column selection
print("\n\n" + "="*60)
print("Example 4: Custom Column Selection")
print("="*60)
system.generate(
    'data/3d_scatter_sample.csv',
    viz_type='3d_scatter',
    x_col='x',
    y_col='y',
    z_col='z',
    color_col='category',
    size_col='value',
    output_path='examples/custom_scatter.html',
    title='Customized Scatter Plot',
    show=False
)

# Example 5: Batch processing multiple files
print("\n\n" + "="*60)
print("Example 5: Batch Processing")
print("="*60)
results = system.batch_generate([
    'data/network_sample.csv',
    'data/3d_scatter_sample.csv',
    'data/surface_sample.csv'
], output_dir='examples/batch_output')

print(f"\nGenerated {len(results)} visualizations")

# Example 6: Working with different data sources
print("\n\n" + "="*60)
print("Example 6: Different Data Sources")
print("="*60)

# From JSON string
import json
json_data = {
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 6, 8, 10],
    'z': [1, 4, 9, 16, 25],
    'category': ['A', 'B', 'A', 'B', 'A']
}
system.generate(
    json.dumps(json_data),
    source_type='json',
    output_path='examples/from_json.html',
    show=False
)

# From DataFrame
import pandas as pd
df = pd.DataFrame({
    'x': range(10),
    'y': range(10, 20),
    'z': [i**2 for i in range(10)]
})
system.generate(
    df,
    output_path='examples/from_dataframe.html',
    show=False
)

print("\n" + "="*60)
print("All examples completed!")
print("="*60)
