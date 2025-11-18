#!/usr/bin/env python3

import yaml
import os

class ConfigLoader:
    """Load and manage configuration from YAML file"""
    
    def __init__(self, config_path='config.yaml'):
        """
        Initialize the config loader.
        
        Args:
            config_path (str): Path to the configuration YAML file
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_path):
            return self._default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._default_config()
    
    def _default_config(self):
        """Return default configuration"""
        return {
            'data': {
                'default_path': 'data/sample_data.csv'
            },
            'output': {
                'default_directory': 'examples',
                'default_format': 'png',
                'dpi': 300
            },
            'visualization': {
                'default_style': 'whitegrid',
                'color_scheme': 'default'
            }
        }
    
    def get(self, key_path, default=None):
        """
        Get a configuration value using dot notation.
        
        Args:
            key_path (str): Path to the config key (e.g., 'output.dpi')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_chart_config(self, chart_type):
        """
        Get configuration for a specific chart type.
        
        Args:
            chart_type (str): Type of chart
            
        Returns:
            dict: Chart configuration
        """
        return self.get(f'charts.{chart_type}', {})

if __name__ == "__main__":
    loader = ConfigLoader()
    print("Configuration loaded successfully!")
    print(f"Default data path: {loader.get('data.default_path')}")
    print(f"Output DPI: {loader.get('output.dpi')}")
