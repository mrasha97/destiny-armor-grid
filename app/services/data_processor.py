import pandas as pd
from typing import Tuple


def filter_armor(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter armor data to keep only Legendary Tier 5 items.

    Args:
        df: Input DataFrame with armor data

    Returns:
        Filtered DataFrame
    """
    filtered = df[
        (df['Rarity'] == 'Legendary') &
        (df['Tier'] == 5)
    ].copy()

    return filtered


def derive_armor_set_and_base(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive Armor Set and Base Item columns from Name.

    Args:
        df: DataFrame with Name column

    Returns:
        DataFrame with added Armor Set and Base Item columns
    """
    df = df.copy()

    name_parts = df['Name'].str.rsplit(' ', n=1, expand=True)

    df['Base Item'] = name_parts[1] if 1 in name_parts.columns else ''
    df['Armor Set'] = name_parts[0] if 0 in name_parts.columns else df['Name']

    return df


def detect_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect duplicates based on exact matching criteria across different Armor Sets.

    A duplicate is defined as: Multiple distinct Armor Sets exist for the same
    combination of (Class, Armor Type, Base Item, Archetype, Tertiary Stat).

    Also detects exact duplicates including Tuning Stat.

    Args:
        df: DataFrame with armor data including derived columns

    Returns:
        DataFrame with added duplicate columns
    """
    df = df.copy()

    # Detect duplicates by Archetype + Tertiary Stat
    grouping_cols = ['Equippable', 'Type', 'Base Item', 'Archetype', 'Tertiary Stat']

    df['Duplicate Same Archetype+Tertiary Across Sets'] = False

    grouped = df.groupby(grouping_cols)['Armor Set'].nunique()

    duplicate_groups = grouped[grouped > 1].index

    for group_key in duplicate_groups:
        mask = True
        for i, col in enumerate(grouping_cols):
            mask = mask & (df[col] == group_key[i])
        df.loc[mask, 'Duplicate Same Archetype+Tertiary Across Sets'] = True

    # Detect exact duplicates including Tuning Stat
    exact_grouping_cols = ['Equippable', 'Type', 'Base Item', 'Archetype', 'Tertiary Stat', 'Tuning Stat']

    df['Exact Duplicate (Including Tuning)'] = False

    exact_grouped = df.groupby(exact_grouping_cols)['Armor Set'].nunique()

    exact_duplicate_groups = exact_grouped[exact_grouped > 1].index

    for group_key in exact_duplicate_groups:
        mask = True
        for i, col in enumerate(exact_grouping_cols):
            mask = mask & (df[col] == group_key[i])
        df.loc[mask, 'Exact Duplicate (Including Tuning)'] = True

    return df


def sort_armor(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sort armor data by specified hierarchy.

    Args:
        df: DataFrame with armor data

    Returns:
        Sorted DataFrame
    """
    return df.sort_values(
        by=['Equippable', 'Type', 'Archetype', 'Armor Set', 'Base Item', 'Name'],
        ascending=True
    ).reset_index(drop=True)


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename columns for clarity in final output.

    Args:
        df: DataFrame with processed armor data

    Returns:
        DataFrame with renamed columns
    """
    column_mapping = {
        'Equippable': 'Class',
        'Type': 'Armor Type',
        'Name': 'Armor Name',
        'Weapons': 'Weapons Stat',
        'Health': 'Health Stat',
        'Class': 'Class Stat',
        'Grenade': 'Grenade Stat',
        'Super': 'Super Stat',
        'Melee': 'Melee Stat',
        'Total': 'Total Stat'
    }

    return df.rename(columns=column_mapping)


def process_armor_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    """
    Complete data processing pipeline for armor data.

    Args:
        df: Raw DataFrame from CSV

    Returns:
        Tuple of (processed DataFrame, metrics dictionary)
    """
    initial_count = len(df)

    filtered = filter_armor(df)
    filtered_count = len(filtered)

    derived = derive_armor_set_and_base(filtered)

    with_duplicates = detect_duplicates(derived)
    duplicate_count = with_duplicates['Duplicate Same Archetype+Tertiary Across Sets'].sum()

    sorted_df = sort_armor(with_duplicates)

    final_df = rename_columns(sorted_df)

    output_columns = [
        'Class', 'Armor Type', 'Armor Name', 'Archetype', 'Tertiary Stat',
        'Tuning Stat', 'Armor Set', 'Base Item', 'Weapons Stat', 'Health Stat',
        'Class Stat', 'Grenade Stat', 'Super Stat', 'Melee Stat', 'Total Stat',
        'Duplicate Same Archetype+Tertiary Across Sets',
        'Exact Duplicate (Including Tuning)'
    ]

    final_df = final_df[output_columns]

    metrics = {
        'initial_count': initial_count,
        'filtered_count': filtered_count,
        'duplicate_count': int(duplicate_count),
        'removed_count': initial_count - filtered_count
    }

    return final_df, metrics

