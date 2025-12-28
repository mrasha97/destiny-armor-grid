import pandas as pd
import pytest
from app.services.data_processor import filter_armor


def test_filter_removes_exotics():
    """
    Test that all Exotic rarity items are removed.
    """
    data = {
        'Name': ['Item1', 'Item2', 'Item3'],
        'Rarity': ['Exotic', 'Legendary', 'Legendary'],
        'Tier': [5, 5, 5],
        'Type': ['Helmet', 'Helmet', 'Helmet'],
        'Equippable': ['Hunter', 'Hunter', 'Hunter']
    }

    df = pd.DataFrame(data)
    result = filter_armor(df)

    assert len(result) == 2, "Should keep only 2 Legendary items"
    assert 'Exotic' not in result['Rarity'].values, "No Exotic items should remain"


def test_filter_removes_non_tier_5():
    """
    Test that non-Tier 5 Legendary items are removed.
    """
    data = {
        'Name': ['Item1', 'Item2', 'Item3', 'Item4'],
        'Rarity': ['Legendary', 'Legendary', 'Legendary', 'Legendary'],
        'Tier': [5, 4, 3, 5],
        'Type': ['Helmet', 'Helmet', 'Helmet', 'Helmet'],
        'Equippable': ['Hunter', 'Hunter', 'Hunter', 'Hunter']
    }

    df = pd.DataFrame(data)
    result = filter_armor(df)

    assert len(result) == 2, "Should keep only 2 Tier 5 items"
    assert all(result['Tier'] == 5), "All remaining items should be Tier 5"


def test_filter_removes_both_exotic_and_non_tier_5():
    """
    Test combined filtering of Exotics and non-Tier 5 items.
    """
    data = {
        'Name': ['Item1', 'Item2', 'Item3', 'Item4', 'Item5'],
        'Rarity': ['Exotic', 'Legendary', 'Legendary', 'Legendary', 'Exotic'],
        'Tier': [5, 5, 4, 5, 3],
        'Type': ['Helmet', 'Helmet', 'Helmet', 'Helmet', 'Helmet'],
        'Equippable': ['Hunter', 'Hunter', 'Hunter', 'Hunter', 'Hunter']
    }

    df = pd.DataFrame(data)
    result = filter_armor(df)

    assert len(result) == 2, "Should keep only 2 Legendary Tier 5 items"
    assert all(result['Rarity'] == 'Legendary'), "All items should be Legendary"
    assert all(result['Tier'] == 5), "All items should be Tier 5"


def test_filter_empty_result():
    """
    Test that filtering can result in an empty DataFrame.
    """
    data = {
        'Name': ['Item1', 'Item2'],
        'Rarity': ['Exotic', 'Exotic'],
        'Tier': [5, 5],
        'Type': ['Helmet', 'Helmet'],
        'Equippable': ['Hunter', 'Hunter']
    }

    df = pd.DataFrame(data)
    result = filter_armor(df)

    assert len(result) == 0, "Should return empty DataFrame when no items match"


def test_filter_keeps_all_legendary_tier_5():
    """
    Test that all Legendary Tier 5 items are kept.
    """
    data = {
        'Name': ['Item1', 'Item2', 'Item3'],
        'Rarity': ['Legendary', 'Legendary', 'Legendary'],
        'Tier': [5, 5, 5],
        'Type': ['Helmet', 'Gauntlets', 'Chest Armor'],
        'Equippable': ['Hunter', 'Warlock', 'Titan']
    }

    df = pd.DataFrame(data)
    result = filter_armor(df)

    assert len(result) == 3, "Should keep all 3 Legendary Tier 5 items"
    assert list(result['Name']) == ['Item1', 'Item2', 'Item3']

