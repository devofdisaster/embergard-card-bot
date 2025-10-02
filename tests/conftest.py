"""
Test configuration and fixtures for the Embergard Card Bot test suite.
This file provides pytest fixtures that can be used across multiple test files.
"""

import os
import tempfile
from typing import Generator, Tuple

import pandas as pd
import pytest


@pytest.fixture
def sample_cards_data() -> pd.DataFrame:
    """Create a sample cards DataFrame for testing."""
    return pd.DataFrame(
        {
            "Set": ["Embergard", "Embergard", "Embergard", "Beastgrave"],
            "Number": ["BL1", "BL2", "BL3", "BG1"],
            "Name": [
                "Strike the Head",
                "Branching Fate",
                "Perfect Strike",
                "Mollog's Mob",
            ],
            "Type": ["Objective", "Objective", "Objective", "Fighter"],
            "Glory/Cost": [1, 1, 1, "-"],
            "Description": [
                "Score this immediately after an enemy fighter is slain by a friendly fighter if the target was a **leader**.",
                "Score this immediately after you make an Attack roll that contained 3 or more dice.",
                "Score this immediately after you make an Attack roll if all of the results were successes.",
                "A mighty troggoth warlord leading his grots.",
            ],
            "ObjType": ["Surge", "Surge", "Surge", "-"],
            "Restrictions": ["-", "-", "-", "-"],
            "Deck": [
                "Blazing Assault Rivals Deck",
                "Blazing Assault Rivals Deck",
                "Blazing Assault Rivals Deck",
                "Mollog's Mob",
            ],
            "Forsaken": ["", "", "", ""],
            "Restricted": ["", "", "", ""],
            "Rotated": ["", "", "", ""],
            "CustomImage": ["", "", "", ""],
        }
    )


@pytest.fixture
def sample_warbands_data() -> pd.DataFrame:
    """Create a sample warbands DataFrame for testing."""
    return pd.DataFrame(
        {
            "Warband": [
                "Grand Alliance Order",
                "Grand Alliance Order",
                "Grand Alliance Chaos",
                "Domitan's Stormcoven",
                "Mollog's Mob",
                "Mollog's Mob",
            ],
            "Name": [
                "Grand Alliance Order: Crusaders",
                "Grand Alliance Order: Protectors",
                "Grand Alliance Chaos: Corrupters",
                "Domitan's Stormcoven",
                "Mollog",
                "Bat Squig",
            ],
            "ImageNumber": [1, 2, 1, 0, 1, 2],
            "WarscrollType": [
                "alliance",
                "alliance",
                "alliance",
                "generic",
                None,
                None,
            ],
            "GrandAlliance": ["", "", "", "Grand Alliance Order", "", ""],
        }
    )


@pytest.fixture
def temp_csv_files(
    sample_cards_data: pd.DataFrame, sample_warbands_data: pd.DataFrame
) -> Generator[Tuple[str, str], None, None]:
    """Create temporary CSV files for testing with automatic cleanup."""
    cards_file = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
    sample_cards_data.to_csv(cards_file.name, index=False)
    cards_file.close()

    warbands_file = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
    sample_warbands_data.to_csv(warbands_file.name, index=False)
    warbands_file.close()

    yield cards_file.name, warbands_file.name

    # Cleanup after test
    try:
        os.unlink(cards_file.name)
        os.unlink(warbands_file.name)
    except OSError:
        pass


def cleanup_temp_files(cards_path: str, warbands_path: str) -> None:
    """Clean up temporary CSV files."""
    try:
        os.unlink(cards_path)
        os.unlink(warbands_path)
    except OSError:
        pass  # Files might already be deleted


@pytest.fixture
def library_with_data(temp_csv_files):
    """Create a Library instance with test data loaded."""
    from src.card_library import Library

    cards_path, warbands_path = temp_csv_files
    library = Library(card_path=cards_path, warband_path=warbands_path)
    library.load()
    return library
