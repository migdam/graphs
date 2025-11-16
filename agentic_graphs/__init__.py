"""
Autonomous 3D Graph Generation System

A fully autonomous system that creates beautiful 3D visualizations from any data source.

Key Features:
- Supports multiple data sources (CSV, JSON, Excel, SQL, APIs)
- Automatic data analysis and pattern detection
- Intelligent visualization selection
- Beautiful 3D graphs using Plotly
- Fully autonomous operation

Quick Start:
    >>> from agentic_graphs import auto_visualize
    >>> auto_visualize('data.csv')

Advanced Usage:
    >>> from agentic_graphs import AutonomousGraphSystem
    >>> system = AutonomousGraphSystem()
    >>> system.generate('network_data.csv', viz_type='3d_network')
"""

from .autonomous_system import (
    AutonomousGraphSystem,
    auto_visualize,
    analyze_data
)
from .agent_core import AutonomousGraphAgent, DataProfile
from .data_connectors import (
    AutoConnector,
    load_data,
    CSVConnector,
    JSONConnector,
    ExcelConnector,
    SQLConnector,
    APIConnector
)
from .visualizers_3d import VisualizerFactory
from .ai_analytics import AIGraphAnalytics, AnalyticsReport, GraphInsight

__version__ = '1.1.0'
__author__ = 'Autonomous Graph System'

__all__ = [
    # Main system
    'AutonomousGraphSystem',
    'auto_visualize',
    'analyze_data',

    # Agent core
    'AutonomousGraphAgent',
    'DataProfile',

    # Data connectors
    'AutoConnector',
    'load_data',
    'CSVConnector',
    'JSONConnector',
    'ExcelConnector',
    'SQLConnector',
    'APIConnector',

    # Visualizers
    'VisualizerFactory',

    # AI Analytics
    'AIGraphAnalytics',
    'AnalyticsReport',
    'GraphInsight',
]
