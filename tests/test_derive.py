import pandas as pd
import pytest
from app.services.data_processor import derive_armor_set_and_base


def test_derive_armor_set_standard_names():
    """
    Test derivation of Armor Set and Base Item for standard two-word names.
    """
    data = {
        'Name': ['Bushido Cowl', 'Techsec Grips', 'Phoenix Robes']
    }

    df = pd.DataFrame(data)
    result = derive_armor_set_and_base(df)

    assert result.loc[0, 'Armor Set'] == 'Bushido'
    assert result.loc[0, 'Base Item'] == 'Cowl'

    assert result.loc[1, 'Armor Set'] == 'Techsec'
    assert result.loc[1, 'Base Item'] == 'Grips'

    assert result.loc[2, 'Armor Set'] == 'Phoenix'
    assert result.loc[2, 'Base Item'] == 'Robes'


def test_derive_armor_set_multi_word_names():
    """
    Test derivation for armor names with multiple words before the base item.
    """
    data = {
        'Name': ['Iron Banner Helm', 'Trials of Osiris Gauntlets', 'Deep Stone Crypt Plate']
    }

    df = pd.DataFrame(data)
    result = derive_armor_set_and_base(df)

    assert result.loc[0, 'Armor Set'] == 'Iron Banner'
    assert result.loc[0, 'Base Item'] == 'Helm'

    assert result.loc[1, 'Armor Set'] == 'Trials of Osiris'
    assert result.loc[1, 'Base Item'] == 'Gauntlets'

    assert result.loc[2, 'Armor Set'] == 'Deep Stone Crypt'
    assert result.loc[2, 'Base Item'] == 'Plate'


def test_derive_armor_set_single_word():
    """
    Test derivation when name is a single word.
    """
    data = {
        'Name': ['Helmet']
    }

    df = pd.DataFrame(data)
    result = derive_armor_set_and_base(df)

    assert result.loc[0, 'Armor Set'] == 'Helmet'
    assert result.loc[0, 'Base Item'] == ''


def test_derive_armor_set_mixed_formats():
    """
    Test derivation with a mix of name formats.
    """
    data = {
        'Name': [
            'Wildwood Cowl',
            'Exodus Down Vest',
            'Prodigal Boots',
            'Tangled Web Cloak'
        ]
    }

    df = pd.DataFrame(data)
    result = derive_armor_set_and_base(df)

    assert result.loc[0, 'Armor Set'] == 'Wildwood'
    assert result.loc[0, 'Base Item'] == 'Cowl'

    assert result.loc[1, 'Armor Set'] == 'Exodus Down'
    assert result.loc[1, 'Base Item'] == 'Vest'

    assert result.loc[2, 'Armor Set'] == 'Prodigal'
    assert result.loc[2, 'Base Item'] == 'Boots'

    assert result.loc[3, 'Armor Set'] == 'Tangled Web'
    assert result.loc[3, 'Base Item'] == 'Cloak'


def test_derive_preserves_original_name():
    """
    Test that the original Name column is preserved.
    """
    data = {
        'Name': ['Bushido Cowl', 'Techsec Grips']
    }

    df = pd.DataFrame(data)
    result = derive_armor_set_and_base(df)

    assert 'Name' in result.columns
    assert list(result['Name']) == ['Bushido Cowl', 'Techsec Grips']


def test_derive_with_special_characters():
    """
    Test derivation with armor names containing special characters.
    """
    data = {
        'Name': ["Reverie Dawn Helm", "Scatterhorn Vest"]
    }

    df = pd.DataFrame(data)
    result = derive_armor_set_and_base(df)

    assert result.loc[0, 'Armor Set'] == 'Reverie Dawn'
    assert result.loc[0, 'Base Item'] == 'Helm'

    assert result.loc[1, 'Armor Set'] == 'Scatterhorn'
    assert result.loc[1, 'Base Item'] == 'Vest'

