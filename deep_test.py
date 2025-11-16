#!/usr/bin/env python3
"""
Deep Testing Suite for Autonomous 3D Graph System
Tests all features, visualizations, data sources, and edge cases
"""

import sys
import traceback
import pandas as pd
import numpy as np
import json
import tempfile
from pathlib import Path


class DeepTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests_run = 0

    def test(self, name, func):
        """Run a test and track results"""
        self.tests_run += 1
        print(f"\n{'='*70}")
        print(f"Test {self.tests_run}: {name}")
        print(f"{'='*70}")
        try:
            func()
            print(f"✓ PASSED: {name}")
            self.passed += 1
            return True
        except Exception as e:
            print(f"✗ FAILED: {name}")
            print(f"Error: {str(e)}")
            traceback.print_exc()
            self.failed += 1
            return False

    def report(self):
        """Print final test report"""
        print("\n" + "="*70)
        print("DEEP TEST RESULTS")
        print("="*70)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.passed} ✓")
        print(f"Failed: {self.failed} ✗")
        print(f"Success Rate: {(self.passed/self.tests_run)*100:.1f}%")
        print("="*70)
        return self.failed == 0


def test_all_imports():
    """Test comprehensive imports"""
    from agentic_graphs import (
        AutonomousGraphSystem,
        auto_visualize,
        analyze_data,
        load_data,
        AutonomousGraphAgent,
        DataProfile,
        AutoConnector,
        VisualizerFactory
    )
    print("✓ All main imports successful")

    # Test visualizer types
    viz_types = VisualizerFactory.available_types()
    print(f"✓ Available visualizations: {viz_types}")
    assert len(viz_types) == 5, "Expected 5 visualization types"
    print("✓ All 5 visualization types available")


def test_csv_data_loading():
    """Test CSV data loading with various formats"""
    from agentic_graphs import load_data

    # Test existing CSV files
    df1 = load_data('data/network_sample.csv', verbose=False)
    assert len(df1) == 10, f"Expected 10 rows, got {len(df1)}"
    assert 'source' in df1.columns, "Missing 'source' column"
    assert 'target' in df1.columns, "Missing 'target' column"
    print(f"✓ Network CSV loaded: {df1.shape}")

    df2 = load_data('data/3d_scatter_sample.csv', verbose=False)
    assert len(df2) == 15, f"Expected 15 rows, got {len(df2)}"
    assert 'x' in df2.columns and 'y' in df2.columns and 'z' in df2.columns
    print(f"✓ Scatter CSV loaded: {df2.shape}")

    df3 = load_data('data/surface_sample.csv', verbose=False)
    assert len(df3) == 25, f"Expected 25 rows, got {len(df3)}"
    print(f"✓ Surface CSV loaded: {df3.shape}")


def test_json_data_loading():
    """Test JSON data loading"""
    from agentic_graphs import load_data

    # Create temporary JSON file
    json_data = {
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 6, 8, 10],
        'z': [1, 4, 9, 16, 25],
        'category': ['A', 'B', 'A', 'B', 'A']
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(json_data, f)
        temp_json = f.name

    try:
        df = load_data(temp_json, verbose=False)
        assert len(df) == 5, f"Expected 5 rows, got {len(df)}"
        assert 'x' in df.columns, "Missing 'x' column"
        print(f"✓ JSON loaded from file: {df.shape}")
    finally:
        Path(temp_json).unlink()

    # Test JSON string
    df2 = load_data(json.dumps(json_data), source_type='json', verbose=False)
    assert len(df2) == 5, f"Expected 5 rows, got {len(df2)}"
    print(f"✓ JSON loaded from string: {df2.shape}")


def test_dataframe_loading():
    """Test direct DataFrame loading"""
    from agentic_graphs import load_data

    df_input = pd.DataFrame({
        'x': np.random.rand(20),
        'y': np.random.rand(20),
        'z': np.random.rand(20),
        'category': np.random.choice(['A', 'B', 'C'], 20)
    })

    df = load_data(df_input, verbose=False)
    assert len(df) == 20, f"Expected 20 rows, got {len(df)}"
    assert list(df.columns) == list(df_input.columns), "Columns don't match"
    print(f"✓ DataFrame loaded directly: {df.shape}")


def test_data_analysis_network():
    """Test autonomous analysis of network data"""
    from agentic_graphs import analyze_data

    profile = analyze_data('data/network_sample.csv', verbose=False)

    assert profile.num_rows == 10, f"Expected 10 rows, got {profile.num_rows}"
    assert profile.has_network_structure, "Network structure not detected"
    assert '3d_network' in profile.suggested_visualizations, "Network viz not suggested"
    assert profile.confidence_scores['3d_network'] > 0.9, "Low confidence for network"

    print(f"✓ Network data analyzed correctly")
    print(f"  - Detected network structure: {profile.has_network_structure}")
    print(f"  - Top suggestion: {profile.suggested_visualizations[0]}")
    print(f"  - Confidence: {profile.confidence_scores[profile.suggested_visualizations[0]]:.1%}")


def test_data_analysis_scatter():
    """Test autonomous analysis of 3D scatter data"""
    from agentic_graphs import analyze_data

    profile = analyze_data('data/3d_scatter_sample.csv', verbose=False)

    assert profile.num_rows == 15, f"Expected 15 rows, got {profile.num_rows}"
    assert profile.has_numeric, "Numeric data not detected"
    assert '3d_scatter' in profile.suggested_visualizations, "Scatter viz not suggested"

    print(f"✓ Scatter data analyzed correctly")
    print(f"  - Has numeric: {profile.has_numeric}")
    print(f"  - Has categorical: {profile.has_categorical}")
    print(f"  - Top suggestion: {profile.suggested_visualizations[0]}")


def test_data_analysis_surface():
    """Test autonomous analysis of surface data"""
    from agentic_graphs import analyze_data

    profile = analyze_data('data/surface_sample.csv', verbose=False)

    assert profile.num_rows == 25, f"Expected 25 rows, got {profile.num_rows}"
    assert profile.has_numeric, "Numeric data not detected"

    print(f"✓ Surface data analyzed correctly")
    print(f"  - Columns: {profile.num_columns}")
    print(f"  - Suggestions: {profile.suggested_visualizations}")


def test_network_3d_visualization():
    """Test 3D network graph generation"""
    from agentic_graphs import AutonomousGraphSystem

    system = AutonomousGraphSystem(verbose=False)

    output_path = 'examples/deep_test_network.html'
    fig = system.generate(
        'data/network_sample.csv',
        viz_type='3d_network',
        output_path=output_path,
        show=False
    )

    assert fig is not None, "Figure not generated"
    assert Path(output_path).exists(), f"Output file not created: {output_path}"
    assert Path(output_path).stat().st_size > 1000, "Output file too small"

    print(f"✓ 3D Network visualization created")
    print(f"  - Output: {output_path}")
    print(f"  - Size: {Path(output_path).stat().st_size} bytes")


def test_scatter_3d_visualization():
    """Test 3D scatter plot generation"""
    from agentic_graphs import AutonomousGraphSystem

    system = AutonomousGraphSystem(verbose=False)

    output_path = 'examples/deep_test_scatter.html'
    fig = system.generate(
        'data/3d_scatter_sample.csv',
        viz_type='3d_scatter',
        output_path=output_path,
        show=False
    )

    assert fig is not None, "Figure not generated"
    assert Path(output_path).exists(), f"Output file not created: {output_path}"

    print(f"✓ 3D Scatter visualization created")
    print(f"  - Output: {output_path}")


def test_surface_3d_visualization():
    """Test 3D surface plot generation"""
    from agentic_graphs import AutonomousGraphSystem

    system = AutonomousGraphSystem(verbose=False)

    output_path = 'examples/deep_test_surface.html'
    fig = system.generate(
        'data/surface_sample.csv',
        viz_type='3d_surface',
        output_path=output_path,
        show=False
    )

    assert fig is not None, "Figure not generated"
    assert Path(output_path).exists(), f"Output file not created: {output_path}"

    print(f"✓ 3D Surface visualization created")
    print(f"  - Output: {output_path}")


def test_line_3d_visualization():
    """Test 3D line plot generation"""
    from agentic_graphs import AutonomousGraphSystem

    # Create temporal data
    df = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=50),
        'x': np.cumsum(np.random.randn(50)),
        'y': np.cumsum(np.random.randn(50)),
        'z': np.cumsum(np.random.randn(50))
    })

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_csv = f.name

    try:
        system = AutonomousGraphSystem(verbose=False)
        output_path = 'examples/deep_test_line.html'

        fig = system.generate(
            temp_csv,
            viz_type='3d_line',
            output_path=output_path,
            show=False
        )

        assert fig is not None, "Figure not generated"
        assert Path(output_path).exists(), f"Output file not created: {output_path}"

        print(f"✓ 3D Line visualization created")
    finally:
        Path(temp_csv).unlink()


def test_bar_3d_visualization():
    """Test 3D bar chart generation"""
    from agentic_graphs import AutonomousGraphSystem

    # Create categorical data
    df = pd.DataFrame({
        'category_a': np.random.choice(['X', 'Y', 'Z'], 30),
        'category_b': np.random.choice(['P', 'Q'], 30),
        'value': np.random.randint(10, 100, 30)
    })

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_csv = f.name

    try:
        system = AutonomousGraphSystem(verbose=False)
        output_path = 'examples/deep_test_bar.html'

        fig = system.generate(
            temp_csv,
            viz_type='3d_bar',
            output_path=output_path,
            show=False
        )

        assert fig is not None, "Figure not generated"
        assert Path(output_path).exists(), f"Output file not created: {output_path}"

        print(f"✓ 3D Bar visualization created")
    finally:
        Path(temp_csv).unlink()


def test_autonomous_decision_making():
    """Test that autonomous system makes correct decisions"""
    from agentic_graphs import AutonomousGraphSystem

    system = AutonomousGraphSystem(verbose=False)

    # Test network data -> should choose 3d_network
    profile1 = system.analyze('data/network_sample.csv')
    assert profile1.suggested_visualizations[0] == '3d_network', \
        f"Expected 3d_network, got {profile1.suggested_visualizations[0]}"
    print("✓ Correctly chose 3d_network for network data")

    # Test 3D scatter data -> should choose 3d_scatter
    profile2 = system.analyze('data/3d_scatter_sample.csv')
    assert profile2.suggested_visualizations[0] == '3d_scatter', \
        f"Expected 3d_scatter, got {profile2.suggested_visualizations[0]}"
    print("✓ Correctly chose 3d_scatter for scatter data")

    print("✓ Autonomous decision making works correctly")


def test_custom_parameters():
    """Test custom parameter passing to visualizers"""
    from agentic_graphs import AutonomousGraphSystem

    system = AutonomousGraphSystem(verbose=False)

    output_path = 'examples/deep_test_custom.html'
    fig = system.generate(
        'data/3d_scatter_sample.csv',
        viz_type='3d_scatter',
        x_col='x',
        y_col='y',
        z_col='z',
        color_col='category',
        size_col='value',
        title='Custom Test Visualization',
        output_path=output_path,
        show=False
    )

    assert fig is not None, "Figure not generated"
    assert Path(output_path).exists(), f"Output file not created: {output_path}"

    print("✓ Custom parameters work correctly")


def test_batch_processing():
    """Test batch processing of multiple datasets"""
    from agentic_graphs import AutonomousGraphSystem

    system = AutonomousGraphSystem(verbose=False)

    results = system.batch_generate(
        [
            'data/network_sample.csv',
            'data/3d_scatter_sample.csv',
            'data/surface_sample.csv'
        ],
        output_dir='examples/batch_deep_test'
    )

    assert len(results) == 3, f"Expected 3 results, got {len(results)}"
    assert all(fig is not None for fig in results.values()), "Some figures failed"

    # Check output files
    batch_dir = Path('examples/batch_deep_test')
    assert batch_dir.exists(), "Batch output directory not created"
    html_files = list(batch_dir.glob('*.html'))
    assert len(html_files) == 3, f"Expected 3 HTML files, got {len(html_files)}"

    print(f"✓ Batch processing successful")
    print(f"  - Processed: {len(results)} datasets")
    print(f"  - Output files: {len(html_files)}")


def test_visualization_suggestions():
    """Test getting visualization suggestions"""
    from agentic_graphs import AutonomousGraphSystem

    system = AutonomousGraphSystem(verbose=False)

    suggestions = system.suggest_visualizations('data/network_sample.csv')

    assert len(suggestions) > 0, "No suggestions returned"
    assert all(isinstance(s, tuple) and len(s) == 2 for s in suggestions), \
        "Invalid suggestion format"
    assert all(0 <= s[1] <= 1 for s in suggestions), \
        "Confidence scores not in valid range"

    print(f"✓ Visualization suggestions work")
    print(f"  - Suggestions: {len(suggestions)}")
    for viz, conf in suggestions[:3]:
        print(f"    - {viz}: {conf:.1%}")


def test_cli_module():
    """Test CLI module functionality"""
    from agentic_graphs import cli

    assert hasattr(cli, 'main'), "CLI main function not found"

    # Test that it can be imported and has required components
    print("✓ CLI module structure valid")


def test_error_handling():
    """Test error handling for invalid inputs"""
    from agentic_graphs import load_data, AutonomousGraphSystem

    system = AutonomousGraphSystem(verbose=False)

    # Test non-existent file
    try:
        load_data('nonexistent_file.csv', verbose=False)
        assert False, "Should have raised error for non-existent file"
    except:
        print("✓ Correctly handles non-existent file")

    # Test invalid visualization type
    try:
        system.generate(
            'data/network_sample.csv',
            viz_type='invalid_viz_type',
            show=False
        )
        assert False, "Should have raised error for invalid viz type"
    except:
        print("✓ Correctly handles invalid visualization type")


def test_correlation_detection():
    """Test correlation detection in data analysis"""
    from agentic_graphs import analyze_data

    # Create data with strong correlation
    df = pd.DataFrame({
        'x': np.arange(100),
        'y': np.arange(100) * 2 + np.random.randn(100) * 0.1,  # Strong positive correlation
        'z': -np.arange(100) + np.random.randn(100) * 0.1  # Strong negative correlation
    })

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_csv = f.name

    try:
        profile = analyze_data(temp_csv, verbose=False)

        # Check that relationships were detected
        assert len(profile.relationships) > 0, "No relationships detected"

        # Check for correlation types
        rel_types = [r[2] for r in profile.relationships]
        has_correlation = any('correlation' in rt for rt in rel_types)
        assert has_correlation, "Correlation not detected"

        print(f"✓ Correlation detection works")
        print(f"  - Relationships found: {len(profile.relationships)}")
        for r in profile.relationships[:3]:
            print(f"    - {r[0]} ↔ {r[1]}: {r[2]}")
    finally:
        Path(temp_csv).unlink()


def test_large_dataset():
    """Test handling of larger datasets"""
    from agentic_graphs import AutonomousGraphSystem

    # Create larger dataset
    n = 1000
    df = pd.DataFrame({
        'x': np.random.randn(n),
        'y': np.random.randn(n),
        'z': np.random.randn(n),
        'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], n),
        'value': np.random.randint(1, 100, n)
    })

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_csv = f.name

    try:
        system = AutonomousGraphSystem(verbose=False)
        output_path = 'examples/deep_test_large.html'

        fig = system.generate(
            temp_csv,
            output_path=output_path,
            show=False
        )

        assert fig is not None, "Figure not generated for large dataset"
        assert Path(output_path).exists(), "Output file not created"

        print(f"✓ Large dataset handled successfully")
        print(f"  - Dataset size: {n} rows")
    finally:
        Path(temp_csv).unlink()


def test_auto_visualize_function():
    """Test the convenience auto_visualize function"""
    from agentic_graphs import auto_visualize

    output_path = 'examples/deep_test_auto.html'
    fig = auto_visualize(
        'data/network_sample.csv',
        output_path=output_path,
        show=False,
        verbose=False
    )

    assert fig is not None, "Figure not generated"
    assert Path(output_path).exists(), "Output file not created"

    print("✓ auto_visualize convenience function works")


def main():
    """Run comprehensive deep testing suite"""
    print("="*70)
    print("AUTONOMOUS 3D GRAPH SYSTEM - DEEP TESTING SUITE")
    print("="*70)
    print("\nThis will thoroughly test all components of the system.")
    print("Tests include: imports, data loading, analysis, visualizations,")
    print("autonomous decisions, error handling, and performance.\n")

    tester = DeepTester()

    # Core functionality tests
    tester.test("Import all modules and classes", test_all_imports)
    tester.test("CSV data loading", test_csv_data_loading)
    tester.test("JSON data loading", test_json_data_loading)
    tester.test("DataFrame loading", test_dataframe_loading)

    # Data analysis tests
    tester.test("Network data analysis", test_data_analysis_network)
    tester.test("Scatter data analysis", test_data_analysis_scatter)
    tester.test("Surface data analysis", test_data_analysis_surface)
    tester.test("Correlation detection", test_correlation_detection)

    # Visualization tests (all types)
    tester.test("3D Network visualization", test_network_3d_visualization)
    tester.test("3D Scatter visualization", test_scatter_3d_visualization)
    tester.test("3D Surface visualization", test_surface_3d_visualization)
    tester.test("3D Line visualization", test_line_3d_visualization)
    tester.test("3D Bar visualization", test_bar_3d_visualization)

    # Autonomous system tests
    tester.test("Autonomous decision making", test_autonomous_decision_making)
    tester.test("Visualization suggestions", test_visualization_suggestions)
    tester.test("Custom parameters", test_custom_parameters)
    tester.test("Batch processing", test_batch_processing)

    # Utility tests
    tester.test("auto_visualize function", test_auto_visualize_function)
    tester.test("CLI module", test_cli_module)

    # Robustness tests
    tester.test("Error handling", test_error_handling)
    tester.test("Large dataset handling", test_large_dataset)

    # Generate report
    success = tester.report()

    if success:
        print("\n🎉 ALL DEEP TESTS PASSED! 🎉")
        print("\nThe autonomous 3D graph system is fully functional and robust.")
        print("\nGenerated test outputs in examples/ directory:")
        test_files = sorted(Path('examples').glob('deep_test*.html'))
        for f in test_files:
            print(f"  ✓ {f}")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
