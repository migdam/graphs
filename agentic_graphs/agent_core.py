"""
Autonomous Agent Core for 3D Graph Generation
This module contains the main agent that analyzes data and autonomously
decides on the best 3D visualization strategy.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import json


@dataclass
class DataProfile:
    """Profile of analyzed data with key characteristics"""
    num_rows: int
    num_columns: int
    column_names: List[str]
    column_types: Dict[str, str]
    has_temporal: bool
    has_categorical: bool
    has_numeric: bool
    has_network_structure: bool
    relationships: List[Tuple[str, str, str]]  # (col1, col2, relationship_type)
    statistical_summary: Dict[str, Any]
    suggested_visualizations: List[str]
    confidence_scores: Dict[str, float]


class AutonomousGraphAgent:
    """
    Autonomous agent that analyzes data and determines the best 3D visualization approach.
    Uses heuristics and data analysis to make intelligent decisions without human intervention.
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.visualization_rules = self._initialize_rules()

    def _initialize_rules(self) -> Dict[str, Any]:
        """Initialize decision rules for visualization selection"""
        return {
            'network_indicators': ['source', 'target', 'from', 'to', 'node', 'edge'],
            'temporal_indicators': ['date', 'time', 'timestamp', 'year', 'month', 'day'],
            'spatial_indicators': ['x', 'y', 'z', 'lat', 'lon', 'latitude', 'longitude'],
            'min_network_cols': 2,
            'min_3d_scatter_cols': 3,
            'max_categories_for_discrete': 20,
            'min_rows_for_surface': 10,
        }

    def analyze_data(self, df: pd.DataFrame) -> DataProfile:
        """
        Comprehensively analyze the dataset and create a data profile.
        This is the core intelligence of the agent.
        """
        if self.verbose:
            print(f"🔍 Analyzing dataset: {df.shape[0]} rows × {df.shape[1]} columns")

        # Basic structure
        num_rows, num_columns = df.shape
        column_names = df.columns.tolist()

        # Identify column types
        column_types = {}
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                column_types[col] = 'numeric'
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                column_types[col] = 'temporal'
            elif pd.api.types.is_categorical_dtype(df[col]) or df[col].dtype == 'object':
                column_types[col] = 'categorical'
            else:
                column_types[col] = 'unknown'

        # Check for specific patterns
        has_temporal = self._detect_temporal(df, column_types)
        has_categorical = 'categorical' in column_types.values()
        has_numeric = 'numeric' in column_types.values()
        has_network_structure = self._detect_network_structure(df, column_names)

        # Analyze relationships between columns
        relationships = self._analyze_relationships(df, column_types)

        # Statistical summary
        statistical_summary = self._compute_statistics(df, column_types)

        # Suggest visualizations based on analysis
        suggestions = self._suggest_visualizations(
            df, column_types, has_temporal, has_categorical,
            has_numeric, has_network_structure, relationships
        )

        profile = DataProfile(
            num_rows=num_rows,
            num_columns=num_columns,
            column_names=column_names,
            column_types=column_types,
            has_temporal=has_temporal,
            has_categorical=has_categorical,
            has_numeric=has_numeric,
            has_network_structure=has_network_structure,
            relationships=relationships,
            statistical_summary=statistical_summary,
            suggested_visualizations=[s[0] for s in suggestions],
            confidence_scores={s[0]: s[1] for s in suggestions}
        )

        if self.verbose:
            self._print_profile(profile)

        return profile

    def _detect_temporal(self, df: pd.DataFrame, column_types: Dict[str, str]) -> bool:
        """Detect if data has temporal components"""
        # Check explicit temporal types
        if 'temporal' in column_types.values():
            return True

        # Check column names for temporal indicators
        temporal_keywords = self.visualization_rules['temporal_indicators']
        for col in df.columns:
            if any(keyword in col.lower() for keyword in temporal_keywords):
                return True

        return False

    def _detect_network_structure(self, df: pd.DataFrame, column_names: List[str]) -> bool:
        """Detect if data represents a network/graph structure"""
        network_keywords = self.visualization_rules['network_indicators']

        # Check for source-target pairs
        lower_cols = [col.lower() for col in column_names]
        has_source = any(kw in col for col in lower_cols for kw in ['source', 'from', 'node1'])
        has_target = any(kw in col for col in lower_cols for kw in ['target', 'to', 'node2'])

        if has_source and has_target:
            return True

        # Check if we have node and edge related columns
        has_node = any('node' in col for col in lower_cols)
        has_edge = any('edge' in col for col in lower_cols)

        return has_node and has_edge

    def _analyze_relationships(self, df: pd.DataFrame, column_types: Dict[str, str]) -> List[Tuple[str, str, str]]:
        """Analyze relationships between columns"""
        relationships = []

        # Find correlations between numeric columns
        numeric_cols = [col for col, dtype in column_types.items() if dtype == 'numeric']
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr()
            for i, col1 in enumerate(numeric_cols):
                for col2 in numeric_cols[i+1:]:
                    corr_value = corr_matrix.loc[col1, col2]
                    if abs(corr_value) > 0.7:
                        rel_type = 'strong_correlation' if corr_value > 0 else 'strong_negative_correlation'
                        relationships.append((col1, col2, rel_type))
                    elif abs(corr_value) > 0.4:
                        rel_type = 'moderate_correlation' if corr_value > 0 else 'moderate_negative_correlation'
                        relationships.append((col1, col2, rel_type))

        return relationships

    def _compute_statistics(self, df: pd.DataFrame, column_types: Dict[str, str]) -> Dict[str, Any]:
        """Compute statistical summary of the data"""
        stats = {
            'numeric_stats': {},
            'categorical_stats': {},
            'missing_values': df.isnull().sum().to_dict()
        }

        # Numeric statistics
        numeric_cols = [col for col, dtype in column_types.items() if dtype == 'numeric']
        for col in numeric_cols:
            stats['numeric_stats'][col] = {
                'mean': float(df[col].mean()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'median': float(df[col].median())
            }

        # Categorical statistics
        categorical_cols = [col for col, dtype in column_types.items() if dtype == 'categorical']
        for col in categorical_cols:
            unique_values = df[col].nunique()
            stats['categorical_stats'][col] = {
                'unique_values': int(unique_values),
                'most_common': df[col].mode()[0] if len(df[col].mode()) > 0 else None
            }

        return stats

    def _suggest_visualizations(
        self, df: pd.DataFrame, column_types: Dict[str, str],
        has_temporal: bool, has_categorical: bool, has_numeric: bool,
        has_network_structure: bool, relationships: List[Tuple]
    ) -> List[Tuple[str, float]]:
        """
        Autonomously suggest the best visualizations with confidence scores.
        Returns list of (visualization_type, confidence_score) tuples.
        """
        suggestions = []

        numeric_cols = [col for col, dtype in column_types.items() if dtype == 'numeric']
        categorical_cols = [col for col, dtype in column_types.items() if dtype == 'categorical']

        # Network graph detection
        if has_network_structure:
            suggestions.append(('3d_network', 0.95))

        # 3D scatter plot - need at least 3 numeric columns
        if len(numeric_cols) >= 3:
            confidence = min(0.9, 0.6 + len(numeric_cols) * 0.1)
            suggestions.append(('3d_scatter', confidence))

        # 3D surface plot - good for continuous functions
        if len(numeric_cols) >= 3 and df.shape[0] >= self.visualization_rules['min_rows_for_surface']:
            # Check if data might represent a surface
            if len(numeric_cols) == 3:
                suggestions.append(('3d_surface', 0.75))

        # 3D line plot - for temporal data with multiple dimensions
        if has_temporal and len(numeric_cols) >= 2:
            suggestions.append(('3d_line', 0.8))

        # 3D bar chart - for categorical with numeric values
        if has_categorical and len(numeric_cols) >= 1:
            if len(categorical_cols) <= 2 and df.shape[0] <= 100:
                suggestions.append(('3d_bar', 0.7))

        # Mesh plot - for spatial data
        spatial_keywords = self.visualization_rules['spatial_indicators']
        has_spatial = any(any(kw in col.lower() for kw in spatial_keywords) for col in df.columns)
        if has_spatial and len(numeric_cols) >= 3:
            suggestions.append(('3d_mesh', 0.85))

        # Sort by confidence score
        suggestions.sort(key=lambda x: x[1], reverse=True)

        return suggestions if suggestions else [('3d_scatter', 0.5)]

    def _print_profile(self, profile: DataProfile):
        """Pretty print the data profile"""
        print("\n" + "="*60)
        print("📊 DATA PROFILE")
        print("="*60)
        print(f"Dimensions: {profile.num_rows} rows × {profile.num_columns} columns")
        print(f"\nColumn Types:")
        for col, dtype in profile.column_types.items():
            print(f"  • {col}: {dtype}")

        print(f"\nData Characteristics:")
        print(f"  • Temporal data: {'✓' if profile.has_temporal else '✗'}")
        print(f"  • Categorical data: {'✓' if profile.has_categorical else '✗'}")
        print(f"  • Numeric data: {'✓' if profile.has_numeric else '✗'}")
        print(f"  • Network structure: {'✓' if profile.has_network_structure else '✗'}")

        if profile.relationships:
            print(f"\n🔗 Detected Relationships:")
            for col1, col2, rel_type in profile.relationships[:5]:
                print(f"  • {col1} ↔ {col2}: {rel_type}")

        print(f"\n🎨 Recommended Visualizations:")
        for i, viz_type in enumerate(profile.suggested_visualizations[:3], 1):
            confidence = profile.confidence_scores[viz_type]
            print(f"  {i}. {viz_type.upper()} (confidence: {confidence:.1%})")
        print("="*60 + "\n")

    def decide_visualization(self, df: pd.DataFrame, preference: Optional[str] = None) -> Tuple[str, DataProfile]:
        """
        Autonomously decide on the best visualization type.

        Args:
            df: DataFrame to visualize
            preference: Optional user preference to override autonomous decision

        Returns:
            Tuple of (visualization_type, data_profile)
        """
        profile = self.analyze_data(df)

        if preference and preference in profile.suggested_visualizations:
            viz_type = preference
            if self.verbose:
                print(f"✓ Using user preference: {viz_type}")
        else:
            viz_type = profile.suggested_visualizations[0]
            if self.verbose:
                print(f"🤖 Autonomous decision: {viz_type} (confidence: {profile.confidence_scores[viz_type]:.1%})")

        return viz_type, profile
