#!/usr/bin/env python3
"""
Excel Integration Utilities
Provides functions for reading and writing Excel files (.xls, .xlsx).
"""

import pandas as pd
import os
import logging
from typing import Optional, List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def read_excel(file_path: str, 
               sheet_name: Optional[str] = None,
               header: int = 0,
               usecols: Optional[List[str]] = None) -> Optional[pd.DataFrame]:
    """
    Read data from an Excel file (.xls or .xlsx).
    
    Args:
        file_path: Path to the Excel file
        sheet_name: Name or index of sheet to read (None = first sheet)
        header: Row number to use as column names (0-indexed)
        usecols: List of column names to read (None = all columns)
        
    Returns:
        DataFrame or None if error
        
    Example:
        df = read_excel('data/sales.xlsx', sheet_name='2024')
        df = read_excel('data/report.xls', usecols=['Date', 'Sales', 'Profit'])
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"Excel file not found: {file_path}")
            return None
        
        # Determine sheet name
        sheet_to_read = sheet_name if sheet_name is not None else 0
        
        logger.info(f"Reading Excel file: {file_path}")
        if sheet_name:
            logger.info(f"Sheet: {sheet_name}")
        
        # Read Excel file
        df = pd.read_excel(
            file_path,
            sheet_name=sheet_to_read,
            header=header,
            usecols=usecols,
            engine='openpyxl'  # Use openpyxl for .xlsx files
        )
        
        logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        logger.info(f"Columns: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error reading Excel file: {str(e)}")
        return None


def list_sheets(file_path: str) -> Optional[List[str]]:
    """
    List all sheet names in an Excel file.
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        List of sheet names or None if error
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"Excel file not found: {file_path}")
            return None
        
        xl_file = pd.ExcelFile(file_path)
        sheets = xl_file.sheet_names
        
        logger.info(f"Found {len(sheets)} sheets: {sheets}")
        return sheets
        
    except Exception as e:
        logger.error(f"Error listing sheets: {str(e)}")
        return None


def write_excel(df: pd.DataFrame,
                file_path: str,
                sheet_name: str = 'Sheet1',
                index: bool = False) -> bool:
    """
    Write DataFrame to an Excel file.
    
    Args:
        df: DataFrame to write
        file_path: Path to save the Excel file
        sheet_name: Name of the sheet
        index: Whether to write row indices
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        logger.info(f"Writing {len(df)} rows to {file_path}")
        
        # Write to Excel
        df.to_excel(file_path, sheet_name=sheet_name, index=index, engine='openpyxl')
        
        logger.info(f"Successfully wrote to {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error writing Excel file: {str(e)}")
        return False


def excel_to_csv(excel_path: str,
                 csv_path: str,
                 sheet_name: Optional[str] = None) -> bool:
    """
    Convert an Excel file to CSV format.
    
    Args:
        excel_path: Path to input Excel file
        csv_path: Path to output CSV file
        sheet_name: Sheet to convert (None = first sheet)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        df = read_excel(excel_path, sheet_name=sheet_name)
        if df is None:
            return False
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        logger.info(f"Converting to CSV: {csv_path}")
        df.to_csv(csv_path, index=False)
        
        logger.info(f"Successfully converted to CSV")
        return True
        
    except Exception as e:
        logger.error(f"Error converting to CSV: {str(e)}")
        return False


def get_excel_info(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Get information about an Excel file.
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        Dictionary with file information or None if error
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"Excel file not found: {file_path}")
            return None
        
        xl_file = pd.ExcelFile(file_path)
        sheets = xl_file.sheet_names
        
        info = {
            'file_path': file_path,
            'file_size': os.path.getsize(file_path),
            'num_sheets': len(sheets),
            'sheet_names': sheets,
            'sheets_info': {}
        }
        
        # Get info for each sheet
        for sheet in sheets:
            df = pd.read_excel(xl_file, sheet_name=sheet, nrows=0)
            info['sheets_info'][sheet] = {
                'columns': list(df.columns),
                'num_columns': len(df.columns)
            }
        
        return info
        
    except Exception as e:
        logger.error(f"Error getting Excel info: {str(e)}")
        return None


def validate_excel_file(file_path: str) -> bool:
    """
    Validate if a file is a valid Excel file.
    
    Args:
        file_path: Path to check
        
    Returns:
        True if valid Excel file, False otherwise
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return False
    
    # Check file extension
    valid_extensions = ['.xls', '.xlsx', '.xlsm', '.xlsb']
    _, ext = os.path.splitext(file_path.lower())
    
    if ext not in valid_extensions:
        logger.error(f"Invalid Excel file extension: {ext}")
        logger.info(f"Valid extensions: {valid_extensions}")
        return False
    
    # Try to read the file
    try:
        pd.ExcelFile(file_path)
        logger.info(f"Valid Excel file: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Invalid Excel file: {str(e)}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Excel file utilities',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List sheets command
    list_parser = subparsers.add_parser('list', help='List sheets in Excel file')
    list_parser.add_argument('file', help='Path to Excel file')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get Excel file information')
    info_parser.add_argument('file', help='Path to Excel file')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert Excel to CSV')
    convert_parser.add_argument('input', help='Input Excel file')
    convert_parser.add_argument('output', help='Output CSV file')
    convert_parser.add_argument('--sheet', help='Sheet name to convert')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_sheets(args.file)
    elif args.command == 'info':
        info = get_excel_info(args.file)
        if info:
            print(f"\nFile: {info['file_path']}")
            print(f"Size: {info['file_size']:,} bytes")
            print(f"Sheets: {info['num_sheets']}")
            for sheet, sheet_info in info['sheets_info'].items():
                print(f"\n  Sheet: {sheet}")
                print(f"  Columns ({sheet_info['num_columns']}): {', '.join(sheet_info['columns'])}")
    elif args.command == 'convert':
        excel_to_csv(args.input, args.output, args.sheet)
    else:
        parser.print_help()
