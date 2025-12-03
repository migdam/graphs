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
