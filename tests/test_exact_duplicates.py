#!/usr/bin/env python
"""
Test the exact duplicate detection with tuning stat.
"""
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.data_processor import detect_duplicates, derive_armor_set_and_base

def test_exact_duplicate_detection():
    """Test that exact duplicates including tuning stat are detected."""
    print("Testing exact duplicate detection with tuning stat...")

    # Create test data
    data = {
        'Name': [
            'Set A Cowl', 'Set B Cowl', 'Set C Cowl', 'Set D Cowl'
        ],
        'Equippable': ['Hunter', 'Hunter', 'Hunter', 'Hunter'],
        'Type': ['Helmet', 'Helmet', 'Helmet', 'Helmet'],
        'Archetype': ['Paragon', 'Paragon', 'Paragon', 'Vanguard'],
        'Tertiary Stat': ['grenade', 'grenade', 'grenade', 'super'],
        'Tuning Stat': ['weapons', 'weapons', 'health', 'weapons']
    }

    df = pd.DataFrame(data)

    # Derive armor set and base item
    df = derive_armor_set_and_base(df)

    # Detect duplicates
    result = detect_duplicates(df)

    print("\n✓ Test Data:")
    for i, row in result.iterrows():
        print(f"  {i+1}. {row['Name']} | {row['Archetype']} | {row['Tertiary Stat']} | {row['Tuning Stat']}")
        print(f"      General Dup: {row['Duplicate Same Archetype+Tertiary Across Sets']}")
        print(f"      Exact Dup: {row['Exact Duplicate (Including Tuning)']}")

    # Verify results
    print("\n✓ Checking detection logic...")

    # Set A and Set B should be EXACT duplicates (same archetype + tertiary + tuning)
    assert result.iloc[0]['Exact Duplicate (Including Tuning)'] and result.iloc[1]['Exact Duplicate (Including Tuning)'], \
        "Set A and Set B should be exact duplicates"
    print("  ✓ Set A and Set B correctly marked as EXACT duplicates (same tuning: weapons)")

    # Set C should be a general duplicate but NOT an exact duplicate (different tuning)
    assert result.iloc[2]['Duplicate Same Archetype+Tertiary Across Sets'] and not result.iloc[2]['Exact Duplicate (Including Tuning)'], \
        "Set C should be general duplicate but NOT exact duplicate"
    print("  ✓ Set C correctly marked as general duplicate only (different tuning: health)")

    # Set D should not be a duplicate at all (different archetype)
    assert not result.iloc[3]['Duplicate Same Archetype+Tertiary Across Sets'] and not result.iloc[3]['Exact Duplicate (Including Tuning)'], \
        "Set D should not be a duplicate"
    print("  ✓ Set D correctly marked as NOT a duplicate (different archetype)")

    # Check columns exist
    assert 'Exact Duplicate (Including Tuning)' in result.columns, \
        "'Exact Duplicate (Including Tuning)' column missing"
    print("  ✓ 'Exact Duplicate (Including Tuning)' column exists")

if __name__ == '__main__':
    print("="*70)
    print("Exact Duplicate Detection Test")
    print("="*70)
    print()

    if test_exact_duplicate_detection():
        print("\n" + "="*70)
        print("✓ ALL TESTS PASSED")
        print("="*70)
        print("\nThe tuning stat grouping feature now works correctly!")
        print("\nFeature Summary:")
        print("  • New column: 'Exact Duplicate (Including Tuning)'")
        print("  • Visible only when toggle is ON")
        print("  • Shows TRUE for exact duplicates (archetype + tertiary + tuning)")
        print("  • Shows FALSE for general duplicates with different tuning")
        print("\nUsage:")
        print("  1. Upload your armor data")
        print("  2. Enable 'Group by Tuning Stat' toggle")
        print("  3. See the new 'Exact Duplicate' column appear")
        print("  4. Items with TRUE are 100% identical (prime for dismantling)")
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("✗ TEST FAILED")
        print("="*70)
        sys.exit(1)

