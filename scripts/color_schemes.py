#!/usr/bin/env python3

import seaborn as sns

# Define various color schemes for different visualization types
COLOR_SCHEMES = {
    'default': {
        'palette': 'viridis',
        'sequential': 'YlGnBu',
        'diverging': 'RdYlBu',
        'categorical': 'Set2'
    },
    'professional': {
        'palette': 'muted',
        'sequential': 'Blues',
        'diverging': 'coolwarm',
        'categorical': 'Set1'
    },
    'vibrant': {
        'palette': 'bright',
        'sequential': 'plasma',
        'diverging': 'Spectral',
        'categorical': 'husl'
    },
    'pastel': {
        'palette': 'pastel',
        'sequential': 'PuBuGn',
        'diverging': 'PiYG',
        'categorical': 'Pastel1'
    },
    'dark': {
        'palette': 'dark',
        'sequential': 'cividis',
        'diverging': 'BrBG',
        'categorical': 'Dark2'
    }
}

def get_palette(scheme='default', palette_type='palette', n_colors=10):
    """
    Get a color palette based on the scheme and type.
    
    Args:
        scheme (str): Color scheme name (default, professional, vibrant, pastel, dark)
        palette_type (str): Type of palette (palette, sequential, diverging, categorical)
        n_colors (int): Number of colors to generate
        
    Returns:
        list: List of colors
    """
    if scheme not in COLOR_SCHEMES:
        scheme = 'default'
    
    if palette_type not in COLOR_SCHEMES[scheme]:
        palette_type = 'palette'
    
    palette_name = COLOR_SCHEMES[scheme][palette_type]
    
    try:
        return sns.color_palette(palette_name, n_colors)
    except:
        return sns.color_palette('viridis', n_colors)

def apply_style(scheme='default', context='notebook'):
    """
    Apply a predefined style to all visualizations.
    
    Args:
        scheme (str): Color scheme name
        context (str): Seaborn context (paper, notebook, talk, poster)
    """
    sns.set_theme(style='whitegrid', context=context)
    
    # Set the color palette
    if scheme in COLOR_SCHEMES:
        palette = get_palette(scheme, 'palette')
        sns.set_palette(palette)

def list_schemes():
    """
    List all available color schemes.
    
    Returns:
        list: List of scheme names
    """
    return list(COLOR_SCHEMES.keys())

def get_scheme_info(scheme='default'):
    """
    Get information about a specific color scheme.
    
    Args:
        scheme (str): Color scheme name
        
    Returns:
        dict: Dictionary with scheme information
    """
    if scheme not in COLOR_SCHEMES:
        return None
    
    return COLOR_SCHEMES[scheme]

if __name__ == "__main__":
    print("Available color schemes:")
    for scheme in list_schemes():
        print(f"  - {scheme}: {get_scheme_info(scheme)}")
