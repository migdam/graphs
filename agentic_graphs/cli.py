#!/usr/bin/env python3
"""
Command-line interface for the Autonomous 3D Graph System
"""

import argparse
import sys
from pathlib import Path

from .autonomous_system import AutonomousGraphSystem
from .visualizers_3d import VisualizerFactory


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Autonomous 3D Graph Generation System - Create beautiful 3D visualizations from any data source',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Automatically analyze and visualize data
  python -m agentic_graphs.cli data.csv

  # Specify output file
  python -m agentic_graphs.cli data.csv -o visualization.html

  # Force specific visualization type
  python -m agentic_graphs.cli data.json --viz-type 3d_scatter

  # Load from API
  python -m agentic_graphs.cli https://api.example.com/data --source-type api

  # Analyze data without visualization
  python -m agentic_graphs.cli data.csv --analyze-only

  # Batch process multiple files
  python -m agentic_graphs.cli data1.csv data2.json data3.xlsx --batch

  # List available visualization types
  python -m agentic_graphs.cli --list-viz
        """
    )

    parser.add_argument(
        'data_source',
        nargs='*',
        help='Data source(s) - file path, URL, or SQL query'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output file path (HTML, PNG, etc.)'
    )

    parser.add_argument(
        '--viz-type',
        type=str,
        default=None,
        choices=VisualizerFactory.available_types(),
        help='Force specific visualization type'
    )

    parser.add_argument(
        '--source-type',
        type=str,
        default=None,
        choices=['csv', 'json', 'excel', 'sql', 'api'],
        help='Explicitly specify data source type'
    )

    parser.add_argument(
        '--title',
        type=str,
        default=None,
        help='Custom title for the visualization'
    )

    parser.add_argument(
        '--no-show',
        action='store_true',
        help='Do not display the visualization (only save to file)'
    )

    parser.add_argument(
        '--analyze-only',
        action='store_true',
        help='Only analyze data without creating visualization'
    )

    parser.add_argument(
        '--batch',
        action='store_true',
        help='Process multiple data sources in batch mode'
    )

    parser.add_argument(
        '--batch-output-dir',
        type=str,
        default='examples/batch',
        help='Output directory for batch processing'
    )

    parser.add_argument(
        '--list-viz',
        action='store_true',
        help='List all available visualization types'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )

    parser.add_argument(
        '--suggest',
        action='store_true',
        help='Show visualization suggestions without generating'
    )

    # AI Analytics options
    parser.add_argument(
        '--analytics',
        action='store_true',
        help='Run AI-powered analytics on the data'
    )

    parser.add_argument(
        '--analytics-only',
        action='store_true',
        help='Only run analytics without visualization'
    )

    parser.add_argument(
        '--export-analytics',
        type=str,
        default=None,
        help='Export analytics report to JSON file'
    )

    # Additional visualizer parameters
    parser.add_argument('--x-col', type=str, help='X-axis column name')
    parser.add_argument('--y-col', type=str, help='Y-axis column name')
    parser.add_argument('--z-col', type=str, help='Z-axis column name')
    parser.add_argument('--color-col', type=str, help='Color column name')
    parser.add_argument('--size-col', type=str, help='Size column name')

    args = parser.parse_args()

    # Handle list-viz command
    if args.list_viz:
        print("\n🎨 Available 3D Visualization Types:")
        print("="*60)
        for viz_type in VisualizerFactory.available_types():
            print(f"  • {viz_type}")
        print("="*60)
        return 0

    # Validate data source
    if not args.data_source:
        parser.print_help()
        print("\n❌ Error: Please provide at least one data source")
        return 1

    # Initialize system
    verbose = not args.quiet
    system = AutonomousGraphSystem(verbose=verbose)

    try:
        # Handle batch processing
        if args.batch:
            system.batch_generate(
                args.data_source,
                output_dir=args.batch_output_dir
            )
            return 0

        # Handle single data source
        data_source = args.data_source[0]

        # Handle analyze-only mode
        if args.analyze_only:
            system.analyze(data_source, source_type=args.source_type)
            return 0

        # Handle suggest mode
        if args.suggest:
            system.suggest_visualizations(data_source, source_type=args.source_type)
            return 0

        # Handle analytics-only mode
        if args.analytics_only:
            system.run_analytics(
                data_source,
                source_type=args.source_type,
                export_path=args.export_analytics
            )
            return 0

        # Prepare visualizer kwargs
        viz_kwargs = {}
        if args.x_col:
            viz_kwargs['x_col'] = args.x_col
        if args.y_col:
            viz_kwargs['y_col'] = args.y_col
        if args.z_col:
            viz_kwargs['z_col'] = args.z_col
        if args.color_col:
            viz_kwargs['color_col'] = args.color_col
        if args.size_col:
            viz_kwargs['size_col'] = args.size_col

        # Generate visualization (with or without analytics)
        if args.analytics:
            system.generate_with_analytics(
                data_source=data_source,
                output_path=args.output,
                analytics_path=args.export_analytics,
                viz_type=args.viz_type,
                source_type=args.source_type,
                title=args.title,
                show=not args.no_show,
                **viz_kwargs
            )
        else:
            system.generate(
                data_source=data_source,
                output_path=args.output,
                viz_type=args.viz_type,
                source_type=args.source_type,
                title=args.title,
                show=not args.no_show,
                **viz_kwargs
            )

        return 0

    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        if verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
