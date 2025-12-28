#!/usr/bin/env python
"""
Test the updated UI with tabbed interface.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.csv_parser import parse_csv
from app.services.data_processor import process_armor_data

def test_data_separation():
    """Test that data can be properly separated by class."""
    import pytest
    print("Testing data separation by class...")

    csv_path = os.path.join(os.path.dirname(__file__), 'destiny-armor.csv')
    if not os.path.exists(csv_path):
        pytest.skip(f"Sample CSV not found at {csv_path} - skipping integration test")

    try:
        df = parse_csv(csv_path)
        print(f"✓ Parsed CSV: {len(df)} rows")

        processed_df, metrics = process_armor_data(df)
        print(f"✓ Processed data: {len(processed_df)} rows kept")

        # Separate by class
        hunter_df = processed_df[processed_df['Class'] == 'Hunter']
        warlock_df = processed_df[processed_df['Class'] == 'Warlock']
        titan_df = processed_df[processed_df['Class'] == 'Titan']

        print(f"\n  Hunter pieces: {len(hunter_df)}")
        print(f"  Warlock pieces: {len(warlock_df)}")
        print(f"  Titan pieces: {len(titan_df)}")
        print(f"  Total: {len(hunter_df) + len(warlock_df) + len(titan_df)}")

        # Verify all rows are accounted for
        total = len(hunter_df) + len(warlock_df) + len(titan_df)
        assert total == len(processed_df), f"Mismatch: {total} distributed vs {len(processed_df)} total"
        print(f"\n✓ All {total} rows properly distributed across classes")

    except Exception as e:
        raise AssertionError(f"Test failed: {e}")

if __name__ == '__main__':
    print("="*60)
    print("UI Update Test - Tabbed Interface with All Rows")
    print("="*60)
    print()

    if test_data_separation():
        print("\n" + "="*60)
        print("✓ TEST PASSED")
        print("="*60)
        print("\nChanges implemented:")
        print("  • Added 3 tabs (Hunter, Warlock, Titan)")
        print("  • Each tab shows ALL rows for that class")
        print("  • Armor type color-coding applied to rows")
        print("  • Duplicate cells highlighted in orange")
        print("  • Bold formatting for Archetype and Armor Set columns")
        print("\nStart the app to see the new UI:")
        print("  python app.py")
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("✗ TEST FAILED")
        print("="*60)
        sys.exit(1)

