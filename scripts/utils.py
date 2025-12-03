#!/usr/bin/env python3
"""
Utility Module
Shared functions for data validation, logging, and file operations.
"""

import pandas as pd
import os
import logging
from typing import List, Optional, Dict, Any
import yaml

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def validate_data(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """
    Validate that the DataFrame contains required columns.
    
    Args:
        df: pandas DataFrame to validate
        required_columns: list of required column names
        
    Returns:
        bool: True if valid, False otherwise
    """
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing required columns: {missing_cols}")
        logger.info(f"Available columns: {list(df.columns)}")
        return False
    return True


def validate_file_exists(file_path: str) -> bool:
    """Check if a file exists."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return False
    return True


def ensure_directory(directory: str) -> None:
    """Ensure a directory exists, create if it doesn't."""
    os.makedirs(directory, exist_ok=True)
    logger.debug(f"Directory ensured: {directory}")


def load_csv_data(file_path: str, **kwargs) -> Optional[pd.DataFrame]:
    """
    Load CSV data with error handling.
    
    Args:
        file_path: Path to CSV file
        **kwargs: Additional arguments for pd.read_csv
        
    Returns:
        DataFrame or None if error
    """
    try:
        if not validate_file_exists(file_path):
            return None
        logger.info(f"Loading data from {file_path}")
        df = pd.read_csv(file_path, **kwargs)
        logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        return df
    except Exception as e:
        logger.error(f"Error loading CSV: {str(e)}")
        return None


def save_figure(fig, output_path: str, format: str = 'png', dpi: int = 300, **kwargs) -> bool:
    """
    Save a matplotlib figure with error handling.
    
    Args:
        fig: Matplotlib figure object
        output_path: Path to save the figure
        format: Output format (png, svg, pdf)
        dpi: DPI for raster formats
        **kwargs: Additional savefig arguments
        
    Returns:
        bool: True if successful
    """
    try:
        # Ensure output directory exists
        ensure_directory(os.path.dirname(output_path))
        
        # Adjust extension
        output_path = output_path.rsplit('.', 1)[0] + f'.{format}'
        
        # Save figure
        fig.savefig(output_path, dpi=dpi, format=format, bbox_inches='tight', **kwargs)
        logger.info(f"Figure saved to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving figure: {str(e)}")
        return False


def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Dictionary with configuration
    """
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        else:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return get_default_config()
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}, using defaults")
        return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """Get default configuration."""
    return {
        'output': {
            'format': 'png',
            'dpi': 300,
            'directory': 'examples'
        },
        'style': {
            'theme': 'whitegrid',
            'palette': 'viridis',
            'figure_size': [10, 6]
        },
        'logging': {
            'level': 'INFO'
        }
    }


def clean_data(df: pd.DataFrame, drop_na: bool = True, fill_value: Any = None) -> pd.DataFrame:
    """
    Clean DataFrame by handling missing values.
    
    Args:
        df: Input DataFrame
        drop_na: Whether to drop rows with NA values
        fill_value: Value to fill NAs with (if not dropping)
        
    Returns:
        Cleaned DataFrame
    """
    if drop_na:
        df_clean = df.dropna()
        logger.info(f"Dropped {len(df) - len(df_clean)} rows with missing values")
    elif fill_value is not None:
        df_clean = df.fillna(fill_value)
        logger.info(f"Filled missing values with {fill_value}")
    else:
        df_clean = df
    
    return df_clean


def aggregate_data(df: pd.DataFrame, group_by: str, agg_col: str, 
                   agg_func: str = 'sum') -> pd.DataFrame:
    """
    Aggregate data by grouping.
    
    Args:
        df: Input DataFrame
        group_by: Column to group by
        agg_col: Column to aggregate
        agg_func: Aggregation function (sum, mean, count, etc.)
        
    Returns:
        Aggregated DataFrame
    """
    try:
        agg_df = df.groupby(group_by)[agg_col].agg(agg_func).reset_index()
        logger.info(f"Aggregated data: {len(agg_df)} groups")
        return agg_df
    except Exception as e:
        logger.error(f"Error aggregating data: {str(e)}")
        return df


def filter_data(df: pd.DataFrame, column: str, values: List[Any]) -> pd.DataFrame:
    """
    Filter DataFrame by column values.
    
    Args:
        df: Input DataFrame
        column: Column to filter on
        values: List of values to keep
        
    Returns:
        Filtered DataFrame
    """
    filtered_df = df[df[column].isin(values)]
    logger.info(f"Filtered data: {len(filtered_df)} rows remaining")
    return filtered_df


def get_color_palette(name: str = 'viridis', n_colors: int = 10) -> List:
    """
    Get a color palette.
    
    Args:
        name: Palette name
        n_colors: Number of colors
        
    Returns:
        List of colors
    """
    import seaborn as sns
    return sns.color_palette(name, n_colors=n_colors)
