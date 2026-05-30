# 🤖 Autonomous 3D Graph Generation System

**Version 1.1.0** - Now with AI-Powered Analytics!

A fully autonomous system that creates **beautiful 3D visualizations** from any data source. Simply provide your data, and the AI-powered agent analyzes it, determines the best visualization approach, generates stunning interactive 3D graphs, and provides intelligent insights.

## ✨ Key Features

- **🧠 Fully Autonomous**: Automatically analyzes data and selects the best visualization
- **📊 Multiple Data Sources**: CSV, JSON, Excel, SQL databases, REST APIs, pandas DataFrames
- **🎨 Beautiful 3D Visualizations**: Network graphs, scatter plots, surfaces, lines, bars, and meshes
- **🤖 AI-Powered Analytics**: Automatic insight extraction, pattern detection, trend analysis
- **🔍 Intelligent Analysis**: Detects patterns, relationships, and data characteristics
- **⚡ Easy to Use**: One-line command to visualize any data
- **🎯 Customizable**: Override autonomous decisions when needed
- **📦 Batch Processing**: Process multiple datasets automatically
- **💡 Actionable Recommendations**: Get data-driven suggestions

## 🚀 Quick Start

### Installation

```bash
# Option 1: install dependencies only
pip install -r requirements.txt

# Option 2: install as a package (provides the `agentic-graphs` CLI command)
pip install -e .

# Optional extras for Excel, SQL, and static image export
pip install -e ".[all]"
```

Once installed as a package you can use the `agentic-graphs` command directly:

```bash
agentic-graphs data.csv --analytics
```

### Simplest Usage

```python
from agentic_graphs import auto_visualize

# That's it! The system does everything automatically
auto_visualize('data.csv')
```

### With AI Analytics (NEW!)

```python
from agentic_graphs import AutonomousGraphSystem

system = AutonomousGraphSystem()

# Get visualization + AI insights
fig, report = system.generate_with_analytics('data.csv')

# View insights
print(report.key_findings)
print(report.recommendations)
```

### Command Line

```bash
# Automatically analyze and visualize
python -m agentic_graphs.cli data.csv

# With AI analytics
python -m agentic_graphs.cli data.csv --analytics

# Analytics only
python -m agentic_graphs.cli data.csv --analytics-only

# Save to file
python -m agentic_graphs.cli data.csv -o my_visualization.html

# Force specific visualization type
python -m agentic_graphs.cli data.csv --viz-type 3d_network

# Batch process multiple files
python -m agentic_graphs.cli file1.csv file2.json file3.xlsx --batch
```

## 📚 Documentation

Comprehensive documentation is available:

- **[Quick Start Guide](docs/QUICK_START.md)** - Get started in 5 minutes
- **[User Guide](docs/USER_GUIDE.md)** - Complete feature documentation
- **[API Reference](docs/API_REFERENCE.md)** - Detailed API documentation
- **[Architecture](docs/ARCHITECTURE.md)** - System internals and design
- **[Testing Report](TESTING_REPORT.md)** - Comprehensive test results

## 📁 Project Structure

```
graphs/
├── agentic_graphs/           # 🤖 Autonomous 3D graph system
│   ├── agent_core.py         #    Autonomous decision-making agent
│   ├── data_connectors.py    #    Multi-source data loaders
│   ├── visualizers_3d.py     #    3D visualization engines
│   ├── ai_analytics.py       #    AI-powered analytics engine (NEW!)
│   ├── autonomous_system.py  #    Main orchestrator
│   └── cli.py                #    Command-line interface
├── docs/                      # 📚 Comprehensive documentation
│   ├── QUICK_START.md        #    5-minute quick start
│   ├── USER_GUIDE.md         #    Complete user guide
│   ├── API_REFERENCE.md      #    Detailed API docs
│   └── ARCHITECTURE.md       #    System architecture
├── examples/                  # Example scripts and outputs
│   ├── example_basic.py      #    Basic usage examples
│   ├── example_advanced.py   #    Advanced features
│   └── analytics_demo.py     #    AI analytics demos (NEW!)
├── data/                      # Sample datasets
│   ├── sample_data.csv
│   ├── network_sample.csv
│   ├── 3d_scatter_sample.csv
│   └── surface_sample.csv
├── scripts/                   # Legacy 2D visualization scripts
│   ├── line_chart.py
│   ├── bar_chart.py
│   └── heatmap.py
├── test_system.py            # Basic test suite
├── deep_test.py              # Comprehensive tests
├── test_analytics.py         # Analytics tests (NEW!)
├── README.md                 # This file
├── TESTING_REPORT.md         # Test results
└── requirements.txt          # Dependencies
```

## 🎨 Available 3D Visualizations

The system can automatically choose from:

- **3D Network Graphs** - Visualize relationships and connections
- **3D Scatter Plots** - Explore multi-dimensional data
- **3D Surface Plots** - Visualize continuous functions
- **3D Line Plots** - Track temporal or sequential data
- **3D Bar Charts** - Compare categorical data

## 💡 Usage Examples

### Example 1: Basic Autonomous Usage

```python
from agentic_graphs import auto_visualize

# The system automatically:
# 1. Loads the data
# 2. Analyzes structure and content
# 3. Selects best visualization
# 4. Generates beautiful 3D graph
auto_visualize('network_data.csv')
```

### Example 2: Advanced Control

```python
from agentic_graphs import AutonomousGraphSystem

system = AutonomousGraphSystem()

# Analyze data first
profile = system.analyze('data.csv')
print(f"Recommended: {profile.suggested_visualizations}")

# Generate with custom parameters
system.generate(
    'data.csv',
    viz_type='3d_scatter',
    x_col='dimension1',
    y_col='dimension2',
    z_col='dimension3',
    color_col='category',
    output_path='output.html',
    title='My Custom Visualization'
)
```

### Example 3: Multiple Data Sources

```python
from agentic_graphs import auto_visualize

# From CSV
auto_visualize('data.csv')

# From JSON
auto_visualize('data.json')

# From API
auto_visualize('https://api.example.com/data', source_type='api')

# From SQL
auto_visualize('SELECT * FROM table', source_type='sql',
               connection_string='sqlite:///mydb.db')

# From DataFrame
import pandas as pd
df = pd.DataFrame({'x': [1,2,3], 'y': [4,5,6], 'z': [7,8,9]})
auto_visualize(df)
```

### Example 4: Batch Processing

```python
from agentic_graphs import AutonomousGraphSystem

system = AutonomousGraphSystem()

# Process multiple files autonomously
results = system.batch_generate([
    'sales_data.csv',
    'network_data.json',
    'sensor_data.xlsx'
], output_dir='visualizations/')
```

## 🧠 How It Works

The autonomous system follows this intelligent workflow:

1. **Data Loading** 🔄
   - Automatically detects data source type (CSV, JSON, API, etc.)
   - Loads and parses data into a unified format

2. **Data Analysis** 🔍
   - Identifies column types (numeric, categorical, temporal)
   - Detects patterns (networks, correlations, trends)
   - Analyzes data structure and relationships

3. **Autonomous Decision** 🎯
   - Evaluates all available visualization types
   - Calculates confidence scores for each option
   - Selects the optimal visualization

4. **Visualization Generation** 🎨
   - Creates beautiful, interactive 3D graph
   - Applies intelligent defaults for colors, sizing, layouts
   - Generates publication-ready output

## 📋 CLI Reference

```bash
# Basic usage
python -m agentic_graphs.cli <data_source> [options]

# Options:
  -o, --output PATH          Output file path
  --viz-type TYPE            Force specific visualization
  --source-type TYPE         Specify data source type
  --title TEXT               Custom title
  --no-show                  Don't display (only save)
  --analyze-only             Only analyze, don't visualize
  --suggest                  Show suggestions without generating
  --batch                    Batch process multiple files
  --list-viz                 List available visualizations
  --quiet                    Suppress verbose output

# Column selection:
  --x-col NAME               X-axis column
  --y-col NAME               Y-axis column
  --z-col NAME               Z-axis column
  --color-col NAME           Color column
  --size-col NAME            Size column
```

## 🎓 Examples Directory

Run the example scripts to see the system in action:

```bash
# Basic examples
python examples/example_basic.py

# Advanced features
python examples/example_advanced.py
```

## 🔧 Legacy 2D Visualizations

The repository also includes legacy 2D visualization scripts:

```bash
python scripts/line_chart.py --data data/sample_data.csv
python scripts/bar_chart.py --data data/sample_data.csv
python scripts/heatmap.py --data data/sample_data.csv
```

## 🤝 Contributing

This is an autonomous system that continuously learns and improves. Contributions welcome!

## 📄 License

MIT License - Feel free to use and modify

---

**Built with ❤️ using Plotly, NetworkX, and Python**