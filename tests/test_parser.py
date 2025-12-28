import pandas as pd
import pytest
import tempfile
import os
from app.services.csv_parser import (
    parse_csv, validate_csv_schema, CSVParserError, REQUIRED_COLUMNS
)


def test_validate_csv_schema_valid():
    """
    Test schema validation with all required columns present.
    """
    df = pd.DataFrame(columns=REQUIRED_COLUMNS)
    is_valid, missing = validate_csv_schema(df)

    assert is_valid is True
    assert len(missing) == 0


def test_validate_csv_schema_missing_columns():
    """
    Test schema validation with missing required columns.
    """
    df = pd.DataFrame(columns=['Name', 'Rarity', 'Tier'])
    is_valid, missing = validate_csv_schema(df)

    assert is_valid is False
    assert len(missing) > 0
    assert 'Type' in missing
    assert 'Equippable' in missing


def test_parse_csv_valid_file():
    """
    Test parsing a valid CSV file.
    """
    data = {col: ['test'] for col in REQUIRED_COLUMNS}
    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_path = f.name

    try:
        result = parse_csv(temp_path)
        assert len(result) == 1
        assert all(col in result.columns for col in REQUIRED_COLUMNS)
    finally:
        os.unlink(temp_path)


def test_parse_csv_empty_file():
    """
    Test parsing an empty CSV file raises appropriate error.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('')
        temp_path = f.name

    try:
        with pytest.raises(CSVParserError) as exc_info:
            parse_csv(temp_path)
        assert 'empty' in str(exc_info.value).lower()
    finally:
        os.unlink(temp_path)


def test_parse_csv_missing_columns():
    """
    Test parsing CSV with missing required columns.
    """
    df = pd.DataFrame({'Name': ['Item1'], 'Rarity': ['Legendary']})

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_path = f.name

    try:
        with pytest.raises(CSVParserError) as exc_info:
            parse_csv(temp_path)
        assert 'Missing required columns' in str(exc_info.value)
    finally:
        os.unlink(temp_path)


def test_parse_csv_malformed():
    """
    Test parsing a malformed CSV file.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('Name,Rarity\n')
        f.write('Item1,Legendary,ExtraColumn\n')
        temp_path = f.name

    try:
        with pytest.raises(CSVParserError):
            parse_csv(temp_path)
    finally:
        os.unlink(temp_path)


def test_parse_csv_case_sensitive_columns():
    """
    Test that column names are case-sensitive.
    """
    data = {col.lower(): ['test'] for col in REQUIRED_COLUMNS}
    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_path = f.name

    try:
        with pytest.raises(CSVParserError) as exc_info:
            parse_csv(temp_path)
        assert 'Missing required columns' in str(exc_info.value)
    finally:
        os.unlink(temp_path)


def test_parse_csv_with_data():
    """
    Test parsing CSV with actual armor data.
    """
    data = {
        'Name': ['Bushido Cowl', 'Techsec Grips'],
        'Rarity': ['Legendary', 'Legendary'],
        'Tier': [5, 5],
        'Type': ['Helmet', 'Gauntlets'],
        'Equippable': ['Hunter', 'Hunter'],
        'Archetype': ['Paragon', 'Vanguard'],
        'Tertiary Stat': ['grenade', 'melee'],
        'Tuning Stat': ['weapons', 'health'],
        'Weapons': [10, 12],
        'Health': [8, 9],
        'Class': [15, 14],
        'Grenade': [20, 18],
        'Super': [12, 13],
        'Melee': [9, 11],
        'Total': [74, 77]
    }
    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_path = f.name

    try:
        result = parse_csv(temp_path)
        assert len(result) == 2
        assert result.loc[0, 'Name'] == 'Bushido Cowl'
        assert result.loc[1, 'Name'] == 'Techsec Grips'
    finally:
        os.unlink(temp_path)

