# Embergard Card Bot - AI Agent Instructions

## Architecture Overview

This is a Discord bot for searching and displaying Warhammer Underworlds: Embergard cards using fuzzy search. The bot responds to `((search_term))` patterns in Discord messages.

### Core Components

- **`main.py`**: Entry point that loads environment and starts the Discord client
- **`src/client.py`**: Main Discord client with message parsing and response logic
- **`src/card_library.py`**: Fuzzy search engine using pandas DataFrames and fuzzywuzzy
- **`src/discord/message_factory.py`**: Creates Discord embeds for different content types
- **`src/resources/`**: CSV data files for cards and warbands

## Key Data Flow

1. Discord message → regex pattern matching `\(\(\s?(.*?)\s?\)\)`
2. Query → fuzzy search against CSV data (cards + warbands)
3. Results → Discord embed generation with thumbnails/images
4. Response → single card, warband info, or multi-result list

## Critical Patterns

### Search Logic in `card_library.py`
- Uses **fuzzywuzzy** with `partial_ratio` scorer (threshold: 80)
- Prioritizes: exact matches → substring matches → fuzzy matches
- Handles apostrophe normalization (`'` → `'`)
- Lazy-loads CSV data into pandas DataFrames

### Message Response Logic in `client.py`
Complex branching based on result counts:
- 1 card match → single embed with thumbnail
- 1 warband match → fighter list or warscroll image
- Multiple matches → paginated field list (max 25 fields)
- Alliance warbands → multiple embeds for different warscroll options

### Environment Configuration
Required `.env` variables:
- `CLIENT_TOKEN`: Discord bot token
- `IMAGES_URL`: Base URL for custom card images (optional)

## Development Workflows

### Setup and Running
```bash
make install    # Creates venv, installs deps, creates logs/ dir
make run        # Runs bot directly (no venv)
make lint       # Ruff linting
make test       # Unit tests
```

### Data Updates
- **Card data**: Update `src/resources/library.csv` from UnderworldsDB
- **Warband data**: Manually update `src/resources/warbands.csv`
- **Custom images**: Set `IMAGES_URL` env var and `CustomImage` column in CSV

### Branch Strategy
- `main`: Latest Embergard edition
- `v1plus`: First edition with community balance changes

## Code Conventions

### CSV Data Structure
- **library.csv**: Cards with Name, Type, Description, Set, Deck columns
- **warbands.csv**: Fighters/warscrolls with Warband, Name, WarscrollType columns
- WarscrollType values: `null` (fighter), `"alliance"`, `"generic"`

### Discord Embed Patterns
- Single cards: thumbnail + description with icon replacements
- Warbands: image + fighter lists in fields
- Multi-results: field-based lists (5 items per field, max 25 fields)

### Icon System
- Custom Discord emoji IDs in `src/discord/custom_icons.py`
- Text replacement via `src/discord/replacement_icon_map.py`
- Pattern: `:iconname:` → Discord emoji in descriptions

## Testing Considerations

- Test fuzzy search edge cases (apostrophes, partial matches)
- Verify embed field limits (25 max, 1024 char limit per field)
- Test alliance warband multi-embed responses
- Validate CSV parsing with pandas

## Integration Points

- **UnderworldsDB**: External card data source (manual sync required)
- **Discord API**: via discord.py library with message content intents
- **Custom image hosting**: Optional external image URLs via `IMAGES_URL`

When modifying search logic, consider the prioritization order and fuzzy matching thresholds. When adding new card types or warband features, update both the CSV structure and the corresponding embed generation logic in `message_factory.py`.