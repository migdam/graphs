# Autonomous 3D Graph System - User Guide

**Version 1.1.0**

Welcome to the comprehensive user guide for the Autonomous 3D Graph Generation System with AI Analytics.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Core Concepts](#core-concepts)
5. [Data Sources](#data-sources)
6. [Visualizations](#visualizations)
7. [AI Analytics](#ai-analytics)
8. [Advanced Usage](#advanced-usage)
9. [CLI Reference](#cli-reference)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

---

## Introduction

The Autonomous 3D Graph System is an intelligent visualization platform that:

- **Analyzes** your data automatically
- **Selects** the best 3D visualization approach
- **Generates** beautiful, interactive graphs
- **Extracts** AI-powered insights and patterns
- **Recommends** actions based on data analysis

### Key Features

✨ **Fully Autonomous** - Minimal configuration required
🎨 **Beautiful 3D Graphics** - Interactive visualizations using Plotly
🧠 **AI-Powered Analytics** - Automatic insight extraction
📊 **Multiple Data Sources** - CSV, JSON, Excel, SQL, APIs, DataFrames
🚀 **Production Ready** - Tested and validated

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
# Clone or navigate to the project directory
cd /path/to/graphs

# Install required packages
pip install -r requirements.txt
```

### Verify Installation

```bash
# Test the system
python test_system.py

# Should output: All tests passed
```

---

## Quick Start

### 1. One-Line Visualization

The simplest way to use the system:

```python
from agentic_graphs import auto_visualize

auto_visualize('data.csv')
```

This single line:
- Loads your data
- Analyzes structure
- Selects best visualization
- Creates interactive 3D graph
- Displays the result

### 2. With AI Analytics

Get insights along with visualization:

```python
from agentic_graphs import AutonomousGraphSystem

system = AutonomousGraphSystem()
fig, report = system.generate_with_analytics('data.csv')

# View insights
print(report.key_findings)
```

### 3. CLI Usage

```bash
# Analyze and visualize
python -m agentic_graphs.cli data.csv

# With AI analytics
python -m agentic_graphs.cli data.csv --analytics

# Save to file
python -m agentic_graphs.cli data.csv -o output.html
```

---

## Core Concepts

### The Autonomous Agent

The system uses an AI agent that makes intelligent decisions:

1. **Data Profiling** - Analyzes your data structure
2. **Pattern Recognition** - Identifies data characteristics
3. **Visualization Selection** - Chooses optimal graph type
4. **Parameter Optimization** - Selects best columns and settings

### Confidence Scores

Every decision has a confidence score (0-100%):

- **90-100%**: Highly confident (e.g., network detection)
- **70-89%**: Confident (e.g., scatter plot for numeric data)
- **50-69%**: Moderate confidence (fallback options)

### Data Profile

The agent creates a comprehensive data profile:

```python
from agentic_graphs import analyze_data

profile = analyze_data('data.csv')

print(f"Rows: {profile.num_rows}")
print(f"Columns: {profile.num_columns}")
print(f"Has network: {profile.has_network_structure}")
print(f"Recommended: {profile.suggested_visualizations[0]}")
print(f"Confidence: {profile.confidence_scores}")
```

---

## Data Sources

### Supported Formats

The system automatically detects and loads from:

#### 1. CSV Files

```python
auto_visualize('data.csv')
```

#### 2. JSON Files/Strings

```python
# From file
auto_visualize('data.json')

# From string
import json
data = {'x': [1,2,3], 'y': [4,5,6], 'z': [7,8,9]}
auto_visualize(json.dumps(data), source_type='json')
```

#### 3. Excel Files

```python
auto_visualize('data.xlsx')

# Specify sheet
system.generate('data.xlsx', sheet_name='Sheet2')
```

#### 4. SQL Databases

```python
# SQLite
auto_visualize(
    'SELECT * FROM table',
    source_type='sql',
    connection_string='sqlite:///database.db'
)

# PostgreSQL
auto_visualize(
    'SELECT * FROM users',
    source_type='sql',
    connection_string='postgresql://user:pass@localhost/db'
)
```

#### 5. REST APIs

```python
auto_visualize(
    'https://api.example.com/data',
    source_type='api',
    headers={'Authorization': 'Bearer token'}
)
```

#### 6. Pandas DataFrames

```python
import pandas as pd

df = pd.read_csv('data.csv')
auto_visualize(df)
```

### Data Format Requirements

#### For Network Graphs

Must have source-target columns:

```csv
source,target,weight
Alice,Bob,5
Bob,Charlie,3
```

Column names can include: `source`, `target`, `from`, `to`, `node1`, `node2`

#### For 3D Scatter

At least 3 numeric columns:

```csv
x,y,z,value,category
1.2,2.3,3.4,10,A
2.1,3.2,4.1,15,B
```

#### For Surface Plots

Continuous numeric data:

```csv
x,y,z
0,0,0.5
0,1,1.2
1,0,2.1
```

---

## Visualizations

### Available Types

#### 1. 3D Network Graph

**Best for**: Relationships, connections, social networks, dependencies

**Auto-detected when**: Data has source-target columns

```python
# Automatic
auto_visualize('network_data.csv')

# Explicit
system.generate('network_data.csv', viz_type='3d_network')
```

**Features**:
- Interactive node exploration
- Edge weight visualization
- Hub detection
- Network density calculation

#### 2. 3D Scatter Plot

**Best for**: Multi-dimensional numeric data, clustering, distributions

**Auto-detected when**: 3+ numeric columns present

```python
system.generate(
    'data.csv',
    viz_type='3d_scatter',
    x_col='dimension1',
    y_col='dimension2',
    z_col='dimension3',
    color_col='category',
    size_col='value'
)
```

**Features**:
- Color encoding by category
- Size encoding by value
- Hover information
- 3D rotation and zoom

#### 3. 3D Surface Plot

**Best for**: Continuous functions, heat maps, terrain data

**Auto-detected when**: Suitable numeric grid structure

```python
auto_visualize('surface_data.csv', viz_type='3d_surface')
```

**Features**:
- Smooth surface interpolation
- Color gradient mapping
- Contour lines
- Interactive rotation

#### 4. 3D Line Plot

**Best for**: Temporal data, trajectories, time series

**Auto-detected when**: Temporal columns detected

```python
system.generate('timeseries.csv', viz_type='3d_line')
```

**Features**:
- Multi-line support
- Temporal tracking
- Trend visualization

#### 5. 3D Bar Chart

**Best for**: Categorical comparisons, grouped data

**Auto-detected when**: Categorical + numeric columns

```python
auto_visualize('categories.csv', viz_type='3d_bar')
```

**Features**:
- 3D bar rendering
- Category grouping
- Value comparisons

### Customization Options

#### Colors

```python
system.generate(
    'data.csv',
    color_col='category',  # Color by column
    colorscale='Viridis'   # Color scheme
)
```

#### Sizing

```python
system.generate(
    'data.csv',
    size_col='value',  # Size by column
)
```

#### Layout (for networks)

```python
system.generate(
    'network.csv',
    viz_type='3d_network',
    layout='spring'  # 'spring', 'kamada_kawai', 'circular'
)
```

#### Titles and Labels

```python
system.generate(
    'data.csv',
    title='My Custom Visualization',
    x_col='dimension_x',
    y_col='dimension_y',
    z_col='dimension_z'
)
```

---

## AI Analytics

### Overview

The AI Analytics Engine automatically extracts insights from your data.

### Features

🔍 **Pattern Detection**
- Cluster identification
- Multimodal distributions
- Data groupings

📊 **Statistical Analysis**
- Distribution skewness
- Outlier detection (IQR method)
- Variability analysis

📈 **Trend Analysis**
- Correlation detection
- Linear trends
- Monotonic patterns

⚠️ **Anomaly Detection**
- Statistical outliers
- Unusual patterns
- Data quality issues

🔗 **Relationship Analysis**
- Variable correlations
- Categorical influences
- Dependency detection

### Usage

#### Analytics Only

```python
from agentic_graphs import AutonomousGraphSystem

system = AutonomousGraphSystem()
report = system.run_analytics('data.csv')

# View insights
print(f"Total insights: {len(report.insights)}")
print(f"Key findings: {report.key_findings}")
print(f"Recommendations: {report.recommendations}")
```

#### Visualization + Analytics

```python
# Get both visualization and analytics
fig, report = system.generate_with_analytics('data.csv')

# Access insights
for insight in report.insights:
    print(f"{insight.title} ({insight.confidence:.0%})")
    print(f"  {insight.description}")
    print(f"  Recommendation: {insight.recommendation}")
```

#### Export Analytics

```python
# Export to JSON
report = system.run_analytics(
    'data.csv',
    export_path='analytics_report.json'
)

# Auto-export with visualization
fig, report = system.generate_with_analytics(
    'data.csv',
    output_path='viz.html',
    analytics_path='analytics.json'
)
```

### Analytics Report Structure

```python
report.timestamp              # When generated
report.data_summary          # Statistics (rows, cols, types)
report.insights              # List of GraphInsight objects
report.patterns              # Detected patterns
report.anomalies             # Detected anomalies
report.trends                # Identified trends
report.recommendations       # Action items
report.natural_language_summary  # Human-readable summary
report.key_findings          # Top 5 insights
```

### Insight Categories

Each insight has a category:

- **pattern**: Data structure patterns
- **anomaly**: Outliers and unusual values
- **trend**: Correlations and trends
- **relationship**: Variable dependencies
- **statistical**: Statistical properties

### Confidence Levels

Analytics provides confidence scores:

```python
for insight in report.insights:
    if insight.confidence > 0.8:
        print(f"High confidence: {insight.title}")
    elif insight.confidence > 0.6:
        print(f"Moderate confidence: {insight.title}")
```

### Network-Specific Analytics

For network data, get additional insights:

```python
report = system.run_analytics('network.csv')

# Network metrics in insights
# - Network density
# - Hub nodes
# - Average degree
# - Clustering patterns
```

---

## Advanced Usage

### Batch Processing

Process multiple datasets:

```python
system = AutonomousGraphSystem()

results = system.batch_generate([
    'dataset1.csv',
    'dataset2.json',
    'dataset3.xlsx'
], output_dir='batch_output/')

# Check results
for name, fig in results.items():
    if fig:
        print(f"✓ {name}")
    else:
        print(f"✗ {name} failed")
```

### Custom Analysis Pipeline

```python
# 1. Load data
from agentic_graphs import load_data
df = load_data('data.csv')

# 2. Profile data
from agentic_graphs import AutonomousGraphAgent
agent = AutonomousGraphAgent()
profile = agent.analyze_data(df)

# 3. Run analytics
from agentic_graphs import AIGraphAnalytics
analytics = AIGraphAnalytics()
report = analytics.analyze(df, '3d_scatter', profile)

# 4. Create visualization
from agentic_graphs import VisualizerFactory
viz = VisualizerFactory.create('3d_scatter')
fig = viz.create(df, output_path='output.html')
```

### Programmatic Control

```python
system = AutonomousGraphSystem(verbose=False)

# Analyze first
profile = system.analyze('data.csv')

# Get suggestions
suggestions = system.suggest_visualizations('data.csv')

# Choose based on confidence
viz_type, confidence = suggestions[0]

if confidence > 0.8:
    # Generate with high-confidence choice
    fig = system.generate('data.csv', viz_type=viz_type)
else:
    # Manual override
    fig = system.generate('data.csv', viz_type='3d_scatter')
```

### Error Handling

```python
try:
    fig = system.generate('data.csv')
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Invalid data: {e}")
except Exception as e:
    print(f"Error: {e}")
```

### Performance Optimization

For large datasets:

```python
# Sample data first
import pandas as pd
df = pd.read_csv('large_data.csv')
df_sample = df.sample(n=1000, random_state=42)

# Visualize sample
auto_visualize(df_sample)
```

---

## CLI Reference

### Basic Commands

```bash
# Visualize data
python -m agentic_graphs.cli data.csv

# With output file
python -m agentic_graphs.cli data.csv -o output.html

# Force visualization type
python -m agentic_graphs.cli data.csv --viz-type 3d_network

# Quiet mode
python -m agentic_graphs.cli data.csv --quiet
```

### Analysis Commands

```bash
# Analyze only (no visualization)
python -m agentic_graphs.cli data.csv --analyze-only

# Get suggestions
python -m agentic_graphs.cli data.csv --suggest

# List available visualizations
python -m agentic_graphs.cli --list-viz
```

### Analytics Commands

```bash
# Run analytics only
python -m agentic_graphs.cli data.csv --analytics-only

# Visualization + analytics
python -m agentic_graphs.cli data.csv --analytics

# Export analytics to JSON
python -m agentic_graphs.cli data.csv --analytics-only \
  --export-analytics report.json
```

### Customization

```bash
# Custom title
python -m agentic_graphs.cli data.csv --title "My Graph"

# Specify columns
python -m agentic_graphs.cli data.csv \
  --x-col dimension1 \
  --y-col dimension2 \
  --z-col dimension3 \
  --color-col category

# Don't display (save only)
python -m agentic_graphs.cli data.csv -o output.html --no-show
```

### Batch Processing

```bash
# Process multiple files
python -m agentic_graphs.cli file1.csv file2.json file3.xlsx --batch

# Specify output directory
python -m agentic_graphs.cli *.csv --batch \
  --batch-output-dir results/
```

---

## Best Practices

### Data Preparation

✅ **DO**:
- Use descriptive column names
- Remove duplicate rows
- Handle missing values appropriately
- Use consistent data types

❌ **DON'T**:
- Mix data types in columns
- Use special characters in column names
- Leave large amounts of missing data
- Mix delimiters in CSV files

### Visualization Selection

- **Network data**: Use clear source/target column names
- **Numeric data**: Ensure 3+ dimensions for 3D plots
- **Temporal data**: Use proper date formats
- **Categorical data**: Limit categories to <20 for clarity

### Performance

For datasets with:
- **< 1,000 rows**: Full dataset visualization works well
- **1,000-10,000 rows**: Consider sampling for interactivity
- **> 10,000 rows**: Definitely sample or aggregate first

### Analytics Usage

- Review confidence scores before acting on insights
- Cross-reference high-confidence insights with domain knowledge
- Use recommendations as starting points, not absolutes
- Export analytics for reproducibility

---

## Troubleshooting

### Common Issues

#### "No module named 'agentic_graphs'"

```bash
# Ensure you're in the correct directory
cd /path/to/graphs

# Or add to Python path
export PYTHONPATH="/path/to/graphs:$PYTHONPATH"
```

#### "Could not auto-detect source type"

```python
# Specify explicitly
auto_visualize('data.txt', source_type='csv')
```

#### "No visualization suggested"

Your data might not match any pattern. Try:

```python
# Force a visualization type
system.generate('data.csv', viz_type='3d_scatter')
```

#### Visualization not displaying

```python
# Ensure show=True (default)
system.generate('data.csv', show=True)

# Or open HTML file manually
system.generate('data.csv', output_path='viz.html')
# Then open viz.html in browser
```

#### Memory issues with large datasets

```python
# Sample the data
import pandas as pd
df = pd.read_csv('large.csv')
df_sample = df.sample(n=5000)
auto_visualize(df_sample)
```

### Getting Help

1. Check documentation: `docs/`
2. Run tests: `python test_system.py`
3. View examples: `examples/`
4. Check error messages for details

---

## Next Steps

- Try the [examples](../examples/)
- Run the [deep tests](../deep_test.py)
- Explore the [showcase](../showcase.py)
- Check the [API Reference](API_REFERENCE.md)

---

**Version 1.1.0** | Built with ❤️ using Plotly, NetworkX, and Python
