#!/usr/bin/env python3
"""
Test AI Analytics Feature
"""

import sys
from agentic_graphs import AutonomousGraphSystem

def test_analytics_only():
    """Test analytics without visualization"""
    print("="*70)
    print("Test 1: Analytics Only")
    print("="*70)

    system = AutonomousGraphSystem(verbose=True)

    report = system.run_analytics('data/3d_scatter_sample.csv')

    assert report is not None
    assert len(report.insights) > 0
    assert report.natural_language_summary
    print("\n✓ Test 1 passed!")

    return report


def test_analytics_with_viz():
    """Test analytics with visualization"""
    print("\n" + "="*70)
    print("Test 2: Analytics with Visualization")
    print("="*70)

    system = AutonomousGraphSystem(verbose=True)

    fig, report = system.generate_with_analytics(
        'data/network_sample.csv',
        output_path='examples/test_analytics_network.html',
        show=False
    )

    assert fig is not None
    assert report is not None
    assert len(report.insights) > 0
    print("\n✓ Test 2 passed!")

    return fig, report


def test_analytics_export():
    """Test analytics report export"""
    print("\n" + "="*70)
    print("Test 3: Analytics Export")
    print("="*70)

    system = AutonomousGraphSystem(verbose=True)

    report = system.run_analytics(
        'data/3d_scatter_sample.csv',
        export_path='examples/analytics_report.json'
    )

    import json
    from pathlib import Path

    analytics_file = Path('examples/analytics_report.json')
    assert analytics_file.exists(), "Analytics file not created"

    with open(analytics_file) as f:
        data = json.load(f)

    assert 'insights' in data
    assert 'recommendations' in data
    assert 'summary' in data
    print("\n✓ Test 3 passed!")
    print(f"✓ Analytics exported to: {analytics_file}")

    return report


def main():
    """Run all analytics tests"""
    print("🤖 AI ANALYTICS TESTING SUITE")
    print("="*70)

    try:
        # Test 1
        report1 = test_analytics_only()

        # Test 2
        fig, report2 = test_analytics_with_viz()

        # Test 3
        report3 = test_analytics_export()

        # Summary
        print("\n" + "="*70)
        print("✅ ALL ANALYTICS TESTS PASSED")
        print("="*70)

        print("\nSample Insights from Test 1:")
        for i, insight in enumerate(report1.insights[:3], 1):
            print(f"\n{i}. {insight.title}")
            print(f"   {insight.description}")
            print(f"   Confidence: {insight.confidence:.0%}")

        print("\n" + "="*70)
        return 0

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
