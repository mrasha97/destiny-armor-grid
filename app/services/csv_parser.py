import pandas as pd
from typing import List, Tuple


class CSVParserError(Exception):
    """Custom exception for CSV parsing errors."""
    pass


REQUIRED_COLUMNS = [
    'Name', 'Rarity', 'Tier', 'Type', 'Equippable', 'Archetype',
    'Tertiary Stat', 'Tuning Stat', 'Weapons', 'Health', 'Class',
    'Grenade', 'Super', 'Melee', 'Total'
]


def validate_csv_schema(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate that the DataFrame contains all required columns.

    Args:
        df: Input DataFrame to validate

    Returns:
        Tuple of (is_valid, missing_columns)
    """
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return len(missing_columns) == 0, missing_columns


def parse_csv(file_path: str) -> pd.DataFrame:
    """
    Parse and validate CSV file with Destiny 2 armor data.

    Args:
        file_path: Path to the CSV file

    Returns:
        DataFrame containing validated armor data

    Raises:
        CSVParserError: If CSV is invalid or missing required columns
    """
    try:
        df = pd.read_csv(file_path)

        if df.empty:
            raise CSVParserError("CSV file is empty")

        is_valid, missing = validate_csv_schema(df)
        if not is_valid:
            raise CSVParserError(
                f"Missing required columns: {', '.join(missing)}"
            )

        return df

    except pd.errors.EmptyDataError:
        raise CSVParserError("CSV file is empty or corrupted")
    except pd.errors.ParserError as e:
        raise CSVParserError(f"Failed to parse CSV: {str(e)}")
    except Exception as e:
        if isinstance(e, CSVParserError):
            raise
        raise CSVParserError(f"Error reading CSV file: {str(e)}")

