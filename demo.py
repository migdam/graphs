#!/usr/bin/env python3
"""
Quick Demo of the Autonomous 3D Graph System

This script demonstrates the autonomous capabilities of the system.
It will analyze different types of data and create appropriate visualizations.
"""

from agentic_graphs import AutonomousGraphSystem

def main():
    print("="*70)
    print("  🤖 AUTONOMOUS 3D GRAPH GENERATION SYSTEM - DEMO")
    print("="*70)
    print("\nThis demo showcases the autonomous capabilities of the system.")
    print("Watch as it analyzes different datasets and creates the best")
    print("3D visualization for each one automatically!\n")

    # Initialize the autonomous system
    system = AutonomousGraphSystem(verbose=True)

    # Demo 1: Network data
    print("\n" + "🔹"*35)
    print("DEMO 1: Network/Graph Data")
    print("🔹"*35)
    print("The system will detect this is network data and create a 3D network graph.")
    input("\nPress Enter to continue...")

    system.generate(
        'data/network_sample.csv',
        output_path='examples/demo_network.html',
        show=False
    )
    print(f"\n✓ Created: examples/demo_network.html")

    # Demo 2: 3D Scatter data
    print("\n" + "🔹"*35)
    print("DEMO 2: Multi-dimensional Numeric Data")
    print("🔹"*35)
    print("The system will detect numeric columns and create a 3D scatter plot.")
    input("\nPress Enter to continue...")

    system.generate(
        'data/3d_scatter_sample.csv',
        output_path='examples/demo_scatter.html',
        show=False
    )
    print(f"\n✓ Created: examples/demo_scatter.html")

    # Demo 3: Surface data
    print("\n" + "🔹"*35)
    print("DEMO 3: Continuous Surface Data")
    print("🔹"*35)
    print("The system will analyze the data pattern and create a 3D surface.")
    input("\nPress Enter to continue...")

    system.generate(
        'data/surface_sample.csv',
        output_path='examples/demo_surface.html',
        show=False
    )
    print(f"\n✓ Created: examples/demo_surface.html")

    # Demo 4: Get suggestions without generating
    print("\n" + "🔹"*35)
    print("DEMO 4: Getting Visualization Suggestions")
    print("🔹"*35)
    print("The system can analyze and suggest without generating...")
    input("\nPress Enter to continue...")

    suggestions = system.suggest_visualizations('data/network_sample.csv')

    # Final summary
    print("\n" + "="*70)
    print("  ✅ DEMO COMPLETE!")
    print("="*70)
    print("\nGenerated visualizations:")
    print("  • examples/demo_network.html  - 3D Network Graph")
    print("  • examples/demo_scatter.html  - 3D Scatter Plot")
    print("  • examples/demo_surface.html  - 3D Surface Plot")
    print("\nOpen these HTML files in your browser to explore the interactive 3D graphs!")
    print("\nNext steps:")
    print("  • Try: python -m agentic_graphs.cli --list-viz")
    print("  • Try: python -m agentic_graphs.cli data/network_sample.csv")
    print("  • Read: README.md for full documentation")
    print("="*70)

if __name__ == '__main__':
    main()
