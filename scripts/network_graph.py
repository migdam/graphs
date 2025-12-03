#!/usr/bin/env python3
"""
Network Graph Generator
Creates network/graph visualizations for relationship data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import os
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def validate_data(df, required_columns):
    """Validate that the DataFrame contains required columns."""
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing required columns: {missing_cols}")
        logger.info(f"Available columns: {list(df.columns)}")
        return False
    return True


def create_network_graph(data_path="../data/network_data.csv", 
                        output_path="../examples/network_graph.png",
                        source_col='source',
                        target_col='target',
                        weight_col=None,
                        layout='spring',
                        output_format='png'):
    """
    Create a network graph from CSV data.
    
    Args:
        data_path: Path to input CSV file with edge list
        output_path: Path to save output image
        source_col: Column name for source nodes
        target_col: Column name for target nodes
        weight_col: Optional column name for edge weights
        layout: Layout algorithm (spring, circular, random, shell)
        output_format: Output format (png, svg, pdf)
    """
    try:
        # Check if file exists
        if not os.path.exists(data_path):
            logger.error(f"Data file not found: {data_path}")
            return False
        
        # Read the data
        logger.info(f"Reading data from {data_path}")
        df = pd.read_csv(data_path)
        
        # Validate required columns
        required_cols = [source_col, target_col]
        if weight_col:
            required_cols.append(weight_col)
            
        if not validate_data(df, required_cols):
            return False
        
        # Create graph
        if weight_col:
            G = nx.from_pandas_edgelist(df, source=source_col, target=target_col, 
                                       edge_attr=weight_col)
        else:
            G = nx.from_pandas_edgelist(df, source=source_col, target=target_col)
        
        logger.info(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        
        # Create figure
        plt.figure(figsize=(14, 10))
        
        # Choose layout
        layout_functions = {
            'spring': nx.spring_layout,
            'circular': nx.circular_layout,
            'random': nx.random_layout,
            'shell': nx.shell_layout
        }
        
        if layout not in layout_functions:
            logger.warning(f"Unknown layout '{layout}', using 'spring' instead")
            layout = 'spring'
        
        pos = layout_functions[layout](G, seed=42)
        
        # Calculate node sizes based on degree
        node_sizes = [300 + 100 * G.degree(node) for node in G.nodes()]
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                              node_color='lightblue', alpha=0.9,
                              edgecolors='darkblue', linewidths=2)
        
        # Draw edges
        if weight_col:
            edges = G.edges()
            weights = [G[u][v][weight_col] for u, v in edges]
            nx.draw_networkx_edges(G, pos, width=weights, alpha=0.5, 
                                  edge_color='gray')
        else:
            nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.5, 
                                  edge_color='gray')
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        # Customize the chart
        plt.title('Network Graph Visualization', fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        
        # Add network statistics as text
        stats_text = f"Nodes: {G.number_of_nodes()}\n"
        stats_text += f"Edges: {G.number_of_edges()}\n"
        if G.number_of_nodes() > 0:
            stats_text += f"Avg Degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}"
        
        plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Adjust output path extension
        output_path = output_path.rsplit('.', 1)[0] + f'.{output_format}'
        
        # Save the chart
        plt.savefig(output_path, dpi=300, format=output_format, bbox_inches='tight')
        logger.info(f"Network graph saved to {output_path}")
        
        # Show the chart
        plt.show()
        return True
        
    except Exception as e:
        logger.error(f"Error creating network graph: {str(e)}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate a network graph from CSV edge list',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--data', type=str, default='../data/network_data.csv',
                        help='Path to the CSV data file (edge list)')
    parser.add_argument('--output', type=str, default='../examples/network_graph.png',
                        help='Path to save the output image')
    parser.add_argument('--source', type=str, default='source',
                        help='Column name for source nodes')
    parser.add_argument('--target', type=str, default='target',
                        help='Column name for target nodes')
    parser.add_argument('--weight', type=str, default=None,
                        help='Column name for edge weights (optional)')
    parser.add_argument('--layout', type=str, default='spring',
                        choices=['spring', 'circular', 'random', 'shell'],
                        help='Graph layout algorithm')
    parser.add_argument('--format', type=str, default='png', choices=['png', 'svg', 'pdf'],
                        help='Output format')
    
    args = parser.parse_args()
    
    success = create_network_graph(
        args.data,
        args.output,
        args.source,
        args.target,
        args.weight,
        args.layout,
        args.format
    )
    
    sys.exit(0 if success else 1)
