"""
AI-Powered Graph Analytics Engine
Automatically extracts insights, detects patterns, and generates intelligent analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class GraphInsight:
    """A single insight about the graph/data"""
    category: str  # 'pattern', 'anomaly', 'trend', 'relationship', 'statistical'
    title: str
    description: str
    confidence: float  # 0.0 to 1.0
    severity: str  # 'low', 'medium', 'high'
    data_points: Dict[str, Any]
    recommendation: Optional[str] = None


@dataclass
class AnalyticsReport:
    """Complete analytics report for a graph"""
    timestamp: str
    data_summary: Dict[str, Any]
    insights: List[GraphInsight]
    patterns: List[str]
    anomalies: List[str]
    trends: List[str]
    recommendations: List[str]
    natural_language_summary: str
    key_findings: List[str]


class AIGraphAnalytics:
    """
    AI-Powered Analytics Engine for Graph Data

    Capabilities:
    - Automatic insight extraction
    - Pattern detection (clusters, cycles, distributions)
    - Anomaly detection (outliers, unusual patterns)
    - Trend analysis (temporal, correlations)
    - Natural language summaries
    - Intelligent recommendations
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.insights = []

    def analyze(
        self,
        df: pd.DataFrame,
        viz_type: str,
        profile: Optional[Any] = None
    ) -> AnalyticsReport:
        """
        Perform comprehensive AI-powered analysis of graph data

        Args:
            df: DataFrame to analyze
            viz_type: Type of visualization being used
            profile: Optional DataProfile from agent_core

        Returns:
            AnalyticsReport with all insights and recommendations
        """
        if self.verbose:
            print("\n🤖 AI Analytics Engine - Starting Analysis")
            print("="*60)

        self.insights = []

        # Run all analysis modules
        self._analyze_statistical(df)
        self._analyze_patterns(df, viz_type)
        self._analyze_anomalies(df)
        self._analyze_trends(df)
        self._analyze_relationships(df)

        if viz_type == '3d_network':
            self._analyze_network_specific(df)

        # Organize insights
        patterns = [i.description for i in self.insights if i.category == 'pattern']
        anomalies = [i.description for i in self.insights if i.category == 'anomaly']
        trends = [i.description for i in self.insights if i.category == 'trend']

        # Generate recommendations
        recommendations = self._generate_recommendations(df, viz_type)

        # Create natural language summary
        summary = self._generate_natural_language_summary(df, viz_type)

        # Extract key findings
        key_findings = self._extract_key_findings()

        # Data summary
        data_summary = self._create_data_summary(df)

        report = AnalyticsReport(
            timestamp=datetime.now().isoformat(),
            data_summary=data_summary,
            insights=self.insights,
            patterns=patterns,
            anomalies=anomalies,
            trends=trends,
            recommendations=recommendations,
            natural_language_summary=summary,
            key_findings=key_findings
        )

        if self.verbose:
            self._print_report(report)

        return report

    def _analyze_statistical(self, df: pd.DataFrame):
        """Extract statistical insights"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            data = df[col].dropna()
            if len(data) == 0:
                continue

            mean = data.mean()
            std = data.std()
            median = data.median()

            # Check for skewness
            skew = data.skew()
            if abs(skew) > 1.0:
                severity = 'high' if abs(skew) > 2.0 else 'medium'
                direction = 'right' if skew > 0 else 'left'

                self.insights.append(GraphInsight(
                    category='statistical',
                    title=f'Skewed Distribution in {col}',
                    description=f'{col} shows {direction}-skewed distribution (skewness: {skew:.2f})',
                    confidence=min(abs(skew) / 3.0, 1.0),
                    severity=severity,
                    data_points={'column': col, 'skewness': float(skew), 'mean': float(mean)},
                    recommendation=f'Consider log transformation or outlier investigation for {col}'
                ))

            # Check coefficient of variation
            if mean != 0:
                cv = (std / abs(mean)) * 100
                if cv > 50:
                    self.insights.append(GraphInsight(
                        category='statistical',
                        title=f'High Variability in {col}',
                        description=f'{col} has high variability (CV: {cv:.1f}%)',
                        confidence=0.9,
                        severity='medium',
                        data_points={'column': col, 'cv': float(cv), 'std': float(std)},
                        recommendation=f'High variability in {col} may indicate multiple subgroups'
                    ))

    def _analyze_patterns(self, df: pd.DataFrame, viz_type: str):
        """Detect patterns in the data"""

        # Clustering patterns for scatter data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            # Simple clustering detection using standard deviation
            for col in numeric_cols[:3]:  # Check first 3 numeric columns
                data = df[col].dropna()
                if len(data) < 10:
                    continue

                # Check for bimodal distribution (simple heuristic)
                hist, bins = np.histogram(data, bins=10)
                peaks = np.where((hist[1:-1] > hist[:-2]) & (hist[1:-1] > hist[2:]))[0] + 1

                if len(peaks) >= 2:
                    self.insights.append(GraphInsight(
                        category='pattern',
                        title=f'Multimodal Distribution in {col}',
                        description=f'{col} shows {len(peaks)} distinct clusters or groups',
                        confidence=0.75,
                        severity='medium',
                        data_points={'column': col, 'peaks': int(len(peaks))},
                        recommendation=f'Consider grouping or segmentation analysis for {col}'
                    ))

        # Periodic patterns
        if any('date' in col.lower() or 'time' in col.lower() for col in df.columns):
            self.insights.append(GraphInsight(
                category='pattern',
                title='Temporal Data Detected',
                description='Data contains time-based information suitable for trend analysis',
                confidence=1.0,
                severity='low',
                data_points={'type': 'temporal'},
                recommendation='Consider time-series analysis or animated visualizations'
            ))

    def _analyze_anomalies(self, df: pd.DataFrame):
        """Detect anomalies and outliers"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            data = df[col].dropna()
            if len(data) < 10:
                continue

            # IQR method for outliers
            q1 = data.quantile(0.25)
            q3 = data.quantile(0.75)
            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outliers = data[(data < lower_bound) | (data > upper_bound)]
            outlier_pct = (len(outliers) / len(data)) * 100

            if outlier_pct > 5:
                self.insights.append(GraphInsight(
                    category='anomaly',
                    title=f'Outliers Detected in {col}',
                    description=f'{outlier_pct:.1f}% of {col} values are statistical outliers',
                    confidence=0.9,
                    severity='high' if outlier_pct > 10 else 'medium',
                    data_points={
                        'column': col,
                        'outlier_count': int(len(outliers)),
                        'outlier_pct': float(outlier_pct),
                        'bounds': [float(lower_bound), float(upper_bound)]
                    },
                    recommendation=f'Investigate outliers in {col} - may indicate errors or special cases'
                ))

    def _analyze_trends(self, df: pd.DataFrame):
        """Detect trends in the data"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        # Linear trends
        if len(numeric_cols) >= 2:
            for i, col1 in enumerate(numeric_cols[:3]):
                for col2 in numeric_cols[i+1:4]:
                    valid_data = df[[col1, col2]].dropna()
                    if len(valid_data) < 10:
                        continue

                    corr = valid_data[col1].corr(valid_data[col2])

                    if abs(corr) > 0.7:
                        direction = 'positive' if corr > 0 else 'negative'
                        strength = 'strong' if abs(corr) > 0.9 else 'moderate'

                        self.insights.append(GraphInsight(
                            category='trend',
                            title=f'{strength.title()} {direction.title()} Correlation',
                            description=f'{col1} and {col2} show {strength} {direction} correlation (r={corr:.3f})',
                            confidence=abs(corr),
                            severity='high' if abs(corr) > 0.9 else 'medium',
                            data_points={
                                'col1': col1,
                                'col2': col2,
                                'correlation': float(corr)
                            },
                            recommendation=f'Strong relationship between {col1} and {col2} suggests predictive potential'
                        ))

        # Monotonic trends (if index is sequential)
        if df.index.is_monotonic_increasing:
            for col in numeric_cols[:3]:
                data = df[col].dropna()
                if len(data) < 10:
                    continue

                # Simple linear regression
                x = np.arange(len(data))
                y = data.values
                slope = np.polyfit(x, y, 1)[0]

                # Normalize slope by data range
                data_range = data.max() - data.min()
                if data_range > 0:
                    normalized_slope = slope * len(data) / data_range

                    if abs(normalized_slope) > 0.3:
                        direction = 'increasing' if normalized_slope > 0 else 'decreasing'
                        self.insights.append(GraphInsight(
                            category='trend',
                            title=f'{direction.title()} Trend in {col}',
                            description=f'{col} shows a clear {direction} trend over the dataset',
                            confidence=min(abs(normalized_slope), 1.0),
                            severity='medium',
                            data_points={'column': col, 'slope': float(slope)},
                            recommendation=f'Monitor {col} - trend suggests continued {direction} pattern'
                        ))

    def _analyze_relationships(self, df: pd.DataFrame):
        """Analyze relationships between variables"""
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        # Categorical vs Numeric relationships
        for cat_col in categorical_cols[:2]:
            for num_col in numeric_cols[:2]:
                groups = df.groupby(cat_col)[num_col].agg(['mean', 'std', 'count'])
                groups = groups[groups['count'] >= 3]  # Need at least 3 samples

                if len(groups) >= 2:
                    # Check variance between groups
                    overall_var = df[num_col].var()
                    between_var = groups['mean'].var()

                    if overall_var > 0:
                        variance_ratio = between_var / overall_var

                        if variance_ratio > 0.3:
                            self.insights.append(GraphInsight(
                                category='relationship',
                                title=f'{cat_col} Influences {num_col}',
                                description=f'{cat_col} groups show distinct {num_col} values',
                                confidence=min(variance_ratio, 1.0),
                                severity='medium',
                                data_points={
                                    'categorical': cat_col,
                                    'numeric': num_col,
                                    'variance_ratio': float(variance_ratio)
                                },
                                recommendation=f'Use {cat_col} for color/grouping in visualizations'
                            ))

    def _analyze_network_specific(self, df: pd.DataFrame):
        """Network-specific analytics"""
        # Detect network columns
        source_col = None
        target_col = None

        for col in df.columns:
            if any(kw in col.lower() for kw in ['source', 'from', 'node1']):
                source_col = col
            elif any(kw in col.lower() for kw in ['target', 'to', 'node2']):
                target_col = col

        if source_col and target_col:
            # Network density
            unique_nodes = pd.concat([df[source_col], df[target_col]]).nunique()
            num_edges = len(df)
            max_edges = unique_nodes * (unique_nodes - 1)

            if max_edges > 0:
                density = num_edges / max_edges

                density_level = 'sparse' if density < 0.1 else 'moderate' if density < 0.5 else 'dense'

                self.insights.append(GraphInsight(
                    category='pattern',
                    title=f'{density_level.title()} Network',
                    description=f'Network has {unique_nodes} nodes and {num_edges} edges (density: {density:.3f})',
                    confidence=1.0,
                    severity='low',
                    data_points={
                        'nodes': int(unique_nodes),
                        'edges': int(num_edges),
                        'density': float(density)
                    },
                    recommendation=f'Network is {density_level}, consider hub analysis'
                ))

            # Hub detection (nodes with many connections)
            node_degrees = pd.concat([
                df[source_col].value_counts(),
                df[target_col].value_counts()
            ]).groupby(level=0).sum()

            if len(node_degrees) > 0:
                avg_degree = node_degrees.mean()
                hubs = node_degrees[node_degrees > avg_degree * 2]

                if len(hubs) > 0:
                    top_hub = hubs.idxmax()
                    self.insights.append(GraphInsight(
                        category='pattern',
                        title='Network Hubs Detected',
                        description=f'{len(hubs)} hub nodes identified, top hub: {top_hub} ({hubs.max():.0f} connections)',
                        confidence=0.95,
                        severity='high',
                        data_points={
                            'hub_count': int(len(hubs)),
                            'top_hub': str(top_hub),
                            'top_connections': int(hubs.max())
                        },
                        recommendation='Focus on hub nodes for network influence analysis'
                    ))

    def _generate_recommendations(self, df: pd.DataFrame, viz_type: str) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Collect recommendations from insights
        for insight in self.insights:
            if insight.recommendation and insight.confidence > 0.7:
                recommendations.append(insight.recommendation)

        # General recommendations based on data
        if len(df) > 1000:
            recommendations.append('Consider aggregation or sampling for better performance with large datasets')

        if df.isnull().sum().sum() > 0:
            null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            if null_pct > 5:
                recommendations.append(f'Dataset has {null_pct:.1f}% missing values - consider imputation or filtering')

        # Visualization-specific recommendations
        if viz_type == '3d_scatter':
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            if len(categorical_cols) > 0:
                recommendations.append(f'Use {categorical_cols[0]} for color encoding to reveal patterns')

        return recommendations[:5]  # Top 5 recommendations

    def _generate_natural_language_summary(self, df: pd.DataFrame, viz_type: str) -> str:
        """Generate natural language summary of the analysis"""
        summary_parts = []

        # Dataset overview
        summary_parts.append(
            f"This {viz_type.replace('3d_', '').replace('_', ' ')} visualization "
            f"represents a dataset with {len(df)} records and {len(df.columns)} variables."
        )

        # Key insights
        high_confidence_insights = [i for i in self.insights if i.confidence > 0.8]
        if high_confidence_insights:
            summary_parts.append(
                f"Analysis identified {len(high_confidence_insights)} high-confidence insights."
            )

        # Patterns
        patterns = [i for i in self.insights if i.category == 'pattern']
        if patterns:
            summary_parts.append(
                f"Detected {len(patterns)} distinct patterns in the data structure."
            )

        # Anomalies
        anomalies = [i for i in self.insights if i.category == 'anomaly']
        if anomalies:
            summary_parts.append(
                f"Found {len(anomalies)} anomalies that may require attention."
            )

        # Trends
        trends = [i for i in self.insights if i.category == 'trend']
        if trends:
            summary_parts.append(
                f"Identified {len(trends)} significant trends or correlations."
            )

        return ' '.join(summary_parts)

    def _extract_key_findings(self) -> List[str]:
        """Extract the most important findings"""
        # Sort insights by confidence and severity
        severity_score = {'high': 3, 'medium': 2, 'low': 1}
        sorted_insights = sorted(
            self.insights,
            key=lambda x: x.confidence * severity_score.get(x.severity, 1),
            reverse=True
        )

        return [f"{i.title}: {i.description}" for i in sorted_insights[:5]]

    def _create_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Create data summary statistics"""
        return {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
            'categorical_columns': len(df.select_dtypes(include=['object', 'category']).columns),
            'missing_values': int(df.isnull().sum().sum()),
            'missing_percentage': float((df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100),
            'memory_usage_mb': float(df.memory_usage(deep=True).sum() / 1024 / 1024)
        }

    def _print_report(self, report: AnalyticsReport):
        """Pretty print the analytics report"""
        print("\n" + "="*60)
        print("📊 AI ANALYTICS REPORT")
        print("="*60)

        print(f"\n📈 Data Summary:")
        print(f"  Records: {report.data_summary['total_records']}")
        print(f"  Columns: {report.data_summary['total_columns']} "
              f"({report.data_summary['numeric_columns']} numeric, "
              f"{report.data_summary['categorical_columns']} categorical)")

        if report.data_summary['missing_percentage'] > 0:
            print(f"  Missing Values: {report.data_summary['missing_values']} "
                  f"({report.data_summary['missing_percentage']:.1f}%)")

        print(f"\n💡 Key Findings ({len(report.key_findings)}):")
        for i, finding in enumerate(report.key_findings, 1):
            print(f"  {i}. {finding}")

        if report.patterns:
            print(f"\n🔍 Patterns Detected ({len(report.patterns)}):")
            for pattern in report.patterns[:3]:
                print(f"  • {pattern}")

        if report.anomalies:
            print(f"\n⚠️  Anomalies Found ({len(report.anomalies)}):")
            for anomaly in report.anomalies[:3]:
                print(f"  • {anomaly}")

        if report.trends:
            print(f"\n📈 Trends Identified ({len(report.trends)}):")
            for trend in report.trends[:3]:
                print(f"  • {trend}")

        if report.recommendations:
            print(f"\n💡 Recommendations ({len(report.recommendations)}):")
            for i, rec in enumerate(report.recommendations, 1):
                print(f"  {i}. {rec}")

        print(f"\n📝 Summary:")
        print(f"  {report.natural_language_summary}")

        print("\n" + "="*60)

    def export_report(self, report: AnalyticsReport, output_path: str):
        """Export analytics report to JSON"""
        report_dict = {
            'timestamp': report.timestamp,
            'data_summary': report.data_summary,
            'insights': [
                {
                    'category': i.category,
                    'title': i.title,
                    'description': i.description,
                    'confidence': i.confidence,
                    'severity': i.severity,
                    'data_points': i.data_points,
                    'recommendation': i.recommendation
                }
                for i in report.insights
            ],
            'patterns': report.patterns,
            'anomalies': report.anomalies,
            'trends': report.trends,
            'recommendations': report.recommendations,
            'summary': report.natural_language_summary,
            'key_findings': report.key_findings
        }

        with open(output_path, 'w') as f:
            json.dump(report_dict, f, indent=2)

        if self.verbose:
            print(f"\n✓ Analytics report exported to: {output_path}")
