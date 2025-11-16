"""
3D Graph Visualizers using Plotly
Supports various types of beautiful 3D visualizations
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import networkx as nx


class Base3DVisualizer:
    """Base class for 3D visualizers"""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.default_config = {
            'width': 1200,
            'height': 800,
            'theme': 'plotly_dark',
        }

    def create(
        self,
        df: pd.DataFrame,
        output_path: Optional[str] = None,
        title: Optional[str] = None,
        **kwargs
    ) -> go.Figure:
        """Create the visualization"""
        raise NotImplementedError

    def _save_figure(self, fig: go.Figure, output_path: str):
        """Save figure to file"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.suffix == '.html':
            fig.write_html(str(path))
        elif path.suffix in ['.png', '.jpg', '.jpeg']:
            fig.write_image(str(path))
        elif path.suffix == '.json':
            fig.write_json(str(path))
        else:
            # Default to HTML
            fig.write_html(str(path) + '.html')

        if self.verbose:
            print(f"✓ Saved visualization to: {output_path}")


class Scatter3DVisualizer(Base3DVisualizer):
    """Create beautiful 3D scatter plots"""

    def create(
        self,
        df: pd.DataFrame,
        x_col: Optional[str] = None,
        y_col: Optional[str] = None,
        z_col: Optional[str] = None,
        color_col: Optional[str] = None,
        size_col: Optional[str] = None,
        output_path: Optional[str] = None,
        title: Optional[str] = None,
        **kwargs
    ) -> go.Figure:
        """
        Create 3D scatter plot.

        Args:
            df: Input DataFrame
            x_col, y_col, z_col: Column names for x, y, z axes (auto-detected if None)
            color_col: Column for color coding
            size_col: Column for marker size
            output_path: Where to save the figure
            title: Plot title
        """
        if self.verbose:
            print("🎨 Creating 3D scatter plot...")

        # Auto-detect numeric columns if not specified
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if x_col is None:
            x_col = numeric_cols[0] if len(numeric_cols) > 0 else df.columns[0]
        if y_col is None:
            y_col = numeric_cols[1] if len(numeric_cols) > 1 else df.columns[1]
        if z_col is None:
            z_col = numeric_cols[2] if len(numeric_cols) > 2 else df.columns[2]

        # Create figure
        fig = px.scatter_3d(
            df,
            x=x_col,
            y=y_col,
            z=z_col,
            color=color_col,
            size=size_col,
            title=title or f"3D Scatter: {x_col} vs {y_col} vs {z_col}",
            template=self.default_config['theme'],
            **kwargs
        )

        # Enhance styling
        fig.update_traces(
            marker=dict(
                line=dict(width=0.5, color='white'),
                opacity=0.8
            )
        )

        fig.update_layout(
            width=self.default_config['width'],
            height=self.default_config['height'],
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col,
            )
        )

        if output_path:
            self._save_figure(fig, output_path)

        return fig


class Surface3DVisualizer(Base3DVisualizer):
    """Create beautiful 3D surface plots"""

    def create(
        self,
        df: pd.DataFrame,
        x_col: Optional[str] = None,
        y_col: Optional[str] = None,
        z_col: Optional[str] = None,
        output_path: Optional[str] = None,
        title: Optional[str] = None,
        colorscale: str = 'Viridis',
        **kwargs
    ) -> go.Figure:
        """Create 3D surface plot"""
        if self.verbose:
            print("🎨 Creating 3D surface plot...")

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if x_col is None:
            x_col = numeric_cols[0] if len(numeric_cols) > 0 else df.columns[0]
        if y_col is None:
            y_col = numeric_cols[1] if len(numeric_cols) > 1 else df.columns[1]
        if z_col is None:
            z_col = numeric_cols[2] if len(numeric_cols) > 2 else df.columns[2]

        # Pivot data for surface plot
        try:
            pivot_df = df.pivot_table(values=z_col, index=y_col, columns=x_col, aggfunc='mean')
        except:
            # If pivot fails, create a grid
            x = df[x_col].values
            y = df[y_col].values
            z = df[z_col].values

            # Create meshgrid
            xi = np.linspace(x.min(), x.max(), 50)
            yi = np.linspace(y.min(), y.max(), 50)
            Xi, Yi = np.meshgrid(xi, yi)

            # Interpolate z values
            from scipy.interpolate import griddata
            Zi = griddata((x, y), z, (Xi, Yi), method='cubic')

            fig = go.Figure(data=[go.Surface(x=Xi, y=Yi, z=Zi, colorscale=colorscale)])
        else:
            fig = go.Figure(data=[go.Surface(
                z=pivot_df.values,
                x=pivot_df.columns,
                y=pivot_df.index,
                colorscale=colorscale
            )])

        fig.update_layout(
            title=title or f"3D Surface: {z_col} over {x_col} and {y_col}",
            template=self.default_config['theme'],
            width=self.default_config['width'],
            height=self.default_config['height'],
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col,
            )
        )

        if output_path:
            self._save_figure(fig, output_path)

        return fig


class Line3DVisualizer(Base3DVisualizer):
    """Create beautiful 3D line plots"""

    def create(
        self,
        df: pd.DataFrame,
        x_col: Optional[str] = None,
        y_col: Optional[str] = None,
        z_col: Optional[str] = None,
        color_col: Optional[str] = None,
        output_path: Optional[str] = None,
        title: Optional[str] = None,
        **kwargs
    ) -> go.Figure:
        """Create 3D line plot"""
        if self.verbose:
            print("🎨 Creating 3D line plot...")

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if x_col is None:
            x_col = numeric_cols[0] if len(numeric_cols) > 0 else df.columns[0]
        if y_col is None:
            y_col = numeric_cols[1] if len(numeric_cols) > 1 else df.columns[1]
        if z_col is None:
            z_col = numeric_cols[2] if len(numeric_cols) > 2 else df.columns[2]

        fig = px.line_3d(
            df,
            x=x_col,
            y=y_col,
            z=z_col,
            color=color_col,
            title=title or f"3D Line: {x_col}, {y_col}, {z_col}",
            template=self.default_config['theme'],
            **kwargs
        )

        fig.update_traces(line=dict(width=3))

        fig.update_layout(
            width=self.default_config['width'],
            height=self.default_config['height'],
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col,
            )
        )

        if output_path:
            self._save_figure(fig, output_path)

        return fig


class Network3DVisualizer(Base3DVisualizer):
    """Create beautiful 3D network graphs"""

    def create(
        self,
        df: pd.DataFrame,
        source_col: Optional[str] = None,
        target_col: Optional[str] = None,
        weight_col: Optional[str] = None,
        node_color_col: Optional[str] = None,
        output_path: Optional[str] = None,
        title: Optional[str] = None,
        layout: str = 'spring',
        **kwargs
    ) -> go.Figure:
        """
        Create 3D network graph.

        Args:
            df: DataFrame with edge list
            source_col: Source node column
            target_col: Target node column
            weight_col: Edge weight column
            node_color_col: Column for node colors
            layout: Layout algorithm ('spring', 'kamada_kawai', 'circular')
        """
        if self.verbose:
            print("🎨 Creating 3D network graph...")

        # Auto-detect source and target columns
        if source_col is None:
            for col in df.columns:
                if any(kw in col.lower() for kw in ['source', 'from', 'node1', 'src']):
                    source_col = col
                    break
            if source_col is None:
                source_col = df.columns[0]

        if target_col is None:
            for col in df.columns:
                if any(kw in col.lower() for kw in ['target', 'to', 'node2', 'dst', 'dest']):
                    target_col = col
                    break
            if target_col is None:
                source_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]

        # Create NetworkX graph
        G = nx.from_pandas_edgelist(
            df,
            source=source_col,
            target=target_col,
            edge_attr=weight_col
        )

        # Calculate 3D layout
        if layout == 'spring':
            pos = nx.spring_layout(G, dim=3, seed=42)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G, dim=3)
        elif layout == 'circular':
            pos_2d = nx.circular_layout(G)
            pos = {node: np.array([coords[0], coords[1], 0]) for node, coords in pos_2d.items()}
        else:
            pos = nx.spring_layout(G, dim=3, seed=42)

        # Extract coordinates
        edge_x = []
        edge_y = []
        edge_z = []

        for edge in G.edges():
            x0, y0, z0 = pos[edge[0]]
            x1, y1, z1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_z.extend([z0, z1, None])

        edge_trace = go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(color='rgba(125, 125, 125, 0.5)', width=2),
            hoverinfo='none',
            name='Edges'
        )

        node_x = []
        node_y = []
        node_z = []
        node_text = []

        for node in G.nodes():
            x, y, z = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_z.append(z)
            node_text.append(f"Node: {node}<br>Connections: {len(list(G.neighbors(node)))}")

        node_trace = go.Scatter3d(
            x=node_x, y=node_y, z=node_z,
            mode='markers+text',
            text=[str(node) for node in G.nodes()],
            textposition='top center',
            hovertext=node_text,
            hoverinfo='text',
            marker=dict(
                size=10,
                color=[len(list(G.neighbors(node))) for node in G.nodes()],
                colorscale='Viridis',
                colorbar=dict(title="Connections"),
                line=dict(color='white', width=0.5)
            ),
            name='Nodes'
        )

        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace])

        fig.update_layout(
            title=title or "3D Network Graph",
            template=self.default_config['theme'],
            width=self.default_config['width'],
            height=self.default_config['height'],
            showlegend=True,
            hovermode='closest',
            scene=dict(
                xaxis=dict(showbackground=False, showticklabels=False, title=''),
                yaxis=dict(showbackground=False, showticklabels=False, title=''),
                zaxis=dict(showbackground=False, showticklabels=False, title=''),
            )
        )

        if output_path:
            self._save_figure(fig, output_path)

        return fig


class Bar3DVisualizer(Base3DVisualizer):
    """Create beautiful 3D bar charts"""

    def create(
        self,
        df: pd.DataFrame,
        x_col: Optional[str] = None,
        y_col: Optional[str] = None,
        z_col: Optional[str] = None,
        output_path: Optional[str] = None,
        title: Optional[str] = None,
        **kwargs
    ) -> go.Figure:
        """Create 3D bar chart"""
        if self.verbose:
            print("🎨 Creating 3D bar chart...")

        # Auto-detect columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if x_col is None:
            x_col = categorical_cols[0] if categorical_cols else df.columns[0]
        if y_col is None:
            y_col = categorical_cols[1] if len(categorical_cols) > 1 else (numeric_cols[0] if numeric_cols else df.columns[1])
        if z_col is None:
            z_col = numeric_cols[0] if numeric_cols else df.columns[2]

        # Create pivot for 3D bars
        if x_col in categorical_cols and y_col in categorical_cols:
            pivot = df.pivot_table(values=z_col, index=x_col, columns=y_col, aggfunc='sum', fill_value=0)

            fig = go.Figure(data=[go.Surface(
                z=pivot.values,
                x=pivot.columns,
                y=pivot.index,
                colorscale='Plasma'
            )])
        else:
            # Use scatter with markers as bars
            fig = go.Figure(data=[go.Scatter3d(
                x=df[x_col],
                y=df[y_col],
                z=df[z_col],
                mode='markers',
                marker=dict(
                    size=12,
                    color=df[z_col],
                    colorscale='Plasma',
                    colorbar=dict(title=z_col),
                    line=dict(width=0.5, color='white')
                )
            )])

        fig.update_layout(
            title=title or f"3D Bar Chart: {z_col}",
            template=self.default_config['theme'],
            width=self.default_config['width'],
            height=self.default_config['height'],
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col,
            )
        )

        if output_path:
            self._save_figure(fig, output_path)

        return fig


class VisualizerFactory:
    """Factory to create appropriate visualizer"""

    VISUALIZERS = {
        '3d_scatter': Scatter3DVisualizer,
        '3d_surface': Surface3DVisualizer,
        '3d_line': Line3DVisualizer,
        '3d_network': Network3DVisualizer,
        '3d_bar': Bar3DVisualizer,
    }

    @classmethod
    def create(cls, viz_type: str, verbose: bool = True) -> Base3DVisualizer:
        """Create visualizer instance"""
        if viz_type not in cls.VISUALIZERS:
            raise ValueError(f"Unknown visualizer type: {viz_type}. Available: {list(cls.VISUALIZERS.keys())}")

        return cls.VISUALIZERS[viz_type](verbose=verbose)

    @classmethod
    def available_types(cls) -> List[str]:
        """Get list of available visualizer types"""
        return list(cls.VISUALIZERS.keys())
