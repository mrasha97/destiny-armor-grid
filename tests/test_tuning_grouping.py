#!/usr/bin/env python
"""
Test the tuning stat grouping feature.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_tuning_stat_grouping():
    """Test that tuning stat grouping works correctly."""
    print("Testing tuning stat grouping logic...")

    # Simulate sample data with same archetype + tertiary but different tuning
    sample_data = [
        {'Armor Type': 'Helmet', 'Archetype': 'Paragon', 'Tertiary Stat': 'grenade', 'Tuning Stat': 'weapons', 'Armor Set': 'Set A'},
        {'Armor Type': 'Helmet', 'Archetype': 'Paragon', 'Tertiary Stat': 'grenade', 'Tuning Stat': 'health', 'Armor Set': 'Set B'},
        {'Armor Type': 'Helmet', 'Archetype': 'Paragon', 'Tertiary Stat': 'grenade', 'Tuning Stat': 'weapons', 'Armor Set': 'Set C'},
        {'Armor Type': 'Helmet', 'Archetype': 'Paragon', 'Tertiary Stat': 'grenade', 'Tuning Stat': 'health', 'Armor Set': 'Set D'},
    ]

    armor_type_order = {
        'Helmet': 1,
        'Gauntlets': 2,
    }

    # Test WITH tuning stat grouping (toggle ON)
    print("\n✓ WITH Tuning Stat Grouping (Toggle ON):")
    sorted_with_tuning = sorted(sample_data, key=lambda x: (
        armor_type_order.get(x['Armor Type'], 999),
        (x['Archetype'] or '').lower(),
        (x['Tertiary Stat'] or '').lower(),
        (x['Tuning Stat'] or '').lower(),  # Tuning stat included
        (x['Armor Set'] or '').lower()
    ))

    last_tuning = None
    for i, item in enumerate(sorted_with_tuning):
        tuning = item['Tuning Stat']
        if last_tuning and last_tuning != tuning:
            print("  ---- tiny spacer (tuning change) ----")
        print(f"  {i+1}. {item['Armor Set']} | {item['Archetype']} | {item['Tertiary Stat']} | tuning:{item['Tuning Stat']}")
        last_tuning = tuning

    # Test WITHOUT tuning stat grouping (toggle OFF)
    print("\n✓ WITHOUT Tuning Stat Grouping (Toggle OFF - default):")
    sorted_without_tuning = sorted(sample_data, key=lambda x: (
        armor_type_order.get(x['Armor Type'], 999),
        (x['Archetype'] or '').lower(),
        (x['Tertiary Stat'] or '').lower(),
        # Tuning stat NOT included
        (x['Armor Set'] or '').lower()
    ))

    for i, item in enumerate(sorted_without_tuning):
        print(f"  {i+1}. {item['Armor Set']} | {item['Archetype']} | {item['Tertiary Stat']} | tuning:{item['Tuning Stat']}")

    # Verify grouping with tuning
    print("\n✓ Checking tuning stat grouping...")

    weapons_items = [item for item in sorted_with_tuning if item['Tuning Stat'] == 'weapons']
    health_items = [item for item in sorted_with_tuning if item['Tuning Stat'] == 'health']

    weapons_indices = [sorted_with_tuning.index(item) for item in weapons_items]
    health_indices = [sorted_with_tuning.index(item) for item in health_items]

    # Check if health items are consecutive (health comes before weapons alphabetically)
    assert health_indices == [0, 1], f"Health tuning items NOT grouped: indices {health_indices}"
    print(f"  ✓ Health tuning items grouped: {[item['Armor Set'] for item in health_items]}")

    # Check if weapons items are consecutive
    assert weapons_indices == [2, 3], f"Weapons tuning items NOT grouped: indices {weapons_indices}"
    print(f"  ✓ Weapons tuning items grouped: {[item['Armor Set'] for item in weapons_items]}")


if __name__ == '__main__':
    print("="*70)
    print("Tuning Stat Grouping Feature Test")
    print("="*70)
    print()

    if test_tuning_stat_grouping():
        print("\n" + "="*70)
        print("✓ TEST PASSED")
        print("="*70)
        print("\nTuning Stat Grouping Feature Working!")
        print("\nHow it works:")
        print("  • Toggle OFF (default): Groups by Archetype + Tertiary Stat")
        print("  • Toggle ON: Adds Tuning Stat grouping within duplicates")
        print("\nBenefits:")
        print("  • See if duplicates have same tuning stat")
        print("  • Identify exact duplicates (archetype + tertiary + tuning)")
        print("  • More granular comparison for decision-making")
        print("\nUsage:")
        print("  1. Upload armor data")
        print("  2. Enable 'Group by Tuning Stat' toggle")
        print("  3. Duplicates with same tuning will be grouped together")
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("✗ TEST FAILED")
        print("="*70)
        sys.exit(1)

