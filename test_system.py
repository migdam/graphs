#!/usr/bin/env python3
"""
Quick test script for the Autonomous 3D Graph System
Tests core functionality without displaying visualizations
"""

import sys
import traceback

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from agentic_graphs import (
            AutonomousGraphSystem,
            auto_visualize,
            analyze_data,
            load_data
        )
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        traceback.print_exc()
        return False

def test_data_loading():
    """Test data loading from various sources"""
    print("\nTesting data loading...")
    try:
        from agentic_graphs import load_data

        # Test CSV loading
        df = load_data('data/network_sample.csv', verbose=False)
        assert len(df) > 0, "CSV data is empty"
        print(f"✓ CSV loading: {len(df)} rows loaded")

        # Test 3D scatter data
        df = load_data('data/3d_scatter_sample.csv', verbose=False)
        assert len(df) > 0, "Scatter data is empty"
        print(f"✓ 3D scatter loading: {len(df)} rows loaded")

        return True
    except Exception as e:
        print(f"✗ Data loading failed: {e}")
        traceback.print_exc()
        return False

def test_data_analysis():
    """Test autonomous data analysis"""
    print("\nTesting data analysis...")
    try:
        from agentic_graphs import analyze_data

        # Analyze network data
        profile = analyze_data('data/network_sample.csv', verbose=False)
        assert profile.num_rows > 0, "No rows detected"
        assert len(profile.suggested_visualizations) > 0, "No visualizations suggested"
        print(f"✓ Network analysis: {profile.num_rows} rows, suggested: {profile.suggested_visualizations[0]}")

        # Analyze 3D scatter data
        profile = analyze_data('data/3d_scatter_sample.csv', verbose=False)
        assert profile.has_numeric, "Numeric data not detected"
        print(f"✓ Scatter analysis: {len(profile.column_names)} columns, suggested: {profile.suggested_visualizations[0]}")

        return True
    except Exception as e:
        print(f"✗ Data analysis failed: {e}")
        traceback.print_exc()
        return False

def test_visualization_generation():
    """Test visualization generation (without display)"""
    print("\nTesting visualization generation...")
    try:
        from agentic_graphs import AutonomousGraphSystem

        system = AutonomousGraphSystem(verbose=False)

        # Test network visualization
        fig = system.generate(
            'data/network_sample.csv',
            output_path='examples/test_network.html',
            show=False
        )
        assert fig is not None, "Figure not generated"
        print("✓ Network visualization generated")

        # Test scatter visualization
        fig = system.generate(
            'data/3d_scatter_sample.csv',
            output_path='examples/test_scatter.html',
            show=False
        )
        assert fig is not None, "Figure not generated"
        print("✓ Scatter visualization generated")

        return True
    except Exception as e:
        print(f"✗ Visualization generation failed: {e}")
        traceback.print_exc()
        return False

def test_cli_available():
    """Test that CLI is available"""
    print("\nTesting CLI availability...")
    try:
        from agentic_graphs import cli
        assert hasattr(cli, 'main'), "CLI main function not found"
        print("✓ CLI module available")
        return True
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Autonomous 3D Graph System - Test Suite")
    print("="*60)

    results = []
    results.append(("Imports", test_imports()))
    results.append(("Data Loading", test_data_loading()))
    results.append(("Data Analysis", test_data_analysis()))
    results.append(("Visualization Generation", test_visualization_generation()))
    results.append(("CLI Availability", test_cli_available()))

    print("\n" + "="*60)
    print("Test Results")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)

    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
