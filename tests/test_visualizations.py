#!/usr/bin/env python3

import unittest
import pandas as pd
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from utils import load_data

class TestVisualizations(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_data.csv')
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'test_output')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def test_load_data(self):
        """Test loading CSV data"""
        if os.path.exists(self.data_path):
            df = load_data(self.data_path)
            self.assertIsInstance(df, pd.DataFrame)
            self.assertGreater(len(df), 0)
    
    def test_data_structure(self):
        """Test that data has expected structure"""
        if os.path.exists(self.data_path):
            df = load_data(self.data_path)
            expected_columns = ['date', 'category', 'value']
            for col in expected_columns:
                self.assertIn(col, df.columns)
    
    def tearDown(self):
        """Clean up test outputs"""
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                os.remove(os.path.join(self.output_dir, file))
            os.rmdir(self.output_dir)

if __name__ == '__main__':
    unittest.main()
