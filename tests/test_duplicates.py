import pandas as pd
import pytest
from app.services.data_processor import detect_duplicates


def test_duplicate_detection_across_different_sets():
    """
    Test that duplicates are correctly identified when the same
    Base Item + Archetype + Tertiary Stat combination exists
    across different Armor Sets.
    """
    data = {
        'Equippable': ['Hunter', 'Hunter', 'Hunter'],
        'Type': ['Helmet', 'Helmet', 'Helmet'],
        'Base Item': ['Cowl', 'Cowl', 'Cowl'],
        'Archetype': ['Paragon', 'Paragon', 'Paragon'],
        'Tertiary Stat': ['grenade', 'grenade', 'grenade'],
        'Tuning Stat': ['Mobility', 'Mobility', 'Mobility'],
        'Armor Set': ['Bushido', 'Techsec', 'Wildwood'],
        'Name': ['Bushido Cowl', 'Techsec Cowl', 'Wildwood Cowl']
    }

    df = pd.DataFrame(data)
    result = detect_duplicates(df)

    assert result['Duplicate Same Archetype+Tertiary Across Sets'].all(), \
        "All three items should be marked as duplicates"


def test_no_duplicate_when_same_set():
    """
    Test that items from the same Armor Set are not marked as duplicates.
    """
    data = {
        'Equippable': ['Hunter', 'Hunter'],
        'Type': ['Helmet', 'Gauntlets'],
        'Base Item': ['Cowl', 'Grips'],
        'Archetype': ['Paragon', 'Paragon'],
        'Tertiary Stat': ['grenade', 'grenade'],
        'Tuning Stat': ['Mobility', 'Mobility'],
        'Armor Set': ['Bushido', 'Bushido'],
        'Name': ['Bushido Cowl', 'Bushido Grips']
    }

    df = pd.DataFrame(data)
    result = detect_duplicates(df)

    assert not result['Duplicate Same Archetype+Tertiary Across Sets'].any(), \
        "Items from same set with different base items should not be duplicates"


def test_no_duplicate_when_different_archetype():
    """
    Test that items are not marked as duplicates if Archetype differs.
    """
    data = {
        'Equippable': ['Hunter', 'Hunter'],
        'Type': ['Helmet', 'Helmet'],
        'Base Item': ['Cowl', 'Cowl'],
        'Archetype': ['Paragon', 'Vanguard'],
        'Tertiary Stat': ['grenade', 'grenade'],
        'Tuning Stat': ['Mobility', 'Mobility'],
        'Armor Set': ['Bushido', 'Techsec'],
        'Name': ['Bushido Cowl', 'Techsec Cowl']
    }

    df = pd.DataFrame(data)
    result = detect_duplicates(df)

    assert not result['Duplicate Same Archetype+Tertiary Across Sets'].any(), \
        "Items with different Archetype should not be duplicates"


def test_no_duplicate_when_different_tertiary():
    """
    Test that items are not marked as duplicates if Tertiary Stat differs.
    """
    data = {
        'Equippable': ['Hunter', 'Hunter'],
        'Type': ['Helmet', 'Helmet'],
        'Base Item': ['Cowl', 'Cowl'],
        'Archetype': ['Paragon', 'Paragon'],
        'Tertiary Stat': ['grenade', 'melee'],
        'Tuning Stat': ['Mobility', 'Mobility'],
        'Armor Set': ['Bushido', 'Techsec'],
        'Name': ['Bushido Cowl', 'Techsec Cowl']
    }

    df = pd.DataFrame(data)
    result = detect_duplicates(df)

    assert not result['Duplicate Same Archetype+Tertiary Across Sets'].any(), \
        "Items with different Tertiary Stat should not be duplicates"


def test_no_duplicate_when_different_base_item():
    """
    Test that items are not marked as duplicates if Base Item differs.
    """
    data = {
        'Equippable': ['Hunter', 'Hunter'],
        'Type': ['Helmet', 'Helmet'],
        'Base Item': ['Cowl', 'Mask'],
        'Archetype': ['Paragon', 'Paragon'],
        'Tertiary Stat': ['grenade', 'grenade'],
        'Tuning Stat': ['Mobility', 'Mobility'],
        'Armor Set': ['Bushido', 'Techsec'],
        'Name': ['Bushido Cowl', 'Techsec Mask']
    }

    df = pd.DataFrame(data)
    result = detect_duplicates(df)

    assert not result['Duplicate Same Archetype+Tertiary Across Sets'].any(), \
        "Items with different Base Item should not be duplicates"


def test_duplicate_detection_two_sets():
    """
    Test duplicate detection with exactly two different sets.
    """
    data = {
        'Equippable': ['Warlock', 'Warlock'],
        'Type': ['Gauntlets', 'Gauntlets'],
        'Base Item': ['Gloves', 'Gloves'],
        'Archetype': ['Vanguard', 'Vanguard'],
        'Tertiary Stat': ['super', 'super'],
        'Tuning Stat': ['Recovery', 'Recovery'],
        'Armor Set': ['Phoenix', 'Scorched'],
        'Name': ['Phoenix Gloves', 'Scorched Gloves']
    }

    df = pd.DataFrame(data)
    result = detect_duplicates(df)

    assert result['Duplicate Same Archetype+Tertiary Across Sets'].all(), \
        "Both items should be marked as duplicates"


def test_mixed_duplicate_and_unique():
    """
    Test a dataset with some duplicates and some unique items.
    """
    data = {
        'Equippable': ['Titan', 'Titan', 'Titan', 'Titan'],
        'Type': ['Chest Armor', 'Chest Armor', 'Leg Armor', 'Leg Armor'],
        'Base Item': ['Plate', 'Plate', 'Greaves', 'Greaves'],
        'Archetype': ['Crucible', 'Crucible', 'Striker', 'Defender'],
        'Tertiary Stat': ['melee', 'melee', 'class', 'class'],
        'Tuning Stat': ['Resilience', 'Resilience', 'Resilience', 'Resilience'],
        'Armor Set': ['Iron', 'Steel', 'Iron', 'Steel'],
        'Name': ['Iron Plate', 'Steel Plate', 'Iron Greaves', 'Steel Greaves']
    }

    df = pd.DataFrame(data)
    result = detect_duplicates(df)

    assert result.loc[0, 'Duplicate Same Archetype+Tertiary Across Sets'] == True
    assert result.loc[1, 'Duplicate Same Archetype+Tertiary Across Sets'] == True
    assert result.loc[2, 'Duplicate Same Archetype+Tertiary Across Sets'] == False
    assert result.loc[3, 'Duplicate Same Archetype+Tertiary Across Sets'] == False

