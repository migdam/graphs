"""
Data Connectors for Various Data Sources
Supports CSV, JSON, Excel, SQL databases, and REST APIs
"""

import pandas as pd
import json
from typing import Dict, Any, Optional, Union
from pathlib import Path
import sqlite3
from urllib.parse import urlparse


class DataConnector:
    """Base class for data connectors"""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def load(self, source: str, **kwargs) -> pd.DataFrame:
        """Load data from source and return as DataFrame"""
        raise NotImplementedError


class CSVConnector(DataConnector):
    """Load data from CSV files"""

    def load(self, source: str, **kwargs) -> pd.DataFrame:
        if self.verbose:
            print(f"📂 Loading CSV from: {source}")

        # Auto-detect datetime columns
        df = pd.read_csv(source, **kwargs)

        # Try to parse date columns
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass

        if self.verbose:
            print(f"✓ Loaded {len(df)} rows from CSV")

        return df


class JSONConnector(DataConnector):
    """Load data from JSON files or strings"""

    def load(self, source: str, **kwargs) -> pd.DataFrame:
        if self.verbose:
            print(f"📂 Loading JSON from: {source}")

        if Path(source).exists():
            # Load from file
            with open(source, 'r') as f:
                data = json.load(f)
        else:
            # Parse as JSON string
            data = json.loads(source)

        # Convert to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            # Check if it's a dict of lists or list of dicts
            if all(isinstance(v, list) for v in data.values()):
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame([data])
        else:
            raise ValueError("Unsupported JSON structure")

        if self.verbose:
            print(f"✓ Loaded {len(df)} rows from JSON")

        return df


class ExcelConnector(DataConnector):
    """Load data from Excel files"""

    def load(self, source: str, sheet_name: Union[str, int] = 0, **kwargs) -> pd.DataFrame:
        if self.verbose:
            print(f"📂 Loading Excel from: {source}, sheet: {sheet_name}")

        df = pd.read_excel(source, sheet_name=sheet_name, **kwargs)

        if self.verbose:
            print(f"✓ Loaded {len(df)} rows from Excel")

        return df


class SQLConnector(DataConnector):
    """Load data from SQL databases"""

    def __init__(self, connection_string: Optional[str] = None, verbose: bool = True):
        super().__init__(verbose)
        self.connection_string = connection_string

    def load(self, source: str, connection_string: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Load data from SQL database.

        Args:
            source: SQL query or table name
            connection_string: Database connection string (sqlite:///path or other SQLAlchemy URL)
        """
        conn_str = connection_string or self.connection_string

        if not conn_str:
            raise ValueError("Connection string required for SQL connector")

        if self.verbose:
            print(f"🗄️ Executing SQL query on: {conn_str}")

        # Detect if source is a query or table name
        if source.strip().lower().startswith('select'):
            query = source
        else:
            query = f"SELECT * FROM {source}"

        # Handle SQLite specially
        if conn_str.startswith('sqlite://'):
            db_path = conn_str.replace('sqlite:///', '')
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
        else:
            # Use SQLAlchemy for other databases
            from sqlalchemy import create_engine
            engine = create_engine(conn_str)
            df = pd.read_sql_query(query, engine)
            engine.dispose()

        if self.verbose:
            print(f"✓ Loaded {len(df)} rows from SQL")

        return df


class APIConnector(DataConnector):
    """Load data from REST APIs"""

    def load(
        self,
        source: str,
        method: str = 'GET',
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data_path: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load data from REST API.

        Args:
            source: API endpoint URL
            method: HTTP method (GET, POST, etc.)
            headers: HTTP headers
            params: Query parameters
            data_path: JSON path to extract data (e.g., 'data.results')
        """
        import requests

        if self.verbose:
            print(f"🌐 Fetching data from API: {source}")

        response = requests.request(
            method=method,
            url=source,
            headers=headers,
            params=params,
            **kwargs
        )
        response.raise_for_status()

        data = response.json()

        # Extract data from nested path if specified
        if data_path:
            for key in data_path.split('.'):
                data = data[key]

        # Convert to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            if all(isinstance(v, list) for v in data.values()):
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame([data])
        else:
            raise ValueError("Unsupported API response structure")

        if self.verbose:
            print(f"✓ Loaded {len(df)} rows from API")

        return df


class DataFrameConnector(DataConnector):
    """Accept an existing pandas DataFrame"""

    def load(self, source: pd.DataFrame, **kwargs) -> pd.DataFrame:
        if self.verbose:
            print(f"📊 Using provided DataFrame")
            print(f"✓ {len(source)} rows available")
        return source.copy()


class AutoConnector:
    """
    Automatically detect and use the appropriate connector based on the source.
    This is the main interface for the autonomous system.
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.connectors = {
            'csv': CSVConnector(verbose),
            'json': JSONConnector(verbose),
            'excel': ExcelConnector(verbose),
            'sql': SQLConnector(verbose=verbose),
            'api': APIConnector(verbose),
            'dataframe': DataFrameConnector(verbose),
        }

    def load(self, source: Any, source_type: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Automatically detect source type and load data.

        Args:
            source: Data source (file path, URL, DataFrame, etc.)
            source_type: Optional explicit source type override
            **kwargs: Additional arguments passed to the connector
        """
        # If DataFrame provided, use directly
        if isinstance(source, pd.DataFrame):
            return self.connectors['dataframe'].load(source, **kwargs)

        # Auto-detect source type
        if source_type is None:
            source_type = self._detect_source_type(source)

        if source_type not in self.connectors:
            raise ValueError(f"Unsupported source type: {source_type}")

        return self.connectors[source_type].load(source, **kwargs)

    def _detect_source_type(self, source: Any) -> str:
        """Automatically detect the source type"""
        if isinstance(source, pd.DataFrame):
            return 'dataframe'

        if isinstance(source, str):
            # Check if it's a URL
            parsed = urlparse(source)
            if parsed.scheme in ['http', 'https']:
                return 'api'

            # Check file extension
            path = Path(source)
            if path.exists():
                ext = path.suffix.lower()
                if ext == '.csv':
                    return 'csv'
                elif ext == '.json':
                    return 'json'
                elif ext in ['.xlsx', '.xls']:
                    return 'excel'
                elif ext in ['.db', '.sqlite', '.sqlite3']:
                    return 'sql'

            # Check if it starts with SQL keywords
            if source.strip().lower().startswith(('select', 'sqlite://', 'postgresql://', 'mysql://')):
                return 'sql'

            # Try to parse as JSON
            try:
                json.loads(source)
                return 'json'
            except:
                pass

        raise ValueError(f"Could not auto-detect source type for: {source}")


# Convenience function for quick loading
def load_data(source: Any, source_type: Optional[str] = None, verbose: bool = True, **kwargs) -> pd.DataFrame:
    """
    Convenience function to load data from any source.

    Args:
        source: Data source (file path, URL, DataFrame, etc.)
        source_type: Optional explicit source type ('csv', 'json', 'excel', 'sql', 'api')
        verbose: Whether to print loading progress
        **kwargs: Additional arguments passed to the connector

    Returns:
        pandas DataFrame
    """
    connector = AutoConnector(verbose=verbose)
    return connector.load(source, source_type, **kwargs)
