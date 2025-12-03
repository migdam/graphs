# Excel Integration Guide

## Overview

The graphs repository now supports Excel files (.xlsx, .xls, .xlsm) as input data sources. You can generate any visualization directly from Excel files without manual conversion to CSV.

## Features

- ✅ Read Excel files (.xlsx, .xls, .xlsm, .xlsb)
- ✅ Support for multiple sheets
- ✅ List sheets in Excel files
- ✅ Convert Excel to CSV
- ✅ Get Excel file information
- ✅ Validate Excel files
- ✅ Universal chart generator from Excel

## Quick Start

### 1. Generate Chart from Excel File

```bash
# Generate a line chart from Excel
python scripts/chart_from_excel.py line data/sample_data.xlsx

# Generate from specific sheet
python scripts/chart_from_excel.py bar data/quarterly_report.xlsx --sheet Q1

# Generate Gantt chart from Excel
python scripts/chart_from_excel.py gantt data/project_timeline.xlsx
```

### 2. List Sheets in Excel File

```bash
python scripts/chart_from_excel.py line data/sample_data.xlsx --list-sheets

# Or use the utility directly
python scripts/excel_utils.py list data/quarterly_report.xlsx
```

### 3. Get Excel File Information

```bash
python scripts/excel_utils.py info data/sample_data.xlsx
```

Output:
```
File: data/sample_data.xlsx
Size: 5,696 bytes
Sheets: 2

  Sheet: Sales
  Columns (3): date, category, value

  Sheet: Costs
  Columns (3): date, category, value
```

### 4. Convert Excel to CSV

```bash
# Convert first sheet
python scripts/excel_utils.py convert data/sample_data.xlsx data/output.csv

# Convert specific sheet
python scripts/excel_utils.py convert data/quarterly_report.xlsx data/q1.csv --sheet Q1
```

## Using Excel Files with Chart Scripts

### Method 1: Universal Chart Generator (Recommended)

```bash
# Syntax
python scripts/chart_from_excel.py CHART_TYPE EXCEL_FILE [OPTIONS]

# Examples
python scripts/chart_from_excel.py line data/sales.xlsx
python scripts/chart_from_excel.py bar data/revenue.xlsx --sheet "2024 Data"
python scripts/chart_from_excel.py scatter data/correlation.xlsx --x column1 --y column2
python scripts/chart_from_excel.py pie data/market_share.xlsx --donut
python scripts/chart_from_excel.py gantt data/project.xlsx --output reports/timeline.pdf
```

### Method 2: Manual Conversion

```bash
# Convert Excel to CSV first
python scripts/excel_utils.py convert data/sales.xlsx data/sales.csv

# Then use any chart script
python scripts/line_chart.py --data data/sales.csv
```

### Method 3: Python API

```python
from scripts.excel_utils import read_excel, write_excel

# Read Excel file
df = read_excel('data/sales.xlsx', sheet_name='Q1')

# Process data
# ... your processing here ...

# Write to Excel
write_excel(df, 'output/results.xlsx', sheet_name='Results')
```

## Excel File Examples

### Sample Excel Files Included

1. **sample_data.xlsx** - Sales and costs data
   - Sheets: Sales, Costs
   - Columns: date, category, value

2. **project_timeline.xlsx** - Project tasks
   - Columns: task, start_date, end_date, progress, owner

3. **quarterly_report.xlsx** - Financial data
   - Sheets: Q1, Q2
   - Columns: month, revenue, expenses

## Chart Types Supported from Excel

All 10 chart types support Excel input:

| Chart Type | Command | Excel Requirements |
|------------|---------|-------------------|
| Line Chart | `line` | date, category, value |
| Bar Chart | `bar` | category, value |
| Scatter Plot | `scatter` | x, y (optional: category) |
| Pie/Donut | `pie` | category, value |
| Heatmap | `heatmap` | date, category, value |
| Area Chart | `area` | date + numeric columns |
| Violin Plot | `violin` | category, value |
| Network Graph | `network` | source, target (optional: weight) |
| Gantt Chart | `gantt` | task, start_date, end_date |
| Milestone Chart | `milestone` | milestone, date (optional: status) |

## Python API Reference

### Read Excel File

```python
from scripts.excel_utils import read_excel

# Read first sheet
df = read_excel('data/file.xlsx')

# Read specific sheet
df = read_excel('data/file.xlsx', sheet_name='Sheet2')

# Read specific columns
df = read_excel('data/file.xlsx', usecols=['Date', 'Sales', 'Profit'])

# Custom header row
df = read_excel('data/file.xlsx', header=1)  # Use row 2 as headers
```

### List Sheets

```python
from scripts.excel_utils import list_sheets

sheets = list_sheets('data/file.xlsx')
print(f"Available sheets: {sheets}")
```

### Write Excel File

```python
from scripts.excel_utils import write_excel
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
write_excel(df, 'output/result.xlsx', sheet_name='Data')
```

### Convert Excel to CSV

```python
from scripts.excel_utils import excel_to_csv

excel_to_csv('data/input.xlsx', 'data/output.csv', sheet_name='Sales')
```

### Get File Information

```python
from scripts.excel_utils import get_excel_info

info = get_excel_info('data/file.xlsx')
print(f"Sheets: {info['sheet_names']}")
print(f"File size: {info['file_size']} bytes")
```

### Validate Excel File

```python
from scripts.excel_utils import validate_excel_file

if validate_excel_file('data/file.xlsx'):
    print("Valid Excel file!")
```

## Command-Line Options

### chart_from_excel.py

```
usage: chart_from_excel.py [-h] [--sheet SHEET] [--output OUTPUT]
                           [--format {png,svg,pdf}] [--list-sheets]
                           [--x X] [--y Y] [--color COLOR]
                           [--category CATEGORY] [--value VALUE] [--donut]
                           {line,bar,scatter,pie,heatmap,area,violin,network,gantt,milestone}
                           excel_file

positional arguments:
  {line,bar,scatter,pie,heatmap,area,violin,network,gantt,milestone}
                        Type of chart to generate
  excel_file            Path to Excel file

optional arguments:
  --sheet SHEET         Sheet name (default: first sheet)
  --output OUTPUT       Output file path
  --format {png,svg,pdf}
                        Output format (default: png)
  --list-sheets         List all sheets in the Excel file and exit
  --x X                 X-axis column (for scatter plot)
  --y Y                 Y-axis column (for scatter plot)
  --color COLOR         Color column (for scatter plot)
  --category CATEGORY   Category column (for pie chart)
  --value VALUE         Value column (for pie chart)
  --donut               Create donut chart
```

### excel_utils.py

```
usage: excel_utils.py [-h] {list,info,convert} ...

Commands:
  list      List sheets in Excel file
  info      Get Excel file information
  convert   Convert Excel to CSV
```

## Best Practices

1. **Use Descriptive Sheet Names**: Name sheets clearly (e.g., "Sales_2024", "Q1_Data")

2. **Structure Your Data**: Keep data in tabular format with headers in the first row

3. **Avoid Merged Cells**: Merged cells can cause reading issues

4. **Use Standard Formats**: 
   - Dates: YYYY-MM-DD format
   - Numbers: Plain numbers without text
   - Categories: Consistent naming

5. **Check Column Names**: Ensure column names match what the chart script expects

6. **Test with Sample Data**: Test with small files first

## Troubleshooting

### "Excel file not found"
- Check file path is correct
- Use absolute paths if needed

### "Missing required columns"
- Run `python scripts/excel_utils.py info your_file.xlsx` to see available columns
- Check column names match exactly (case-sensitive)

### "Error reading Excel file"
- Ensure openpyxl is installed: `pip install openpyxl`
- Check file is not corrupted
- Try opening in Excel/LibreOffice first

### Sheet not found
- Use `--list-sheets` to see available sheets
- Sheet names are case-sensitive

## Performance Tips

- **Large Files**: For files > 100MB, consider converting to CSV first
- **Multiple Sheets**: Convert each sheet separately if needed
- **Memory**: Close Excel files in Excel before processing

## Examples Gallery

### Generate Multiple Charts from One Excel File

```bash
# Generate different charts from different sheets
python scripts/chart_from_excel.py line data/report.xlsx --sheet Sales
python scripts/chart_from_excel.py bar data/report.xlsx --sheet Costs
python scripts/chart_from_excel.py pie data/report.xlsx --sheet Distribution
```

### Batch Process Excel Files

```bash
# Convert all Excel files in a directory
for file in data/*.xlsx; do
    python scripts/excel_utils.py convert "$file" "data/csv/$(basename "$file" .xlsx).csv"
done
```

### Create Dashboard from Excel Data

```bash
# Generate multiple visualizations for a dashboard
python scripts/chart_from_excel.py line data/dashboard.xlsx --sheet Trends --output reports/trends.png
python scripts/chart_from_excel.py bar data/dashboard.xlsx --sheet Comparison --output reports/comparison.png
python scripts/chart_from_excel.py pie data/dashboard.xlsx --sheet Distribution --output reports/distribution.png
```

## Integration with Existing Workflows

### Excel + Python

```python
# Your existing workflow
import pandas as pd
from scripts.excel_utils import read_excel

# Read from Excel
df = read_excel('input/data.xlsx')

# Your processing
df['new_column'] = df['old_column'] * 2

# Generate chart (save to CSV first for compatibility)
df.to_csv('temp/processed.csv', index=False)
# Then use chart scripts...
```

### Automated Reports

```bash
#!/bin/bash
# Report generation script

# Download latest data (your process)
# ...

# Generate charts from Excel
python scripts/chart_from_excel.py line data/latest.xlsx --output reports/monthly_trend.png
python scripts/chart_from_excel.py gantt data/project.xlsx --output reports/timeline.pdf

# Combine into report
# ...
```

## Support

For issues or questions:
- Check this guide first
- Run `python scripts/excel_utils.py --help`
- Create an issue on GitHub with:
  - Excel file structure (sheets, columns)
  - Command you're running
  - Error message

---

✨ **Excel integration makes it easier than ever to visualize your data!**

---

## Embedding Charts in Excel Files

### Overview

You can now embed charts directly into Excel files, creating professional reports with data and visualizations in a single workbook.

### Quick Start

```bash
# Embed a chart into an Excel file
python scripts/embed_in_excel.py data/sample_data.xlsx --chart-type bar

# Specify sheet and position
python scripts/embed_in_excel.py data/report.xlsx --sheet Sales --chart-type line --position H2

# Custom output file
python scripts/embed_in_excel.py data/data.xlsx --output reports/final_report.xlsx
```

### Command-Line Usage

```bash
usage: embed_in_excel.py [-h] [--output OUTPUT] [--sheet SHEET]
                        [--chart-type {line,bar,pie,scatter}]
                        [--position POSITION] [--x X] [--y Y]
                        excel_file

arguments:
  excel_file            Input Excel file
  --output OUTPUT       Output Excel file (default: adds _with_chart suffix)
  --sheet SHEET         Sheet name to use (default: first sheet)
  --chart-type          Type of chart (line, bar, pie, scatter)
  --position POSITION   Cell position for chart (e.g., H2, M10)
  --x X                 X column for scatter plot
  --y Y                 Y column for scatter plot
```

### Python API - Single Chart

```python
from scripts.embed_in_excel import embed_chart_in_excel

# Embed a chart
embed_chart_in_excel(
    excel_path='data/sales.xlsx',
    output_path='reports/sales_report.xlsx',
    sheet_name='Q1',
    chart_type='line',
    position='H2'
)
```

### Python API - Multiple Charts

```python
from scripts.embed_in_excel import embed_multiple_charts

# Define multiple charts
charts_config = [
    {'sheet': 'Sales', 'chart_type': 'line', 'position': 'H2'},
    {'sheet': 'Sales', 'chart_type': 'bar', 'position': 'H20'},
    {'sheet': 'Costs', 'chart_type': 'pie', 'position': 'H2'},
]

# Embed all charts
embed_multiple_charts(
    excel_path='data/report.xlsx',
    output_path='data/report_with_charts.xlsx',
    charts_config=charts_config
)
```

### Python API - Create Complete Report

```python
from scripts.embed_in_excel import create_report_with_charts
import pandas as pd

# Prepare your data
sales_df = pd.DataFrame({
    'date': ['2024-01', '2024-02', '2024-03'],
    'category': ['A', 'A', 'A'],
    'value': [100, 120, 115]
})

costs_df = pd.DataFrame({
    'date': ['2024-01', '2024-02', '2024-03'],
    'category': ['A', 'A', 'A'],
    'value': [60, 70, 65]
})

# Define data sheets
data_dict = {
    'Sales': sales_df,
    'Costs': costs_df
}

# Define chart positions
chart_positions = {
    'Sales': {'chart_type': 'line', 'position': 'F2'},
    'Costs': {'chart_type': 'bar', 'position': 'F2'}
}

# Create report with data and charts
create_report_with_charts(
    data_dict=data_dict,
    output_path='reports/monthly_report.xlsx',
    chart_positions=chart_positions
)
```

### Chart Positioning

Charts are positioned using Excel cell references:

- `H2` - Column H, Row 2 (default)
- `A1` - Top-left corner
- `M10` - Column M, Row 10
- `AA5` - Column AA, Row 5

**Tips:**
- Leave 6-8 columns for data before the chart
- Charts are 500px wide × 312px tall (fits ~8 columns × 15 rows)
- Stack multiple charts vertically with 18-20 row spacing

### Supported Chart Types

| Type | Description | Best For |
|------|-------------|----------|
| `line` | Line chart with multiple series | Time series, trends |
| `bar` | Vertical bar chart | Category comparison |
| `pie` | Pie chart with percentages | Distribution, proportions |
| `scatter` | Scatter plot | Correlation analysis |

### Use Cases

#### 1. Automated Reporting

```python
# Monthly report automation
from scripts.embed_in_excel import create_report_with_charts
import pandas as pd
from datetime import datetime

# Read latest data
sales = pd.read_excel('current_month.xlsx', sheet_name='Sales')
expenses = pd.read_excel('current_month.xlsx', sheet_name='Expenses')

# Create report
create_report_with_charts(
    data_dict={'Sales': sales, 'Expenses': expenses},
    output_path=f'reports/report_{datetime.now():%Y%m}.xlsx',
    chart_positions={
        'Sales': {'chart_type': 'line', 'position': 'H2'},
        'Expenses': {'chart_type': 'bar', 'position': 'H2'}
    }
)
```

#### 2. Dashboard Creation

```python
# Create dashboard with multiple views
charts = [
    {'sheet': 'Overview', 'chart_type': 'line', 'position': 'H2'},
    {'sheet': 'Overview', 'chart_type': 'pie', 'position': 'P2'},
    {'sheet': 'Details', 'chart_type': 'bar', 'position': 'H2'},
]

embed_multiple_charts('data.xlsx', 'dashboard.xlsx', charts)
```

#### 3. Report Generation Pipeline

```bash
#!/bin/bash
# Generate multiple reports

# Process each data file
for file in data/*.xlsx; do
    name=$(basename "$file" .xlsx)
    python scripts/embed_in_excel.py "$file" \
        --output "reports/${name}_report.xlsx" \
        --chart-type line
done
```

### Best Practices

1. **Chart Placement**: Place charts to the right of data (H column or later)
2. **Multiple Charts**: Space charts 18-20 rows apart vertically
3. **File Size**: Each embedded chart adds ~50-100KB
4. **Performance**: Batch operations for multiple files
5. **Testing**: Test with small files first

### Limitations

- Charts are embedded as images (not native Excel charts)
- Cannot edit charts after embedding (must regenerate)
- Limited to 4 chart types (line, bar, pie, scatter)
- Charts are static (no interactive features)

### Troubleshooting

**Chart not appearing:**
- Check cell position is valid (e.g., 'H2' not 'H')
- Ensure position doesn't overlap with data
- Verify sheet name is correct (case-sensitive)

**Image quality issues:**
- Charts are generated at 100 DPI
- Increase DPI in `create_chart_image()` if needed
- Consider SVG export for better quality

**File size too large:**
- Reduce number of embedded charts
- Use lower DPI settings
- Consider external image linking instead

### Examples

See `examples/embed_examples.py` for complete working examples:

```bash
cd examples
python embed_examples.py
```

This creates 4 example reports demonstrating different embedding scenarios.

---

✨ **Create professional Excel reports with embedded visualizations!**
