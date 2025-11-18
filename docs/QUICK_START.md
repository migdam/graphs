# Quick Start Guide

Get up and running with the Autonomous 3D Graph System in 5 minutes!

---

## Installation

```bash
# Navigate to project directory
cd /path/to/graphs

# Install dependencies
pip install -r requirements.txt

# Verify installation
python test_system.py
```

Expected output: `Results: 5/5 tests passed ✓`

---

## Your First Visualization

### Option 1: One Line of Code (Easiest!)

```python
from agentic_graphs import auto_visualize

auto_visualize('data/network_sample.csv')
```

That's it! The system will:
1. ✅ Load your data
2. ✅ Analyze structure
3. ✅ Choose best visualization
4. ✅ Create interactive 3D graph
5. ✅ Display in browser

### Option 2: Command Line

```bash
python -m agentic_graphs.cli data/network_sample.csv
```

### Option 3: With More Control

```python
from agentic_graphs import AutonomousGraphSystem

system = AutonomousGraphSystem()

# Generate and save
fig = system.generate(
    'data/network_sample.csv',
    output_path='my_first_graph.html'
)
```

---

## Try Different Data Types

### Network Data

```python
# Automatic network graph
auto_visualize('data/network_sample.csv')
```

### 3D Scatter Data

```python
# Automatic 3D scatter plot
auto_visualize('data/3d_scatter_sample.csv')
```

### Surface Data

```python
# Automatic 3D surface
auto_visualize('data/surface_sample.csv')
```

---

## Add AI Analytics

### Get Insights Automatically

```python
from agentic_graphs import AutonomousGraphSystem

system = AutonomousGraphSystem()

# Visualize + Get AI insights
fig, report = system.generate_with_analytics('data/3d_scatter_sample.csv')

# View key findings
print("Key Findings:")
for finding in report.key_findings:
    print(f"  • {finding}")

# View recommendations
print("\nRecommendations:")
for rec in report.recommendations:
    print(f"  → {rec}")
```

### Analytics Only (No Visualization)

```python
# Just get analytics insights
report = system.run_analytics('data/network_sample.csv')

print(f"Patterns: {len(report.patterns)}")
print(f"Trends: {len(report.trends)}")
print(report.natural_language_summary)
```

### CLI with Analytics

```bash
# Analytics only
python -m agentic_graphs.cli data/3d_scatter_sample.csv --analytics-only

# Visualization + Analytics
python -m agentic_graphs.cli data/network_sample.csv --analytics

# Export analytics to JSON
python -m agentic_graphs.cli data/network_sample.csv --analytics-only \
  --export-analytics my_analytics.json
```

---

## Customize Your Graphs

### Specify Columns

```python
system.generate(
    'data/3d_scatter_sample.csv',
    x_col='x',
    y_col='y',
    z_col='z',
    color_col='category',
    title='My Custom Graph'
)
```

### Force Visualization Type

```python
# Force 3D scatter even if system suggests something else
system.generate(
    'data/surface_sample.csv',
    viz_type='3d_scatter'
)
```

### Save Without Displaying

```python
system.generate(
    'data/network_sample.csv',
    output_path='graph.html',
    show=False  # Don't open browser
)
```

---

## Work with Your Own Data

### CSV Files

```python
# Just provide the path
auto_visualize('path/to/your/data.csv')
```

### JSON Data

```python
auto_visualize('path/to/your/data.json')

# Or JSON string
import json
data = {'x': [1,2,3], 'y': [4,5,6], 'z': [7,8,9]}
auto_visualize(json.dumps(data), source_type='json')
```

### Excel Files

```python
auto_visualize('path/to/your/data.xlsx')
```

### SQL Database

```python
auto_visualize(
    'SELECT * FROM my_table',
    source_type='sql',
    connection_string='sqlite:///database.db'
)
```

### Pandas DataFrame

```python
import pandas as pd

df = pd.read_csv('your_data.csv')
auto_visualize(df)
```

---

## Batch Process Multiple Files

```python
system = AutonomousGraphSystem()

results = system.batch_generate([
    'file1.csv',
    'file2.json',
    'file3.xlsx'
], output_dir='batch_results/')

print(f"Generated {len(results)} visualizations")
```

---

## Understanding Output

### Visualization Files

The system creates interactive HTML files:
- Rotate: Click and drag
- Zoom: Scroll wheel
- Pan: Shift + drag
- Hover: See data points
- Export: Built-in export to PNG

### Analytics Reports

JSON structure:
```json
{
  "timestamp": "2025-11-16T...",
  "data_summary": {
    "total_records": 15,
    "total_columns": 6,
    ...
  },
  "insights": [...],
  "key_findings": [...],
  "recommendations": [...]
}
```

---

## Next Steps

### Run Examples

```bash
# Basic examples
python examples/example_basic.py

# Advanced examples
python examples/example_advanced.py

# Analytics demo
python examples/analytics_demo.py

# Full showcase
python showcase.py
```

### Run Tests

```bash
# Basic tests
python test_system.py

# Comprehensive tests
python deep_test.py

# Analytics tests
python test_analytics.py
```

### Explore Documentation

1. **[User Guide](USER_GUIDE.md)** - Complete feature documentation
2. **[API Reference](API_REFERENCE.md)** - Detailed API documentation
3. **[Architecture](ARCHITECTURE.md)** - System internals
4. **[README](../README.md)** - Project overview

---

## Common Patterns

### Pattern 1: Quick Exploration

```python
# Load and visualize in one line
auto_visualize('data.csv')
```

### Pattern 2: Analysis First

```python
system = AutonomousGraphSystem()

# Analyze to see what you have
profile = system.analyze('data.csv')
print(f"Suggested: {profile.suggested_visualizations}")

# Then generate
system.generate('data.csv')
```

### Pattern 3: Custom with Analytics

```python
# Get full control + insights
fig, report = system.generate_with_analytics(
    'data.csv',
    viz_type='3d_scatter',
    x_col='dimension1',
    color_col='category',
    title='Analysis Results'
)

# Use both outputs
fig.show()
for rec in report.recommendations:
    print(rec)
```

### Pattern 4: Production Pipeline

```python
import pandas as pd
from agentic_graphs import AutonomousGraphSystem

# Setup
system = AutonomousGraphSystem(verbose=False)

# Load data
df = pd.read_csv('production_data.csv')

# Get insights
report = system.run_analytics(df, export_path='report.json')

# Create visualization
fig = system.generate(
    df,
    output_path='dashboard.html',
    show=False
)

# Send to users/dashboard
print("Visualization ready: dashboard.html")
print(f"Insights: {len(report.key_findings)}")
```

---

## Troubleshooting Quick Fixes

### Can't find data file?

```python
# Use absolute path
import os
data_path = os.path.abspath('data/network_sample.csv')
auto_visualize(data_path)
```

### Wrong visualization chosen?

```python
# Override the decision
system.generate('data.csv', viz_type='3d_scatter')
```

### Want to see what's happening?

```python
# Enable verbose mode
system = AutonomousGraphSystem(verbose=True)
```

### Memory issues?

```python
# Sample your data first
df = pd.read_csv('large_file.csv')
df_sample = df.sample(n=1000)
auto_visualize(df_sample)
```

---

## Get Help

- **Run examples**: `python examples/example_basic.py`
- **Check tests**: `python test_system.py`
- **Read docs**: See `docs/` directory
- **Error messages**: Usually include helpful suggestions

---

## What's Next?

Once you're comfortable with the basics:

1. **Explore all 5 visualization types**
2. **Try the AI analytics features**
3. **Batch process multiple datasets**
4. **Customize visualizations**
5. **Integrate into your workflow**

---

**Ready to create amazing 3D visualizations? Start with**:

```python
from agentic_graphs import auto_visualize
auto_visualize('data/network_sample.csv')
```

**That's it!** 🚀

---

**Version 1.1.0** | Quick Start Guide | Built with ❤️ using Plotly, NetworkX, and Python
