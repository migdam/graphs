# System Architecture

**Autonomous 3D Graph Generation System - Technical Architecture Documentation**

Version 1.1.0

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Decision Making Process](#decision-making-process)
6. [AI Analytics Pipeline](#ai-analytics-pipeline)
7. [Extensibility](#extensibility)
8. [Performance Considerations](#performance-considerations)

---

## Overview

### System Purpose

The Autonomous 3D Graph Generation System is designed to:
- Automatically analyze multi-source data
- Make intelligent visualization decisions
- Generate beautiful 3D interactive graphs
- Provide AI-powered insights and analytics

### Design Principles

1. **Autonomy**: Minimal user input required
2. **Modularity**: Components are independent and reusable
3. **Extensibility**: Easy to add new visualizations or data sources
4. **Robustness**: Comprehensive error handling
5. **Intelligence**: AI-driven decision making

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
├─────────────────────────────────────────────────────────────┤
│  CLI Interface  │  Python API  │  Convenience Functions     │
└────────┬──────────────────────────────────────┬─────────────┘
         │                                       │
         v                                       v
┌─────────────────────────────────────────────────────────────┐
│                  Autonomous System Orchestrator              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Decision   │  │     Data     │  │      AI      │     │
│  │    Agent     │  │  Connectors  │  │  Analytics   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────┬──────────────────────────────────────┬─────────────┘
         │                                       │
         v                                       v
┌─────────────────────────────────────────────────────────────┐
│                  Visualization Layer                         │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐           │
│  │Network │  │Scatter │  │Surface │  │ Line   │  ...       │
│  │  3D    │  │  3D    │  │  3D    │  │  3D    │           │
│  └────────┘  └────────┘  └────────┘  └────────┘           │
└────────┬────────────────────────────────────────────────────┘
         │
         v
┌─────────────────────────────────────────────────────────────┐
│                    Output Layer                              │
│  Interactive HTML  │  PNG/JPG  │  JSON Analytics            │
└─────────────────────────────────────────────────────────────┘
```

### Component Layers

1. **User Interface Layer**: Entry points (CLI, API)
2. **Orchestration Layer**: Coordinates all components
3. **Intelligence Layer**: Decision making and analytics
4. **Data Layer**: Multi-source data loading
5. **Visualization Layer**: Graph generation
6. **Output Layer**: File creation and display

---

## Component Details

### 1. Autonomous System Orchestrator

**File**: `agentic_graphs/autonomous_system.py`

**Purpose**: Main coordinator that ties all components together

**Key Classes**:
- `AutonomousGraphSystem`: Primary entry point

**Responsibilities**:
- Initialize all subsystems
- Coordinate data flow between components
- Handle user requests
- Manage error handling

**Key Methods**:
```python
generate()                    # Main generation pipeline
analyze()                     # Data analysis only
run_analytics()              # AI analytics only
generate_with_analytics()    # Combined generation + analytics
batch_generate()             # Process multiple datasets
```

### 2. Decision Agent

**File**: `agentic_graphs/agent_core.py`

**Purpose**: Autonomous decision-making for visualization selection

**Key Classes**:
- `AutonomousGraphAgent`: AI agent
- `DataProfile`: Data analysis results

**Decision Algorithm**:

```python
def decide_visualization(df, preference=None):
    1. Analyze data structure
       - Detect column types
       - Identify patterns
       - Find relationships

    2. Apply heuristic rules
       - Network detection (source/target)
       - Dimension counting (for 3D scatter)
       - Temporal detection (date columns)
       - Spatial detection (x/y/z columns)

    3. Calculate confidence scores
       - Network: 95% if source/target found
       - Scatter: 60% + 10% per numeric column
       - Surface: 75% if grid structure detected

    4. Rank suggestions by confidence

    5. Return top choice or user preference
```

**Heuristics**:

| Pattern | Detection Method | Confidence |
|---------|------------------|------------|
| Network | source/target columns | 95% |
| 3D Scatter | 3+ numeric columns | 60-90% |
| Surface | Grid structure + 3 numeric | 75% |
| Temporal | Date/time columns | 80% |
| Mesh | Spatial keywords (x/y/z) | 85% |

### 3. Data Connectors

**File**: `agentic_graphs/data_connectors.py`

**Purpose**: Load data from multiple sources

**Architecture**:

```
AutoConnector (auto-detection)
    │
    ├── CSVConnector
    ├── JSONConnector
    ├── ExcelConnector
    ├── SQLConnector
    ├── APIConnector
    └── DataFrameConnector
```

**Auto-Detection Logic**:

```python
def _detect_source_type(source):
    if isinstance(source, pd.DataFrame):
        return 'dataframe'

    if is_url(source):
        return 'api'

    if Path(source).exists():
        return detect_from_extension()

    if is_sql_query(source):
        return 'sql'

    if is_json_string(source):
        return 'json'

    raise ValueError("Could not detect source type")
```

### 4. Visualizers

**File**: `agentic_graphs/visualizers_3d.py`

**Purpose**: Generate 3D visualizations using Plotly

**Class Hierarchy**:

```
Base3DVisualizer (abstract base)
    │
    ├── Scatter3DVisualizer
    ├── Surface3DVisualizer
    ├── Line3DVisualizer
    ├── Network3DVisualizer
    └── Bar3DVisualizer
```

**Factory Pattern**:

```python
VisualizerFactory
    └── create(viz_type: str) -> Base3DVisualizer
```

**Common Interface**:

All visualizers implement:
```python
create(df, output_path, title, **kwargs) -> go.Figure
```

### 5. AI Analytics Engine

**File**: `agentic_graphs/ai_analytics.py`

**Purpose**: Extract insights and generate analytics

**Key Classes**:
- `AIGraphAnalytics`: Main analytics engine
- `GraphInsight`: Single insight container
- `AnalyticsReport`: Complete analytics report

**Analytics Modules**:

1. **Statistical Analysis**
   - Distribution analysis (skewness, kurtosis)
   - Outlier detection (IQR method)
   - Coefficient of variation
   - Multimodal distribution detection

2. **Pattern Detection**
   - Clustering identification
   - Temporal patterns
   - Data groupings

3. **Trend Analysis**
   - Correlation calculation (Pearson)
   - Linear regression
   - Monotonic trend detection

4. **Anomaly Detection**
   - IQR-based outlier detection
   - Statistical anomalies
   - Data quality issues

5. **Relationship Analysis**
   - Categorical vs numeric
   - Variable dependencies
   - Variance analysis

6. **Network-Specific**
   - Density calculation
   - Hub detection
   - Degree distribution

### 6. CLI Interface

**File**: `agentic_graphs/cli.py`

**Purpose**: Command-line interface

**Architecture**:
```python
ArgumentParser
    ├── Data source arguments
    ├── Visualization options
    ├── Analytics options
    ├── Output options
    └── Customization parameters
```

---

## Data Flow

### Standard Generation Pipeline

```
1. User Request
   ↓
2. Data Loading
   AutoConnector.load()
   - Detect source type
   - Call appropriate connector
   - Return DataFrame
   ↓
3. Data Analysis
   AutonomousGraphAgent.analyze_data()
   - Profile data structure
   - Detect patterns
   - Calculate statistics
   ↓
4. Decision Making
   AutonomousGraphAgent.decide_visualization()
   - Evaluate all viz types
   - Calculate confidence scores
   - Select best option
   ↓
5. Visualization Generation
   VisualizerFactory.create(viz_type)
   - Get appropriate visualizer
   - Auto-select columns
   - Generate Plotly figure
   ↓
6. Output
   - Save to file
   - Display (if requested)
   - Return Figure object
```

### Analytics Pipeline

```
1. Data Loading (same as above)
   ↓
2. Data Profiling
   AutonomousGraphAgent.analyze_data()
   ↓
3. Analytics Execution
   AIGraphAnalytics.analyze()
   ├── Statistical Analysis
   ├── Pattern Detection
   ├── Trend Analysis
   ├── Anomaly Detection
   ├── Relationship Analysis
   └── Network Analysis (if applicable)
   ↓
4. Insight Organization
   - Categorize insights
   - Calculate confidence scores
   - Generate recommendations
   - Create natural language summary
   ↓
5. Report Generation
   AnalyticsReport
   - Data summary
   - Insights list
   - Key findings
   - Recommendations
   ↓
6. Output
   - JSON export
   - Return report object
```

### Combined Pipeline (Visualization + Analytics)

```
1. Data Loading
   ↓
2. Data Analysis
   ↓
3. Decision Making
   ↓
4. [PARALLEL EXECUTION]
   ├── Visualization Generation
   │   ↓
   │   Figure object
   │
   └── Analytics Execution
       ↓
       AnalyticsReport
   ↓
5. Output
   - Visualization HTML
   - Analytics JSON (auto-exported)
   - Return (Figure, Report) tuple
```

---

## Decision Making Process

### Visualization Selection Algorithm

**Phase 1: Data Structure Analysis**

```python
for column in df.columns:
    if is_numeric(column):
        numeric_cols.append(column)
    elif is_datetime(column):
        temporal_cols.append(column)
    elif is_categorical(column):
        categorical_cols.append(column)
```

**Phase 2: Pattern Detection**

```python
# Network detection
has_source = any('source' in col.lower() for col in df.columns)
has_target = any('target' in col.lower() for col in df.columns)
if has_source and has_target:
    suggestions.append(('3d_network', 0.95))

# 3D scatter detection
if len(numeric_cols) >= 3:
    confidence = min(0.9, 0.6 + len(numeric_cols) * 0.1)
    suggestions.append(('3d_scatter', confidence))

# Spatial detection
spatial_keywords = ['x', 'y', 'z', 'lat', 'lon']
has_spatial = any(kw in col.lower() for col in df.columns
                  for kw in spatial_keywords)
if has_spatial and len(numeric_cols) >= 3:
    suggestions.append(('3d_mesh', 0.85))
```

**Phase 3: Ranking and Selection**

```python
# Sort by confidence
suggestions.sort(key=lambda x: x[1], reverse=True)

# Return top choice (or user preference)
if user_preference and user_preference in suggestions:
    return user_preference
else:
    return suggestions[0]
```

### Confidence Calculation

Confidence scores are calculated based on:

1. **Direct Indicators**: Exact column name matches (95%)
2. **Strong Indicators**: Pattern matches (80-90%)
3. **Moderate Indicators**: Statistical properties (60-80%)
4. **Weak Indicators**: Fallback options (50-60%)

---

## AI Analytics Pipeline

### Statistical Analysis Module

```python
def _analyze_statistical(df):
    for col in numeric_columns:
        # Skewness
        skew = df[col].skew()
        if abs(skew) > 1.0:
            create_insight('statistical', 'Skewed Distribution')

        # Coefficient of Variation
        cv = (std / mean) * 100
        if cv > 50:
            create_insight('statistical', 'High Variability')
```

### Pattern Detection Module

```python
def _analyze_patterns(df):
    # Multimodal distribution
    hist, bins = np.histogram(data, bins=10)
    peaks = find_peaks(hist)
    if len(peaks) >= 2:
        create_insight('pattern', 'Multimodal Distribution')

    # Temporal patterns
    if has_temporal_columns:
        create_insight('pattern', 'Temporal Data Detected')
```

### Anomaly Detection Module

```python
def _analyze_anomalies(df):
    # IQR method
    q1, q3 = df[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr

    outliers = df[(df[col] < lower) | (df[col] > upper)]
    if len(outliers) / len(df) > 0.05:
        create_insight('anomaly', 'Outliers Detected')
```

### Insight Generation

Each insight contains:
- **Category**: pattern/anomaly/trend/relationship/statistical
- **Title**: Short description
- **Description**: Detailed explanation
- **Confidence**: 0.0-1.0 score
- **Severity**: low/medium/high
- **Data Points**: Supporting evidence
- **Recommendation**: Actionable suggestion

---

## Extensibility

### Adding New Visualizations

1. Create visualizer class inheriting from `Base3DVisualizer`
2. Implement `create()` method
3. Register in `VisualizerFactory.VISUALIZERS`
4. Add detection logic to `AutonomousGraphAgent`

**Example**:

```python
# In visualizers_3d.py
class Cone3DVisualizer(Base3DVisualizer):
    def create(self, df, **kwargs):
        # Implementation
        pass

# In visualizers_3d.py - VisualizerFactory
VISUALIZERS = {
    '3d_scatter': Scatter3DVisualizer,
    # ... existing visualizers
    '3d_cone': Cone3DVisualizer,  # Add new
}

# In agent_core.py - _suggest_visualizations()
if has_vector_fields(df):
    suggestions.append(('3d_cone', 0.85))
```

### Adding New Data Sources

1. Create connector class inheriting from `DataConnector`
2. Implement `load()` method
3. Register in `AutoConnector.connectors`
4. Add detection logic to `AutoConnector._detect_source_type()`

**Example**:

```python
# In data_connectors.py
class ParquetConnector(DataConnector):
    def load(self, source, **kwargs):
        return pd.read_parquet(source, **kwargs)

# In AutoConnector.__init__()
self.connectors = {
    # ... existing connectors
    'parquet': ParquetConnector(verbose),
}

# In _detect_source_type()
ext = path.suffix.lower()
if ext == '.parquet':
    return 'parquet'
```

### Adding New Analytics

1. Add analysis method to `AIGraphAnalytics`
2. Call from `analyze()` method
3. Create appropriate `GraphInsight` objects

**Example**:

```python
def _analyze_seasonality(self, df):
    if self.has_temporal_data(df):
        # Seasonal decomposition
        # Create insights
        self.insights.append(GraphInsight(
            category='pattern',
            title='Seasonal Pattern Detected',
            description='...',
            confidence=0.85,
            severity='medium',
            data_points={...},
            recommendation='...'
        ))

# In analyze()
def analyze(self, df, viz_type, profile):
    # ... existing analysis
    self._analyze_seasonality(df)
```

---

## Performance Considerations

### Memory Management

- DataFrames are copied only when necessary
- Large datasets trigger automatic sampling suggestions
- Visualizations use efficient Plotly rendering

### Computational Complexity

| Operation | Complexity | Optimization |
|-----------|-----------|--------------|
| Data Loading | O(n) | Chunked reading for large files |
| Pattern Detection | O(n*m) | Early termination |
| Correlation Analysis | O(m²) | Limited to first N columns |
| Network Layout | O(n² to n³) | Spring layout with iterations limit |
| Visualization Rendering | O(n) | Plotly optimization |

### Scalability

**Small Datasets (< 1,000 rows)**:
- Full analysis
- All visualizations supported
- Real-time interaction

**Medium Datasets (1,000 - 10,000 rows)**:
- Full analysis
- May need sampling for some viz types
- Good interaction performance

**Large Datasets (> 10,000 rows)**:
- Automatic sampling recommended
- Aggregation for better performance
- Analytics on sampled data

### Optimization Strategies

1. **Lazy Loading**: Data loaded only when needed
2. **Early Termination**: Stop analysis when confidence high
3. **Parallel Processing**: Batch mode uses concurrent execution
4. **Caching**: Common calculations cached
5. **Incremental Processing**: Large files processed in chunks

---

## Error Handling Strategy

### Error Hierarchy

```
Exception
    ├── FileNotFoundError (data source)
    ├── ValueError (invalid data/parameters)
    ├── TypeError (wrong type)
    ├── KeyError (missing column)
    └── RuntimeError (processing error)
```

### Error Recovery

1. **Data Loading Errors**: Try alternative parsers
2. **Column Detection Errors**: Use fallbacks
3. **Visualization Errors**: Fallback to simpler viz
4. **Analytics Errors**: Continue with partial results

### Logging

- Verbose mode: Detailed progress
- Quiet mode: Errors only
- Error messages include actionable suggestions

---

## Testing Strategy

### Test Levels

1. **Unit Tests**: Individual components
2. **Integration Tests**: Component interactions
3. **System Tests**: End-to-end workflows
4. **Performance Tests**: Large dataset handling

### Test Coverage

- Data loading: 100%
- Visualizations: 100% (all 5 types)
- Analytics: 100%
- Decision making: 100%
- CLI: 100%

---

## Future Architecture Considerations

### Planned Enhancements

1. **Real-time Data**: Streaming data support
2. **Collaborative**: Multi-user analytics
3. **Cloud**: Cloud storage integration
4. **ML Models**: Advanced pattern detection
5. **Custom Themes**: User-defined color schemes

### Extension Points

- Plugin system for visualizations
- Custom analytics modules
- Theme marketplace
- Data source plugins

---

**Version 1.1.0** | Architecture Documentation | Built with ❤️ using Plotly, NetworkX, and Python
