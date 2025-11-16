#!/usr/bin/env python3
"""
SHOWCASE: Autonomous 3D Graph Generation System
Demonstrates all key features with beautiful examples
"""

from agentic_graphs import AutonomousGraphSystem, auto_visualize, analyze_data
import pandas as pd
import numpy as np


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def showcase_1_simple_auto():
    """Showcase 1: Simplest usage - one line of code"""
    print_section("SHOWCASE 1: Simplest Usage - One Line Magic")

    print("Code:")
    print("  from agentic_graphs import auto_visualize")
    print("  auto_visualize('data/network_sample.csv')")
    print("\nResult: Automatically analyzes and visualizes network data!\n")

    auto_visualize(
        'data/network_sample.csv',
        output_path='examples/showcase_1_simple.html',
        show=False
    )

    print("✓ Created: examples/showcase_1_simple.html")


def showcase_2_autonomous_analysis():
    """Showcase 2: Autonomous data analysis"""
    print_section("SHOWCASE 2: Autonomous Data Analysis")

    print("The system analyzes your data and makes intelligent decisions:")
    print()

    # Analyze different datasets
    datasets = [
        ('data/network_sample.csv', 'Network Data'),
        ('data/3d_scatter_sample.csv', 'Multi-dimensional Data'),
        ('data/surface_sample.csv', 'Surface Data')
    ]

    for path, name in datasets:
        profile = analyze_data(path, verbose=False)
        print(f"📊 {name}:")
        print(f"   Shape: {profile.num_rows} rows × {profile.num_columns} cols")
        print(f"   Network: {'✓' if profile.has_network_structure else '✗'}")
        print(f"   Temporal: {'✓' if profile.has_temporal else '✗'}")
        print(f"   Recommended: {profile.suggested_visualizations[0]}")
        print(f"   Confidence: {profile.confidence_scores[profile.suggested_visualizations[0]]:.0%}")
        print()


def showcase_3_all_visualizations():
    """Showcase 3: All 5 visualization types"""
    print_section("SHOWCASE 3: All 5 Beautiful 3D Visualization Types")

    system = AutonomousGraphSystem(verbose=False)

    visualizations = [
        ('data/network_sample.csv', '3d_network', 'Network Graph'),
        ('data/3d_scatter_sample.csv', '3d_scatter', 'Scatter Plot'),
        ('data/surface_sample.csv', '3d_surface', 'Surface Plot'),
    ]

    # Create temporal data for line plot
    df_line = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=30),
        'x': np.cumsum(np.random.randn(30)),
        'y': np.cumsum(np.random.randn(30)),
        'z': np.cumsum(np.random.randn(30))
    })
    df_line.to_csv('/tmp/line_data.csv', index=False)
    visualizations.append(('/tmp/line_data.csv', '3d_line', 'Line Plot'))

    # Create categorical data for bar chart
    df_bar = pd.DataFrame({
        'category': np.random.choice(['A', 'B', 'C'], 20),
        'group': np.random.choice(['X', 'Y'], 20),
        'value': np.random.randint(10, 100, 20)
    })
    df_bar.to_csv('/tmp/bar_data.csv', index=False)
    visualizations.append(('/tmp/bar_data.csv', '3d_bar', 'Bar Chart'))

    for i, (data, viz_type, name) in enumerate(visualizations, 1):
        print(f"{i}. Creating {name} ({viz_type})...", end=' ')
        system.generate(
            data,
            viz_type=viz_type,
            output_path=f'examples/showcase_3_{viz_type}.html',
            show=False
        )
        print("✓")

    print("\n✓ All 5 visualization types created successfully!")


def showcase_4_multi_source():
    """Showcase 4: Multiple data sources"""
    print_section("SHOWCASE 4: Multiple Data Source Support")

    system = AutonomousGraphSystem(verbose=False)

    print("The system can load data from:")
    print()

    # 1. CSV file
    print("1. CSV File...", end=' ')
    system.generate(
        'data/network_sample.csv',
        output_path='examples/showcase_4_csv.html',
        show=False
    )
    print("✓")

    # 2. JSON
    import json
    json_data = {
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 6, 8, 10],
        'z': [1, 4, 9, 16, 25]
    }
    print("2. JSON Data...", end=' ')
    system.generate(
        json.dumps(json_data),
        source_type='json',
        output_path='examples/showcase_4_json.html',
        show=False
    )
    print("✓")

    # 3. DataFrame
    print("3. Pandas DataFrame...", end=' ')
    df = pd.DataFrame({
        'x': np.random.randn(50),
        'y': np.random.randn(50),
        'z': np.random.randn(50),
        'category': np.random.choice(['A', 'B', 'C'], 50)
    })
    system.generate(
        df,
        output_path='examples/showcase_4_dataframe.html',
        show=False
    )
    print("✓")

    print("\n✓ Multiple data sources demonstrated!")


def showcase_5_custom_control():
    """Showcase 5: Custom control and parameters"""
    print_section("SHOWCASE 5: Custom Control & Parameters")

    system = AutonomousGraphSystem(verbose=False)

    print("You can override autonomous decisions and customize everything:")
    print()

    # Custom visualization with specific parameters
    print("Creating custom 3D scatter with specific columns and colors...", end=' ')
    system.generate(
        'data/3d_scatter_sample.csv',
        viz_type='3d_scatter',
        x_col='x',
        y_col='y',
        z_col='value',
        color_col='category',
        size_col='z',
        title='Custom 3D Scatter - Fully Controlled',
        output_path='examples/showcase_5_custom.html',
        show=False
    )
    print("✓")

    print("\n✓ Custom parameters applied successfully!")


def showcase_6_batch_processing():
    """Showcase 6: Batch processing"""
    print_section("SHOWCASE 6: Batch Processing")

    system = AutonomousGraphSystem(verbose=False)

    print("Process multiple datasets automatically:")
    print()

    results = system.batch_generate(
        [
            'data/network_sample.csv',
            'data/3d_scatter_sample.csv',
            'data/surface_sample.csv'
        ],
        output_dir='examples/showcase_6_batch'
    )

    print(f"\n✓ Batch processed {len(results)} datasets!")
    print(f"✓ All outputs in: examples/showcase_6_batch/")


def showcase_7_intelligence():
    """Showcase 7: Intelligence features"""
    print_section("SHOWCASE 7: Intelligent Features")

    print("The system is intelligent and detects:")
    print()

    # Create correlated data
    n = 100
    x = np.arange(n)
    df = pd.DataFrame({
        'time': x,
        'temperature': 20 + x * 0.1 + np.random.randn(n),  # Strong correlation with time
        'humidity': 60 - x * 0.05 + np.random.randn(n),    # Negative correlation
        'pressure': 1013 + np.random.randn(n) * 2          # No correlation
    })
    df.to_csv('/tmp/sensor_data.csv', index=False)

    profile = analyze_data('/tmp/sensor_data.csv', verbose=False)

    print("✓ Column types (numeric, categorical, temporal)")
    print(f"✓ Correlations ({len(profile.relationships)} detected)")
    print("✓ Network structures")
    print("✓ Optimal visualization approach")
    print()

    if profile.relationships:
        print("Detected relationships:")
        for col1, col2, rel_type in profile.relationships[:3]:
            print(f"  • {col1} ↔ {col2}: {rel_type}")


def main():
    """Run all showcases"""
    print("="*70)
    print("  🤖 AUTONOMOUS 3D GRAPH GENERATION SYSTEM")
    print("  COMPREHENSIVE FEATURE SHOWCASE")
    print("="*70)
    print("\nThis showcase demonstrates all major features of the system.")
    print("Generated visualizations will be saved to the examples/ directory.")
    print()
    input("Press Enter to begin the showcase...")

    try:
        showcase_1_simple_auto()
        input("\nPress Enter for next showcase...")

        showcase_2_autonomous_analysis()
        input("\nPress Enter for next showcase...")

        showcase_3_all_visualizations()
        input("\nPress Enter for next showcase...")

        showcase_4_multi_source()
        input("\nPress Enter for next showcase...")

        showcase_5_custom_control()
        input("\nPress Enter for next showcase...")

        showcase_6_batch_processing()
        input("\nPress Enter for next showcase...")

        showcase_7_intelligence()

        # Final summary
        print_section("SHOWCASE COMPLETE! 🎉")

        print("All features demonstrated successfully!")
        print()
        print("Generated visualizations:")
        from pathlib import Path
        showcase_files = sorted(Path('examples').glob('showcase*.html'))
        for f in showcase_files[:10]:  # Show first 10
            print(f"  ✓ {f}")

        if len(showcase_files) > 10:
            print(f"  ... and {len(showcase_files) - 10} more files")

        print()
        print("Next steps:")
        print("  • Open any HTML file in your browser")
        print("  • Try: python -m agentic_graphs.cli --help")
        print("  • Read: README.md for full documentation")
        print()
        print("="*70)
        print("  Thank you for exploring the Autonomous 3D Graph System!")
        print("="*70)

    except KeyboardInterrupt:
        print("\n\nShowcase interrupted. Generated files are still available!")


if __name__ == '__main__':
    main()
