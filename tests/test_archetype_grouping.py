#!/usr/bin/env python
"""
Test the archetype grouping logic.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_grouping_logic():
    """Test that duplicates will be grouped together with the new sorting."""
    print("Testing archetype grouping logic...")

    # Simulate sample data
    sample_data = [
        {'Armor Type': 'Helmet', 'Archetype': 'Paragon', 'Tertiary Stat': 'grenade', 'Armor Set': 'Wildwood', 'Name': 'Wildwood Cowl'},
        {'Armor Type': 'Helmet', 'Archetype': 'Paragon', 'Tertiary Stat': 'grenade', 'Armor Set': 'Bushido', 'Name': 'Bushido Cowl'},
        {'Armor Type': 'Helmet', 'Archetype': 'Vanguard', 'Tertiary Stat': 'super', 'Armor Set': 'Phoenix', 'Name': 'Phoenix Cowl'},
        {'Armor Type': 'Helmet', 'Archetype': 'Paragon', 'Tertiary Stat': 'grenade', 'Armor Set': 'Techsec', 'Name': 'Techsec Cowl'},
        {'Armor Type': 'Gauntlets', 'Archetype': 'Crucible', 'Tertiary Stat': 'melee', 'Armor Set': 'Set A', 'Name': 'Set A Grips'},
        {'Armor Type': 'Helmet', 'Archetype': 'Paragon', 'Tertiary Stat': 'melee', 'Armor Set': 'Set B', 'Name': 'Set B Cowl'},
    ]

    # Define armor type order (matching the JavaScript)
    armor_type_order = {
        'Helmet': 1,
        'Gauntlets': 2,
        'Chest Armor': 3,
        'Leg Armor': 4,
        'Hunter Cloak': 5,
        'Warlock Bond': 5,
        'Titan Mark': 5
    }

    # Sort using the same logic as JavaScript
    sorted_data = sorted(sample_data, key=lambda x: (
        armor_type_order.get(x['Armor Type'], 999),
        (x['Archetype'] or '').lower(),
        (x['Tertiary Stat'] or '').lower(),
        (x['Armor Set'] or '').lower()
    ))

    print("\n✓ Sorted order:")
    last_armor_type = None
    last_archetype = None

    for i, item in enumerate(sorted_data):
        armor_type = item['Armor Type']
        archetype = item['Archetype']

        # Show spacers
        if last_armor_type and last_armor_type != armor_type:
            print("  --- LARGE SPACER (armor type change) ---")
            last_archetype = None
        elif last_archetype and last_archetype != archetype:
            print("  - small spacer (archetype change) -")

        print(f"{i+1}. {item['Name']} | {armor_type} | {archetype} | {item['Tertiary Stat']}")

        last_armor_type = armor_type
        last_archetype = archetype

    # Verify duplicates are grouped
    print("\n✓ Checking duplicate grouping...")

    # Find the three Paragon/grenade helmets
    paragon_grenade_helmets = [
        (i, item) for i, item in enumerate(sorted_data)
        if item['Armor Type'] == 'Helmet'
        and item['Archetype'] == 'Paragon'
        and item['Tertiary Stat'] == 'grenade'
    ]

    assert len(paragon_grenade_helmets) == 3, \
        f"Expected 3 Paragon/grenade helmets, found {len(paragon_grenade_helmets)}"

    indices = [i for i, _ in paragon_grenade_helmets]
    names = [item['Armor Set'] for _, item in paragon_grenade_helmets]

    # Check if they're consecutive
    if indices == [0, 1, 2]:  # Should be first three items
        print(f"  ✓ Duplicates grouped together: {', '.join(names)}")
        print(f"  ✓ Indices: {indices} (consecutive)")
    else:
        print(f"  ✗ Duplicates NOT consecutive: indices {indices}")

    assert indices == [0, 1, 2], f"Duplicates NOT consecutive: indices {indices}"

if __name__ == '__main__':
    print("="*70)
    print("Archetype Grouping Logic Test")
    print("="*70)
    print()

    if test_grouping_logic():
        print("\n" + "="*70)
        print("✓ TEST PASSED")
        print("="*70)
        print("\nDuplicates will be grouped together!")
        print("Sort order: Armor Type → Archetype → Tertiary Stat → Armor Set")
        print("\nBenefits:")
        print("  • Easy to compare duplicate armor pieces")
        print("  • Visual grouping with spacers")
        print("  • Quick decision-making on which to keep")
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("✗ TEST FAILED")
        print("="*70)
        sys.exit(1)

