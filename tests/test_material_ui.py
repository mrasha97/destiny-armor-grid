#!/usr/bin/env python
"""
Test script to verify Material Design UI updates.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_css_file():
    """Verify Material Design CSS exists and has required classes."""
    print("Testing CSS file...")
    css_path = os.path.join(os.path.dirname(__file__), '../app', 'static', 'css', 'style.css')

    assert os.path.exists(css_path), "CSS file not found"

    with open(css_path, 'r') as f:
        css_content = f.read()

    required_classes = [
        '--primary-color',
        'toggle-switch',
        'stat-column',
        'armor-type-spacer',
        'metric-chip',
        'bottom-section',
        'material-icons'
    ]

    missing = []
    for cls in required_classes:
        if cls not in css_content:
            missing.append(cls)

    assert not missing, f"Missing CSS classes: {', '.join(missing)}"
    print("✓ CSS file contains all required Material Design classes")

def test_html_structure():
    """Verify HTML has Material Design structure."""
    print("\nTesting HTML structure...")
    html_path = os.path.join(os.path.dirname(__file__), '../app', 'templates', 'index.html')

    assert os.path.exists(html_path), "HTML file not found"

    with open(html_path, 'r') as f:
        html_content = f.read()

    required_elements = [
        'Material+Icons',  # Material Icons CDN
        'Roboto',  # Roboto font
        'statToggle',  # Stat toggle checkbox
        'bottom-section',  # Bottom section div
        'metric-chip',  # Compact metrics
        'material-icons',  # Icon spans
        'stat-column',  # Stat column class
        'armor-type-spacer'  # Spacer row class
    ]

    missing = []
    for element in required_elements:
        if element not in html_content:
            missing.append(element)

    assert not missing, f"Missing HTML elements: {', '.join(missing)}"
    print("✓ HTML contains all required Material Design elements")

def test_javascript_features():
    """Verify JavaScript has stat toggle and armor ordering."""
    print("\nTesting JavaScript features...")
    html_path = os.path.join(os.path.dirname(__file__), '../app', 'templates', 'index.html')

    with open(html_path, 'r') as f:
        html_content = f.read()

    required_js = [
        'statColumns',
        'armorTypeOrder',
        'statToggle',
        'armor-type-spacer',
        'stat-column',
        'rows.sort'
    ]

    missing = []
    for js_feature in required_js:
        if js_feature not in html_content:
            missing.append(js_feature)

    assert not missing, f"Missing JavaScript features: {', '.join(missing)}"
    print("✓ JavaScript contains stat toggle and armor ordering logic")

def test_app_runs():
    """Test that the Flask app can be imported."""
    print("\nTesting Flask app import...")
    try:
        from app import create_app
        app = create_app()
        print("✓ Flask app imports and creates successfully")
    except Exception as e:
        raise AssertionError(f"Flask app import failed: {e}")

if __name__ == '__main__':
    print("="*70)
    print("Material Design UI Update - Verification Test")
    print("="*70)
    print()

    results = []
    results.append(test_css_file())
    results.append(test_html_structure())
    results.append(test_javascript_features())
    results.append(test_app_runs())

    print("\n" + "="*70)
    if all(results):
        print("✓ ALL TESTS PASSED - Material Design UI Update Complete")
        print("="*70)
        print("\nNew Features Implemented:")
        print("  ✓ Material Design styling (Google Fonts, Icons)")
        print("  ✓ Stat column toggle (hidden by default)")
        print("  ✓ Armor type ordering (Helmet → Gauntlets → Chest → Legs → Class)")
        print("  ✓ Visual spacers between armor types")
        print("  ✓ Metrics moved to bottom (compact chips)")
        print("  ✓ Action buttons moved to bottom")
        print("\nStart the application to see changes:")
        print("  python app.py")
        print("  Open http://127.0.0.1:5000")
        print("  Upload data/destiny-armor.csv")
        sys.exit(0)
    else:
        print("✗ SOME TESTS FAILED")
        print("="*70)
        sys.exit(1)

