"""
Autonomous 3D Graph Generation System
Main orchestrator that autonomously creates beautiful 3D visualizations
"""

import pandas as pd
from typing import Optional, Any, Dict, Tuple
from pathlib import Path

from .agent_core import AutonomousGraphAgent, DataProfile
from .data_connectors import AutoConnector, load_data
from .visualizers_3d import VisualizerFactory
from .ai_analytics import AIGraphAnalytics, AnalyticsReport
import plotly.graph_objects as go


class AutonomousGraphSystem:
    """
    Fully autonomous system for creating beautiful 3D graphs.

    This system:
    1. Accepts data from any source (CSV, JSON, API, SQL, etc.)
    2. Automatically analyzes the data structure and content
    3. Intelligently selects the best 3D visualization
    4. Generates beautiful, interactive 3D graphs
    5. Saves outputs in various formats

    Example:
        >>> system = AutonomousGraphSystem()
        >>> system.generate('data.csv', output='visualization.html')
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize the autonomous system.

        Args:
            verbose: Print detailed progress information
        """
        self.verbose = verbose
        self.agent = AutonomousGraphAgent(verbose=verbose)
        self.data_connector = AutoConnector(verbose=verbose)
        self.analytics = AIGraphAnalytics(verbose=verbose)

        if self.verbose:
            print("🤖 Autonomous 3D Graph System Initialized")
            print("  ✓ Decision Agent")
            print("  ✓ Data Connectors")
            print("  ✓ AI Analytics Engine")
            print("="*60)

    def generate(
        self,
        data_source: Any,
        output_path: Optional[str] = None,
        viz_type: Optional[str] = None,
        source_type: Optional[str] = None,
        title: Optional[str] = None,
        show: bool = True,
        **kwargs
    ) -> go.Figure:
        """
        Autonomously generate a 3D visualization from any data source.

        Args:
            data_source: Data source (file path, URL, DataFrame, SQL query, etc.)
            output_path: Where to save the visualization (HTML, PNG, etc.)
            viz_type: Optional visualization type override (e.g., '3d_scatter', '3d_network')
            source_type: Optional data source type override (e.g., 'csv', 'json', 'api')
            title: Optional custom title for the visualization
            show: Whether to display the visualization
            **kwargs: Additional parameters (visualizer params like x_col, y_col, or data loader params)

        Returns:
            Plotly Figure object
        """
        if self.verbose:
            print("\n🚀 Starting Autonomous Graph Generation")
            print("="*60)

        # Separate visualizer kwargs from data loading kwargs
        visualizer_params = {
            'x_col', 'y_col', 'z_col', 'color_col', 'size_col',
            'source_col', 'target_col', 'weight_col', 'node_color_col',
            'layout', 'colorscale'
        }
        viz_kwargs = {k: v for k, v in kwargs.items() if k in visualizer_params}
        data_kwargs = {k: v for k, v in kwargs.items() if k not in visualizer_params}

        # Step 1: Load data from any source
        if self.verbose:
            print("\n📥 Step 1: Loading Data")
            print("-"*60)

        df = self.data_connector.load(data_source, source_type=source_type, **data_kwargs)

        # Step 2: Analyze data and decide on visualization
        if self.verbose:
            print("\n🧠 Step 2: Analyzing Data & Making Decisions")
            print("-"*60)

        selected_viz, profile = self.agent.decide_visualization(df, preference=viz_type)

        # Step 3: Generate visualization
        if self.verbose:
            print(f"\n🎨 Step 3: Generating {selected_viz.upper()} Visualization")
            print("-"*60)

        visualizer = VisualizerFactory.create(selected_viz, verbose=self.verbose)

        # Auto-generate output path if not provided
        if output_path is None:
            output_dir = Path('examples')
            output_dir.mkdir(exist_ok=True)
            output_path = str(output_dir / f'autonomous_{selected_viz}.html')

        # Create the visualization
        fig = visualizer.create(
            df=df,
            output_path=output_path,
            title=title,
            **viz_kwargs
        )

        # Step 4: Display if requested
        if show:
            if self.verbose:
                print("\n👁️ Displaying visualization...")
            fig.show()

        if self.verbose:
            print("\n" + "="*60)
            print("✅ Autonomous Generation Complete!")
            print("="*60)

        return fig

    def analyze(self, data_source: Any, source_type: Optional[str] = None, **kwargs) -> DataProfile:
        """
        Analyze data without generating a visualization.

        Args:
            data_source: Data source to analyze
            source_type: Optional data source type override

        Returns:
            DataProfile with analysis results
        """
        df = self.data_connector.load(data_source, source_type=source_type, **kwargs)
        return self.agent.analyze_data(df)

    def batch_generate(
        self,
        data_sources: list,
        output_dir: str = 'examples/batch',
        **kwargs
    ) -> Dict[str, go.Figure]:
        """
        Generate visualizations for multiple data sources autonomously.

        Args:
            data_sources: List of data sources
            output_dir: Directory to save all visualizations
            **kwargs: Additional parameters

        Returns:
            Dictionary mapping source names to Figure objects
        """
        if self.verbose:
            print(f"\n🚀 Batch Processing {len(data_sources)} Data Sources")
            print("="*60)

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = {}

        for i, source in enumerate(data_sources, 1):
            if self.verbose:
                print(f"\n📊 Processing {i}/{len(data_sources)}: {source}")
                print("-"*60)

            try:
                # Generate filename from source
                if isinstance(source, str):
                    name = Path(source).stem
                else:
                    name = f"dataset_{i}"

                output_file = output_path / f"{name}_visualization.html"

                fig = self.generate(
                    source,
                    output_path=str(output_file),
                    show=False,
                    **kwargs
                )

                results[name] = fig

                if self.verbose:
                    print(f"✓ Completed: {name}")

            except Exception as e:
                if self.verbose:
                    print(f"✗ Failed: {source} - {str(e)}")
                results[source] = None

        if self.verbose:
            print("\n" + "="*60)
            print(f"✅ Batch Processing Complete: {len([r for r in results.values() if r is not None])}/{len(data_sources)} successful")
            print("="*60)

        return results

    def suggest_visualizations(self, data_source: Any, source_type: Optional[str] = None) -> list:
        """
        Get visualization suggestions without generating them.

        Args:
            data_source: Data source to analyze
            source_type: Optional data source type override

        Returns:
            List of suggested visualization types with confidence scores
        """
        df = self.data_connector.load(data_source, source_type=source_type)
        profile = self.agent.analyze_data(df)

        suggestions = [(viz, profile.confidence_scores[viz]) for viz in profile.suggested_visualizations]

        if self.verbose:
            print("\n💡 Visualization Suggestions:")
            print("="*60)
            for viz, confidence in suggestions:
                print(f"  • {viz.upper()}: {confidence:.1%} confidence")
            print("="*60)

        return suggestions

    def available_visualizations(self) -> list:
        """Get list of all available 3D visualization types"""
        return VisualizerFactory.available_types()

    def run_analytics(
        self,
        data_source: Any,
        viz_type: Optional[str] = None,
        source_type: Optional[str] = None,
        export_path: Optional[str] = None,
        **kwargs
    ) -> AnalyticsReport:
        """
        Run AI-powered analytics on data.

        Args:
            data_source: Data source to analyze
            viz_type: Optional visualization type (for context)
            source_type: Optional data source type override
            export_path: Optional path to export JSON report
            **kwargs: Additional parameters

        Returns:
            AnalyticsReport with comprehensive insights

        Example:
            >>> system = AutonomousGraphSystem()
            >>> report = system.run_analytics('data.csv')
            >>> print(report.natural_language_summary)
        """
        # Load data
        df = self.data_connector.load(data_source, source_type=source_type, **kwargs)

        # Determine viz type if not specified
        if viz_type is None:
            profile = self.agent.analyze_data(df)
            viz_type = profile.suggested_visualizations[0]
        else:
            profile = None

        # Run analytics
        report = self.analytics.analyze(df, viz_type, profile)

        # Export if requested
        if export_path:
            self.analytics.export_report(report, export_path)

        return report

    def generate_with_analytics(
        self,
        data_source: Any,
        output_path: Optional[str] = None,
        analytics_path: Optional[str] = None,
        viz_type: Optional[str] = None,
        source_type: Optional[str] = None,
        title: Optional[str] = None,
        show: bool = True,
        **kwargs
    ) -> Tuple[go.Figure, AnalyticsReport]:
        """
        Generate visualization AND run AI analytics in one step.

        Args:
            data_source: Data source
            output_path: Where to save visualization
            analytics_path: Where to save analytics report (JSON)
            viz_type: Optional visualization type
            source_type: Optional data source type
            title: Optional title
            show: Whether to display
            **kwargs: Additional parameters

        Returns:
            Tuple of (Figure, AnalyticsReport)

        Example:
            >>> system = AutonomousGraphSystem()
            >>> fig, report = system.generate_with_analytics('data.csv')
            >>> print(report.key_findings)
        """
        if self.verbose:
            print("\n🚀 Starting Autonomous Generation with AI Analytics")
            print("="*60)

        # Separate visualizer kwargs from data loading kwargs
        visualizer_params = {
            'x_col', 'y_col', 'z_col', 'color_col', 'size_col',
            'source_col', 'target_col', 'weight_col', 'node_color_col',
            'layout', 'colorscale'
        }
        viz_kwargs = {k: v for k, v in kwargs.items() if k in visualizer_params}
        data_kwargs = {k: v for k, v in kwargs.items() if k not in visualizer_params}

        # Load data
        if self.verbose:
            print("\n📥 Step 1: Loading Data")
            print("-"*60)

        df = self.data_connector.load(data_source, source_type=source_type, **data_kwargs)

        # Analyze data and decide on visualization
        if self.verbose:
            print("\n🧠 Step 2: Analyzing Data & Making Decisions")
            print("-"*60)

        selected_viz, profile = self.agent.decide_visualization(df, preference=viz_type)

        # Run AI analytics
        if self.verbose:
            print(f"\n🤖 Step 3: Running AI Analytics")
            print("-"*60)

        report = self.analytics.analyze(df, selected_viz, profile)

        # Generate visualization
        if self.verbose:
            print(f"\n🎨 Step 4: Generating {selected_viz.upper()} Visualization")
            print("-"*60)

        visualizer = VisualizerFactory.create(selected_viz, verbose=self.verbose)

        if output_path is None:
            output_dir = Path('examples')
            output_dir.mkdir(exist_ok=True)
            output_path = str(output_dir / f'autonomous_{selected_viz}.html')

        fig = visualizer.create(
            df=df,
            output_path=output_path,
            title=title,
            **viz_kwargs
        )

        # Export analytics if requested
        if analytics_path:
            self.analytics.export_report(report, analytics_path)
        elif output_path:
            # Auto-export analytics next to visualization
            analytics_auto_path = Path(output_path).with_suffix('.analytics.json')
            self.analytics.export_report(report, str(analytics_auto_path))

        # Display if requested
        if show:
            if self.verbose:
                print("\n👁️ Displaying visualization...")
            fig.show()

        if self.verbose:
            print("\n" + "="*60)
            print("✅ Autonomous Generation with Analytics Complete!")
            print("="*60)

        return fig, report


# Convenience functions for quick usage
def auto_visualize(
    data_source: Any,
    output_path: Optional[str] = None,
    verbose: bool = True,
    **kwargs
) -> go.Figure:
    """
    Quick function to autonomously visualize any data source.

    Args:
        data_source: Any data source (file, URL, DataFrame, etc.)
        output_path: Optional output path
        verbose: Print progress
        **kwargs: Additional parameters

    Returns:
        Plotly Figure

    Example:
        >>> auto_visualize('network_data.csv')
        >>> auto_visualize('https://api.example.com/data', viz_type='3d_scatter')
    """
    system = AutonomousGraphSystem(verbose=verbose)
    return system.generate(data_source, output_path=output_path, **kwargs)


def analyze_data(data_source: Any, verbose: bool = True) -> DataProfile:
    """
    Quick function to analyze data without visualization.

    Args:
        data_source: Any data source
        verbose: Print analysis

    Returns:
        DataProfile

    Example:
        >>> profile = analyze_data('mydata.csv')
    """
    system = AutonomousGraphSystem(verbose=verbose)
    return system.analyze(data_source)
