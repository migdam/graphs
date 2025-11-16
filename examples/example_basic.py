#!/usr/bin/env python3
"""
Basic Example: Autonomous 3D Graph Generation

This example shows the simplest way to use the autonomous system.
Just provide a data source and let the system do the rest!
"""

from agentic_graphs import auto_visualize

# Example 1: Automatically visualize network data
print("Example 1: Network Data")
print("="*60)
auto_visualize('data/network_sample.csv')

# Example 2: Automatically visualize 3D scatter data
print("\n\nExample 2: 3D Scatter Data")
print("="*60)
auto_visualize('data/3d_scatter_sample.csv')

# Example 3: Automatically visualize surface data
print("\n\nExample 3: Surface Data")
print("="*60)
auto_visualize('data/surface_sample.csv')

# Example 4: Save to file instead of showing
print("\n\nExample 4: Save to File")
print("="*60)
auto_visualize(
    'data/network_sample.csv',
    output_path='examples/network_viz.html',
    show=False
)
print("Saved to: examples/network_viz.html")
