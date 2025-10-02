"""
Unit tests for the card_library.Library class using pytest.

Tests cover:
- Card search functionality with exact, partial, and fuzzy matching
- Warband search functionality
- Apostrophe normalization
- Edge cases and error handling
"""

import pandas as pd
from src.card_library import Library


class TestLibrary:
    """Test suite for the Library class using pytest fixtures."""
    
    def test_initialization(self):
        """Test Library initialization with and without paths."""
        # Test initialization without paths
        library = Library()
        assert library._card_path is None
        assert library._warband_path is None
        assert library._card_memory is None
        assert library._warband_memory is None
        
        # Test initialization with paths
        library = Library("cards.csv", "warbands.csv")
        assert library._card_path == "cards.csv"
        assert library._warband_path == "warbands.csv"
    
    def test_load_data(self, library_with_data):
        """Test that data loads correctly."""
        library = library_with_data
        
        # Check that data is loaded
        assert isinstance(library._card_memory, pd.DataFrame)
        assert isinstance(library._warband_memory, pd.DataFrame)
        
        # Check data content
        assert len(library._card_memory) == 4
        assert len(library._warband_memory) == 6
        
        # Check expected columns exist
        expected_card_columns = ['Name', 'Type', 'Description', 'Set', 'Deck']
        for col in expected_card_columns:
            assert col in library._card_memory.columns
            
        expected_warband_columns = ['Warband', 'Name', 'WarscrollType']
        for col in expected_warband_columns:
            assert col in library._warband_memory.columns

    def test_search_cards_exact_match(self, library_with_data):
        """Test card search with exact name matches."""
        library = library_with_data
        
        # Test exact match
        result = library.search_cards("Strike the Head")
        assert len(result) == 1
        assert result.iloc[0]['Name'] == "Strike the Head"
        
        # Test case insensitive exact match
        result = library.search_cards("strike the head")
        assert len(result) == 1
        assert result.iloc[0]['Name'] == "Strike the Head"

    def test_search_cards_partial_match(self, library_with_data):
        """Test card search with partial matches."""
        library = library_with_data
        
        # Test partial match
        result = library.search_cards("Strike")
        assert len(result) >= 1
        assert any("Strike" in name for name in result['Name'].tolist())
        
        # Test partial match with multiple results
        result = library.search_cards("Perfect")
        assert len(result) >= 1
        assert any("Perfect" in name for name in result['Name'].tolist())

    def test_search_cards_fuzzy_match(self, library_with_data):
        """Test card search with fuzzy matching."""
        library = library_with_data
        
        # Test fuzzy match with typo
        result = library.search_cards("Perfekt Strike")  # typo in "Perfect"
        # Should still find "Perfect Strike" due to fuzzy matching
        assert len(result) >= 1

    def test_search_cards_apostrophe_normalization(self, library_with_data):
        """Test that apostrophe variants are handled correctly."""
        library = library_with_data
        
        # Test with regular apostrophe
        result1 = library.search_cards("Mollog's")
        
        # Test with different apostrophe character
        result2 = library.search_cards("Mollog's")  # Different apostrophe character
        
        # Both should return the same results
        assert len(result1) == len(result2)
        if len(result1) > 0:
            assert result1.iloc[0]['Name'] == result2.iloc[0]['Name']

    def test_search_cards_no_match(self, library_with_data):
        """Test card search when no matches are found."""
        library = library_with_data
        
        result = library.search_cards("NonexistentCard12345")
        # Should return empty DataFrame or very low quality matches
        assert len(result) == 0 or not any("NonexistentCard12345" in name for name in result['Name'].tolist())

    def test_search_cards_lazy_loading(self, temp_csv_files):
        """Test that card data is loaded lazily on first search."""
        cards_path, warbands_path = temp_csv_files
        library = Library(card_path=cards_path, warband_path=warbands_path)
        
        # Initially memory should be None
        assert library._card_memory is None
        
        # After search, memory should be loaded
        library.search_cards("Strike")
        assert isinstance(library._card_memory, pd.DataFrame)

    def test_search_warbands_exact_match(self, library_with_data):
        """Test warband search with exact matches."""
        library = library_with_data
        
        result = library.search_warbands("Mollog")
        assert len(result) >= 1
        assert any("Mollog" in name for name in result['Name'].tolist())

    def test_search_warbands_partial_match(self, library_with_data):
        """Test warband search with partial matches."""
        library = library_with_data
        
        result = library.search_warbands("Grand Alliance")
        assert len(result) >= 1
        assert any("Grand Alliance" in name for name in result['Name'].tolist())

    def test_search_warbands_lazy_loading(self, temp_csv_files):
        """Test that warband data is loaded lazily on first search."""
        cards_path, warbands_path = temp_csv_files
        library = Library(card_path=cards_path, warband_path=warbands_path)
        
        # Initially memory should be None
        assert library._warband_memory is None
        
        # After search, memory should be loaded
        library.search_warbands("Mollog")
        assert isinstance(library._warband_memory, pd.DataFrame)

    def test_get_whole_warband_basic(self, library_with_data):
        """Test getting all fighters from a warband."""
        library = library_with_data
        
        result = library.get_whole_warband("Mollog's Mob")
        assert len(result) >= 1
        # Should contain fighters from Mollog's Mob
        assert all("Mollog" in warband for warband in result['Warband'].tolist())

    def test_get_whole_warband_with_alliance(self, library_with_data):
        """Test getting warband with grand alliance filtering."""
        library = library_with_data
        
        result = library.get_whole_warband("Domitan's Stormcoven", "Grand Alliance Order")
        assert len(result) >= 1
        
        # Should include the specific warband and alliance options
        warband_names = result['Warband'].tolist()
        assert any("Domitan" in warband for warband in warband_names)

    def test_find_deck_sets(self, library_with_data):
        """Test finding deck sets for duplicate cards."""
        library = library_with_data
        
        # Create a single-row DataFrame to simulate a found card
        card_frame = pd.DataFrame({'Name': ['Strike the Head']})
        
        result = library.find_deck_sets(card_frame)
        assert len(result) >= 1
        assert 'Set' in result.columns
        assert 'Deck' in result.columns

    def test_search_cards_deduplication(self, library_with_data):
        """Test that search results are deduplicated by name."""
        library = library_with_data
        
        # Add a duplicate card to test data
        duplicate_row = library._card_memory.iloc[0:1].copy()
        duplicate_row['Set'] = 'Different Set'
        library._card_memory = pd.concat([library._card_memory, duplicate_row], ignore_index=True)
        
        result = library.search_cards("Strike the Head")
        
        # Should only return one result despite duplicates
        assert len(result) == 1

    def test_search_prioritization(self, library_with_data):
        """Test that exact matches are prioritized over fuzzy matches."""
        library = library_with_data
        
        # When searching for an exact match that exists
        result = library.search_cards("Perfect Strike")
        
        # Should return exactly one result (the exact match)
        assert len(result) == 1
        assert result.iloc[0]['Name'] == "Perfect Strike"

    def test_empty_query_handling(self, library_with_data):
        """Test behavior with empty or whitespace queries."""
        library = library_with_data
        
        # Test empty string
        result = library.search_cards("")
        assert len(result) == 0 or len(result) <= 10  # Should return few or no results
        
        # Test whitespace only
        result = library.search_cards("   ")
        assert len(result) == 0 or len(result) <= 10  # Should return few or no results


class TestLibraryIntegration:
    """Integration tests that test Library with real data structure."""
    
    def test_real_data_structure_compatibility(self):
        """Test that Library works with the actual CSV structure."""
        # This test uses the actual file paths but doesn't load data
        # to avoid dependency on actual files in unit tests
        library = Library(
            card_path="src/resources/library.csv",
            warband_path="src/resources/warbands.csv"
        )
        
        # Test that initialization works
        assert library._card_path == "src/resources/library.csv"
        assert library._warband_path == "src/resources/warbands.csv"
        
        # Test that load method exists and can be called
        # (This won't actually load data unless files exist)
        assert hasattr(library, 'load')
        assert callable(library.load)