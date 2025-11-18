# Graphs Visualization Repository

A comprehensive Python toolkit for creating beautiful and informative data visualizations. This repository provides 12+ chart types, utilities for data processing, and a powerful CLI for quick visualization generation.

## Features

- **12+ Chart Types**: Line, Bar, Scatter, Pie, Area, Box, Violin, Histogram, Bubble, Radar, Heatmap, and 3D Surface plots
- **Unified CLI**: Generate any chart type with a single command
- **Configurable**: YAML-based configuration for customizing all visualizations
- **Color Schemes**: Multiple built-in color palettes (default, professional, vibrant, pastel, dark)
- **Data Utilities**: Built-in data validation, preprocessing, and cleaning functions
- **Multi-Format Export**: Save visualizations as PNG, SVG, or PDF
- **Unit Tests**: Comprehensive test suite for reliability
- **Modular Design**: Easy to extend with new chart types

## Structure

```
graphs/
├── scripts/           # Individual visualization scripts
│   ├── line_chart.py
│   ├── bar_chart.py
│   ├── scatter_plot.py
│   ├── pie_chart.py
│   ├── area_chart.py
│   ├── box_plot.py
│   ├── violin_plot.py
│   ├── histogram.py
│   ├── bubble_chart.py
│   ├── radar_chart.py
│   ├── heatmap.py
│   ├── surface_3d.py
│   ├── utils.py            # Utility functions
│   ├── color_schemes.py    # Color palette management
│   └── config_loader.py    # Configuration loader
├── data/              # Sample datasets
├── examples/          # Generated visualizations
├── tests/             # Unit tests
├── visualize.py       # Main CLI tool
├── config.yaml        # Configuration file
└── requirements.txt   # Python dependencies
```

## Getting Started

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd graphs
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation by running tests:
   ```bash
   python -m unittest discover tests
   ```

## Usage

### Quick Start - Using the CLI

The easiest way to generate visualizations is using the unified CLI tool:

```bash
# Generate a single chart type
python visualize.py --type line --data data/sample_data.csv

# Generate a specific output path
python visualize.py --type bar --data data/sample_data.csv --output my_chart.png

# Generate ALL chart types at once
python visualize.py --all --data data/sample_data.csv
```

### Individual Scripts

Each visualization type can also be run independently:

```bash
# Line chart
python scripts/line_chart.py --data data/sample_data.csv --output examples/line.png

# Bar chart
python scripts/bar_chart.py --data data/sample_data.csv --output examples/bar.png

# Scatter plot
python scripts/scatter_plot.py --data data/sample_data.csv

# And so on...
```

## Chart Types

### 1. Line Chart
Perfect for showing trends over time.
```bash
python visualize.py --type line --data data/sample_data.csv
```

### 2. Bar Chart
Ideal for comparing values across categories.
```bash
python visualize.py --type bar --data data/sample_data.csv
```

### 3. Scatter Plot
Shows relationships between variables.
```bash
python visualize.py --type scatter --data data/sample_data.csv
```

### 4. Pie Chart
Displays proportions and percentages.
```bash
python visualize.py --type pie --data data/sample_data.csv
```

### 5. Area Chart
Shows cumulative data over time.
```bash
python visualize.py --type area --data data/sample_data.csv
```

### 6. Box Plot
Visualizes statistical distributions.
```bash
python visualize.py --type box --data data/sample_data.csv
```

### 7. Violin Plot
Combines box plot with kernel density estimation.
```bash
python visualize.py --type violin --data data/sample_data.csv
```

### 8. Histogram
Shows frequency distributions.
```bash
python visualize.py --type histogram --data data/sample_data.csv
```

### 9. Bubble Chart
3-dimensional scatter plot with size encoding.
```bash
python visualize.py --type bubble --data data/sample_data.csv
```

### 10. Radar Chart
Compares multiple variables in a circular layout.
```bash
python visualize.py --type radar --data data/sample_data.csv
```

### 11. Heatmap
Displays data density using colors.
```bash
python visualize.py --type heatmap --data data/sample_data.csv
```

### 12. 3D Surface Plot
Creates three-dimensional surface visualizations.
```bash
python visualize.py --type 3d --data data/sample_data.csv
```

## Configuration

Customize visualizations by editing `config.yaml`:

```yaml
visualization:
  default_style: "whitegrid"
  color_scheme: "default"  # Options: default, professional, vibrant, pastel, dark
  figure_size:
    width: 10
    height: 6

output:
  default_format: "png"
  dpi: 300
  formats:
    - png
    - svg
    - pdf
```

## Utilities

### Data Validation
```python
from scripts.utils import validate_data

df = pd.read_csv('data.csv')
validate_data(df, required_columns=['date', 'category', 'value'])
```

### Data Preprocessing
```python
from scripts.utils import preprocess_data

cleaned_df = preprocess_data(df, fill_na=True, remove_duplicates=True)
```

### Multi-Format Export
```python
from scripts.utils import save_figure

save_figure(fig, 'output/chart.png', dpi=300, formats=['png', 'svg', 'pdf'])
```

### Color Schemes
```python
from scripts.color_schemes import apply_style, get_palette

apply_style('professional')  # Apply professional color scheme
colors = get_palette('vibrant', 'categorical', n_colors=5)
```

## Data Format

Input CSV files should have the following structure:

```csv
date,category,value
2024-01-01,A,45
2024-01-01,B,67
2024-01-02,A,52
```

Required columns:
- `date`: Date or time identifier
- `category`: Category label
- `value`: Numeric value to visualize

## Testing

Run the test suite:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_utils
python -m unittest tests.test_visualizations
```

## Examples

After running the CLI with `--all`, you'll find example visualizations in the `examples/` directory:

- `line_chart.png` - Trend analysis
- `bar_chart.png` - Category comparison
- `scatter_plot.png` - Data point distribution
- `pie_chart.png` - Proportional breakdown
- And more...

## Advanced Usage

### Custom Python Integration

```python
import sys
sys.path.insert(0, 'scripts')

from line_chart import create_line_chart
from color_schemes import apply_style
from config_loader import ConfigLoader

# Load configuration
config = ConfigLoader('config.yaml')

# Apply custom style
apply_style('professional')

# Generate chart
create_line_chart('data/mydata.csv', 'output/mychart.png')
```

### Batch Processing

```python
import os
from glob import glob

data_files = glob('data/*.csv')
for data_file in data_files:
    name = os.path.basename(data_file).replace('.csv', '')
    create_line_chart(data_file, f'output/{name}_line.png')
```

## Requirements

- Python 3.7+
- matplotlib >= 3.5.0
- numpy >= 1.20.0
- pandas >= 1.3.0
- seaborn >= 0.11.0
- plotly >= 5.3.0
- pyyaml >= 6.0

## Contributing

Contributions are welcome! To add a new chart type:

1. Create a new script in `scripts/` following the existing pattern
2. Add the chart function to `visualize.py`
3. Update this README with usage examples
4. Add unit tests in `tests/`

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on the repository.