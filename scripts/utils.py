#!/usr/bin/env python3

import pandas as pd
import os
import matplotlib.pyplot as plt

def load_data(file_path):
    """
    Load CSV data from a file path.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded data
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    return pd.read_csv(file_path)

def ensure_output_dir(output_path):
    """
    Ensure the output directory exists.
    
    Args:
        output_path (str): Path where the output file will be saved
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

def save_figure(fig, output_path, dpi=300, formats=['png']):
    """
    Save a matplotlib figure in multiple formats.
    
    Args:
        fig: Matplotlib figure object
        output_path (str): Base path for the output file
        dpi (int): Resolution for the output image
        formats (list): List of formats to save (e.g., ['png', 'svg', 'pdf'])
    """
    ensure_output_dir(output_path)
    
    for fmt in formats:
        # Replace extension with the current format
        base_path = os.path.splitext(output_path)[0]
        format_path = f"{base_path}.{fmt}"
        
        plt.savefig(format_path, dpi=dpi, format=fmt)
        print(f"Saved {fmt.upper()} to {format_path}")

def validate_data(df, required_columns):
    """
    Validate that a DataFrame contains required columns.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        required_columns (list): List of required column names
        
    Raises:
        ValueError: If required columns are missing
    """
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    return True

def preprocess_data(df, fill_na=True, remove_duplicates=True):
    """
    Preprocess data with common cleaning operations.
    
    Args:
        df (pd.DataFrame): DataFrame to preprocess
        fill_na (bool): Whether to fill NA values
        remove_duplicates (bool): Whether to remove duplicate rows
        
    Returns:
        pd.DataFrame: Preprocessed DataFrame
    """
    df_copy = df.copy()
    
    if fill_na:
        # Fill numeric columns with mean, categorical with mode
        for col in df_copy.columns:
            if df_copy[col].dtype in ['float64', 'int64']:
                df_copy[col].fillna(df_copy[col].mean(), inplace=True)
            else:
                df_copy[col].fillna(df_copy[col].mode()[0] if not df_copy[col].mode().empty else '', inplace=True)
    
    if remove_duplicates:
        df_copy = df_copy.drop_duplicates()
    
    return df_copy

def get_color_palette(name='viridis', n_colors=10):
    """
    Get a color palette for visualizations.
    
    Args:
        name (str): Name of the color palette
        n_colors (int): Number of colors to generate
        
    Returns:
        list: List of colors
    """
    import seaborn as sns
    return sns.color_palette(name, n_colors)
