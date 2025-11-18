# API Reference

Complete API documentation for the Autonomous 3D Graph Generation System v1.1.0

---

## Table of Contents

1. [Main System](#main-system)
2. [Agent Core](#agent-core)
3. [Data Connectors](#data-connectors)
4. [Visualizers](#visualizers)
5. [AI Analytics](#ai-analytics)
6. [CLI](#cli)

---

## Main System

### `AutonomousGraphSystem`

Main orchestrator class for autonomous graph generation.

```python
from agentic_graphs import AutonomousGraphSystem

system = AutonomousGraphSystem(verbose=True)
```

#### Constructor

```python
__init__(verbose: bool = True)
```

**Parameters**:
- `verbose` (bool): Print detailed progress information. Default: `True`

**Initializes**:
- Decision agent
- Data connectors
- AI Analytics engine
- Visualization factory

#### Methods

##### `generate()`

Generate a 3D visualization autonomously.

```python
generate(
    data_source: Any,
    output_path: Optional[str] = None,
    viz_type: Optional[str] = None,
    source_type: Optional[str] = None,
    title: Optional[str] = None,
    show: bool = True,
    **kwargs
) -> go.Figure
```

**Parameters**:
- `data_source`: Data source (file path, URL, DataFrame, SQL query, etc.)
- `output_path`: Where to save visualization (HTML, PNG, etc.)
- `viz_type`: Override visualization type ('3d_scatter', '3d_network', etc.)
- `source_type`: Override data source type ('csv', 'json', 'excel', 'sql', 'api')
- `title`: Custom title for visualization
- `show`: Whether to display the visualization
- `**kwargs`: Additional parameters for visualizer or data loader

**Visualizer Parameters** (`**kwargs`):
- `x_col`, `y_col`, `z_col`: Column names for axes
- `color_col`: Column for color encoding
- `size_col`: Column for size encoding
- `source_col`, `target_col`: Network graph columns
- `weight_col`: Edge weight column
- `layout`: Network layout algorithm ('spring', 'kamada_kawai', 'circular')
- `colorscale`: Color scheme name

**Returns**: `plotly.graph_objects.Figure`

**Example**:
```python
fig = system.generate(
    'data.csv',
    viz_type='3d_scatter',
    x_col='x',
    y_col='y',
    z_col='z',
    color_col='category',
    title='My Visualization',
    output_path='output.html'
)
```

##### `analyze()`

Analyze data without generating visualization.

```python
analyze(
    data_source: Any,
    source_type: Optional[str] = None,
    **kwargs
) -> DataProfile
```

**Parameters**:
- `data_source`: Data source to analyze
- `source_type`: Override data source type
- `**kwargs`: Additional data loader parameters

**Returns**: `DataProfile` object with analysis results

**Example**:
```python
profile = system.analyze('data.csv')
print(profile.suggested_visualizations)
print(profile.confidence_scores)
```

##### `run_analytics()`

Run AI-powered analytics on data.

```python
run_analytics(
    data_source: Any,
    viz_type: Optional[str] = None,
    source_type: Optional[str] = None,
    export_path: Optional[str] = None,
    **kwargs
) -> AnalyticsReport
```

**Parameters**:
- `data_source`: Data source to analyze
- `viz_type`: Visualization type for context (auto-detected if None)
- `source_type`: Override data source type
- `export_path`: Path to export JSON report
- `**kwargs`: Additional data loader parameters

**Returns**: `AnalyticsReport` object

**Example**:
```python
report = system.run_analytics(
    'data.csv',
    export_path='analytics.json'
)
print(report.key_findings)
print(report.recommendations)
```

##### `generate_with_analytics()`

Generate visualization AND run AI analytics in one step.

```python
generate_with_analytics(
    data_source: Any,
    output_path: Optional[str] = None,
    analytics_path: Optional[str] = None,
    viz_type: Optional[str] = None,
    source_type: Optional[str] = None,
    title: Optional[str] = None,
    show: bool = True,
    **kwargs
) -> Tuple[go.Figure, AnalyticsReport]
```

**Parameters**:
- All parameters from `generate()` plus:
- `analytics_path`: Path to export analytics JSON

**Returns**: Tuple of `(Figure, AnalyticsReport)`

**Example**:
```python
fig, report = system.generate_with_analytics(
    'data.csv',
    output_path='viz.html',
    analytics_path='analytics.json'
)

# Use the figure
fig.show()

# Use the analytics
for insight in report.insights:
    print(insight.title)
```

##### `batch_generate()`

Generate visualizations for multiple data sources.

```python
batch_generate(
    data_sources: list,
    output_dir: str = 'examples/batch',
    **kwargs
) -> Dict[str, go.Figure]
```

**Parameters**:
- `data_sources`: List of data sources
- `output_dir`: Directory to save all visualizations
- `**kwargs`: Additional parameters passed to each generation

**Returns**: Dictionary mapping source names to Figure objects

**Example**:
```python
results = system.batch_generate([
    'file1.csv',
    'file2.json',
    'file3.xlsx'
], output_dir='visualizations/')
```

##### `suggest_visualizations()`

Get visualization suggestions without generating.

```python
suggest_visualizations(
    data_source: Any,
    source_type: Optional[str] = None
) -> List[Tuple[str, float]]
```

**Parameters**:
- `data_source`: Data source to analyze
- `source_type`: Override data source type

**Returns**: List of `(visualization_type, confidence_score)` tuples

**Example**:
```python
suggestions = system.suggest_visualizations('data.csv')
for viz_type, confidence in suggestions:
    print(f"{viz_type}: {confidence:.1%}")
```

##### `available_visualizations()`

Get list of all available visualization types.

```python
available_visualizations() -> List[str]
```

**Returns**: List of visualization type names

**Example**:
```python
viz_types = system.available_visualizations()
# ['3d_scatter', '3d_surface', '3d_line', '3d_network', '3d_bar']
```

---

### Convenience Functions

#### `auto_visualize()`

Quick function to autonomously visualize any data source.

```python
from agentic_graphs import auto_visualize

auto_visualize(
    data_source: Any,
    output_path: Optional[str] = None,
    verbose: bool = True,
    **kwargs
) -> go.Figure
```

**Example**:
```python
auto_visualize('data.csv')
auto_visualize('data.json', viz_type='3d_scatter', output_path='out.html')
```

#### `analyze_data()`

Quick function to analyze data without visualization.

```python
from agentic_graphs import analyze_data

analyze_data(
    data_source: Any,
    verbose: bool = True
) -> DataProfile
```

**Example**:
```python
profile = analyze_data('data.csv')
```

---

## Agent Core

### `AutonomousGraphAgent`

Agent that analyzes data and makes autonomous decisions.

```python
from agentic_graphs import AutonomousGraphAgent

agent = AutonomousGraphAgent(verbose=True)
```

#### Methods

##### `analyze_data()`

Comprehensively analyze a dataset.

```python
analyze_data(df: pd.DataFrame) -> DataProfile
```

**Parameters**:
- `df`: pandas DataFrame to analyze

**Returns**: `DataProfile` object

##### `decide_visualization()`

Autonomously decide on visualization type.

```python
decide_visualization(
    df: pd.DataFrame,
    preference: Optional[str] = None
) -> Tuple[str, DataProfile]
```

**Parameters**:
- `df`: pandas DataFrame
- `preference`: Optional user preference to override

**Returns**: Tuple of `(visualization_type, data_profile)`

### `DataProfile`

Data class containing analysis results.

**Attributes**:
- `num_rows` (int): Number of rows
- `num_columns` (int): Number of columns
- `column_names` (List[str]): Column names
- `column_types` (Dict[str, str]): Column type mapping
- `has_temporal` (bool): Has temporal data
- `has_categorical` (bool): Has categorical data
- `has_numeric` (bool): Has numeric data
- `has_network_structure` (bool): Has network structure
- `relationships` (List[Tuple]): Detected relationships
- `statistical_summary` (Dict): Statistical summary
- `suggested_visualizations` (List[str]): Ranked suggestions
- `confidence_scores` (Dict[str, float]): Confidence for each suggestion

---

## Data Connectors

### `load_data()`

Convenience function to load data from any source.

```python
from agentic_graphs import load_data

load_data(
    source: Any,
    source_type: Optional[str] = None,
    verbose: bool = True,
    **kwargs
) -> pd.DataFrame
```

**Parameters**:
- `source`: Data source (file path, URL, DataFrame, etc.)
- `source_type`: Explicit source type ('csv', 'json', 'excel', 'sql', 'api')
- `verbose`: Print loading progress
- `**kwargs`: Additional arguments for the connector

**Returns**: pandas DataFrame

**Example**:
```python
df = load_data('data.csv')
df = load_data('data.json', source_type='json')
df = load_data('SELECT * FROM table', source_type='sql',
              connection_string='sqlite:///db.db')
```

### `AutoConnector`

Automatically detects and uses appropriate connector.

```python
from agentic_graphs import AutoConnector

connector = AutoConnector(verbose=True)
df = connector.load('data.csv')
```

### Individual Connectors

#### `CSVConnector`

```python
from agentic_graphs import CSVConnector

connector = CSVConnector(verbose=True)
df = connector.load('data.csv')
```

#### `JSONConnector`

```python
from agentic_graphs import JSONConnector

connector = JSONConnector(verbose=True)
df = connector.load('data.json')
```

#### `ExcelConnector`

```python
from agentic_graphs import ExcelConnector

connector = ExcelConnector(verbose=True)
df = connector.load('data.xlsx', sheet_name='Sheet1')
```

#### `SQLConnector`

```python
from agentic_graphs import SQLConnector

connector = SQLConnector(
    connection_string='sqlite:///database.db',
    verbose=True
)
df = connector.load('SELECT * FROM table')
```

#### `APIConnector`

```python
from agentic_graphs import APIConnector

connector = APIConnector(verbose=True)
df = connector.load(
    'https://api.example.com/data',
    method='GET',
    headers={'Authorization': 'Bearer token'},
    data_path='data.results'  # JSON path to extract
)
```

---

## Visualizers

### `VisualizerFactory`

Factory class for creating visualizers.

```python
from agentic_graphs import VisualizerFactory

# Get available types
types = VisualizerFactory.available_types()

# Create visualizer
visualizer = VisualizerFactory.create('3d_scatter', verbose=True)
```

#### Methods

##### `available_types()`

```python
@classmethod
available_types() -> List[str]
```

**Returns**: List of available visualization types

##### `create()`

```python
@classmethod
create(viz_type: str, verbose: bool = True) -> Base3DVisualizer
```

**Parameters**:
- `viz_type`: Visualization type ('3d_scatter', '3d_network', etc.)
- `verbose`: Print progress

**Returns**: Visualizer instance

### Visualizer Types

All visualizers have a `create()` method:

```python
create(
    df: pd.DataFrame,
    output_path: Optional[str] = None,
    title: Optional[str] = None,
    **kwargs
) -> go.Figure
```

#### `Scatter3DVisualizer`

```python
visualizer.create(
    df,
    x_col='x',
    y_col='y',
    z_col='z',
    color_col='category',
    size_col='value',
    output_path='output.html'
)
```

#### `Surface3DVisualizer`

```python
visualizer.create(
    df,
    x_col='x',
    y_col='y',
    z_col='z',
    colorscale='Viridis',
    output_path='output.html'
)
```

#### `Line3DVisualizer`

```python
visualizer.create(
    df,
    x_col='x',
    y_col='y',
    z_col='z',
    color_col='category',
    output_path='output.html'
)
```

#### `Network3DVisualizer`

```python
visualizer.create(
    df,
    source_col='source',
    target_col='target',
    weight_col='weight',
    layout='spring',
    output_path='output.html'
)
```

#### `Bar3DVisualizer`

```python
visualizer.create(
    df,
    x_col='category',
    y_col='group',
    z_col='value',
    output_path='output.html'
)
```

---

## AI Analytics

### `AIGraphAnalytics`

AI-powered analytics engine for graph data.

```python
from agentic_graphs import AIGraphAnalytics

analytics = AIGraphAnalytics(verbose=True)
```

#### Methods

##### `analyze()`

Perform comprehensive analysis.

```python
analyze(
    df: pd.DataFrame,
    viz_type: str,
    profile: Optional[DataProfile] = None
) -> AnalyticsReport
```

**Parameters**:
- `df`: DataFrame to analyze
- `viz_type`: Visualization type for context
- `profile`: Optional DataProfile from agent

**Returns**: `AnalyticsReport` object

**Example**:
```python
report = analytics.analyze(df, '3d_scatter')

# Access insights
for insight in report.insights:
    print(f"{insight.title}: {insight.confidence:.0%}")
    print(f"  Category: {insight.category}")
    print(f"  Severity: {insight.severity}")
    if insight.recommendation:
        print(f"  Recommendation: {insight.recommendation}")
```

##### `export_report()`

Export analytics report to JSON.

```python
export_report(report: AnalyticsReport, output_path: str)
```

**Parameters**:
- `report`: AnalyticsReport to export
- `output_path`: Path to JSON file

### `GraphInsight`

Data class representing a single insight.

**Attributes**:
- `category` (str): 'pattern', 'anomaly', 'trend', 'relationship', 'statistical'
- `title` (str): Short title
- `description` (str): Detailed description
- `confidence` (float): 0.0 to 1.0
- `severity` (str): 'low', 'medium', 'high'
- `data_points` (Dict): Supporting data
- `recommendation` (Optional[str]): Actionable suggestion

**Example**:
```python
insight = report.insights[0]
print(f"Title: {insight.title}")
print(f"Confidence: {insight.confidence:.0%}")
print(f"Category: {insight.category}")
print(f"Severity: {insight.severity}")
```

### `AnalyticsReport`

Data class containing complete analytics.

**Attributes**:
- `timestamp` (str): ISO 8601 timestamp
- `data_summary` (Dict): Statistical summary
  - `total_records`: Number of rows
  - `total_columns`: Number of columns
  - `numeric_columns`: Count of numeric columns
  - `categorical_columns`: Count of categorical columns
  - `missing_values`: Total missing values
  - `missing_percentage`: Percentage missing
  - `memory_usage_mb`: Memory usage
- `insights` (List[GraphInsight]): All insights
- `patterns` (List[str]): Detected patterns
- `anomalies` (List[str]): Detected anomalies
- `trends` (List[str]): Identified trends
- `recommendations` (List[str]): Action items
- `natural_language_summary` (str): Human-readable summary
- `key_findings` (List[str]): Top 5 most important insights

**Example**:
```python
report = system.run_analytics('data.csv')

# Summary statistics
print(f"Records: {report.data_summary['total_records']}")
print(f"Columns: {report.data_summary['total_columns']}")

# Key findings
for finding in report.key_findings:
    print(f"• {finding}")

# Recommendations
for rec in report.recommendations:
    print(f"→ {rec}")

# Summary
print(report.natural_language_summary)
```

---

## CLI

### Command Line Interface

```bash
python -m agentic_graphs.cli [OPTIONS] [DATA_SOURCE ...]
```

### Options

#### Data Source
```
data_source              Data source(s) - file path, URL, or SQL query
```

#### Output
```
-o, --output PATH        Output file path (HTML, PNG, etc.)
--title TEXT             Custom title for the visualization
--no-show                Do not display the visualization
```

#### Visualization
```
--viz-type TYPE          Force specific visualization type
                         Choices: 3d_scatter, 3d_surface, 3d_line,
                                 3d_network, 3d_bar
--source-type TYPE       Specify data source type
                         Choices: csv, json, excel, sql, api
```

#### Analysis
```
--analyze-only           Only analyze data without visualization
--suggest                Show visualization suggestions
--list-viz               List all available visualization types
```

#### Analytics
```
--analytics              Run AI-powered analytics with visualization
--analytics-only         Only run analytics without visualization
--export-analytics PATH  Export analytics report to JSON file
```

#### Batch Processing
```
--batch                  Process multiple data sources in batch mode
--batch-output-dir PATH  Output directory for batch processing
                         Default: examples/batch
```

#### Column Selection
```
--x-col NAME             X-axis column name
--y-col NAME             Y-axis column name
--z-col NAME             Z-axis column name
--color-col NAME         Color column name
--size-col NAME          Size column name
```

#### Other
```
--quiet                  Suppress verbose output
```

### Examples

```bash
# Basic visualization
python -m agentic_graphs.cli data.csv

# With analytics
python -m agentic_graphs.cli data.csv --analytics

# Analytics only
python -m agentic_graphs.cli data.csv --analytics-only

# Custom output
python -m agentic_graphs.cli data.csv -o viz.html --analytics \
  --export-analytics analytics.json

# Force visualization type
python -m agentic_graphs.cli data.csv --viz-type 3d_network

# Custom columns
python -m agentic_graphs.cli data.csv --x-col lon --y-col lat --z-col value

# Batch processing
python -m agentic_graphs.cli *.csv --batch --batch-output-dir results/
```

---

## Type Hints

The system uses Python type hints throughout:

```python
from typing import Any, Optional, Dict, List, Tuple
import pandas as pd
import plotly.graph_objects as go

# Function signatures are fully typed
def generate(
    data_source: Any,
    output_path: Optional[str] = None,
    viz_type: Optional[str] = None,
    **kwargs
) -> go.Figure:
    ...
```

---

## Error Handling

All public methods may raise:

- `FileNotFoundError`: Data source not found
- `ValueError`: Invalid parameters or data structure
- `TypeError`: Incorrect type for parameters
- `KeyError`: Required column not found
- `Exception`: General errors with descriptive messages

**Example**:
```python
try:
    fig = system.generate('data.csv')
except FileNotFoundError:
    print("Data file not found")
except ValueError as e:
    print(f"Invalid data: {e}")
except Exception as e:
    print(f"Error: {e}")
```

---

## Version Information

```python
import agentic_graphs

print(agentic_graphs.__version__)  # '1.1.0'
print(agentic_graphs.__author__)   # 'Autonomous Graph System'
```

---

**Version 1.1.0** | Complete API Reference | Built with ❤️ using Plotly, NetworkX, and Python
