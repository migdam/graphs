#!/usr/bin/env python3

import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from utils import validate_data, preprocess_data, load_data

class TestUtils(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.sample_df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'category': ['A', 'B', 'A'],
            'value': [45, 67, np.nan]
        })
    
    def test_validate_data_success(self):
        """Test data validation with correct columns"""
        required_columns = ['date', 'category', 'value']
        self.assertTrue(validate_data(self.sample_df, required_columns))
    
    def test_validate_data_failure(self):
        """Test data validation with missing columns"""
        required_columns = ['date', 'category', 'value', 'missing_column']
        with self.assertRaises(ValueError):
            validate_data(self.sample_df, required_columns)
    
    def test_preprocess_data_fill_na(self):
        """Test preprocessing with NA filling"""
        processed_df = preprocess_data(self.sample_df, fill_na=True)
        self.assertFalse(processed_df['value'].isna().any())
    
    def test_preprocess_data_remove_duplicates(self):
        """Test preprocessing with duplicate removal"""
        df_with_dupes = pd.concat([self.sample_df, self.sample_df.iloc[[0]]])
        processed_df = preprocess_data(df_with_dupes, remove_duplicates=True)
        self.assertEqual(len(processed_df), len(self.sample_df))

if __name__ == '__main__':
    unittest.main()
