# Destiny 2 Armor Sorter

A local Flask web application that helps Destiny 2 players organize and analyze their armor inventory from CSV exports. The app provides intelligent filtering, duplicate detection across armor sets, and generates color-coded Excel workbooks with comprehensive summary statistics.

## Features

### Core Functionality
- **CSV Upload**: Drag-and-drop or file browser support for armor data CSV files
- **Intelligent Filtering**: Automatically filters for Legendary Tier 5 armor pieces
- **Duplicate Detection**: Identifies duplicate armor across different sets based on:
  - Archetype + Tertiary Stat combinations
  - Exact duplicates including Tuning Stat
- **Excel Export**: Generates styled workbooks with:
  - Color-coded armor types for easy identification
  - Highlighted duplicates
  - Separate sheets per class (Hunter, Warlock, Titan)
  - Summary dashboard with key metrics

### User Interface
- **Class-Based Tabs**: View armor organized by Hunter, Warlock, and Titan
- **Interactive Preview**: Browse processed armor data before downloading
- **Toggle Views**: 
  - Show/hide stat columns for cleaner viewing
  - Group armor by Tuning Stat
- **Real-time Metrics**: See armor counts and statistics per class
- **Modern Design**: Clean, responsive interface with Material Design icons

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`:
  - Flask 3.0.0
  - pandas 2.2.3
  - openpyxl 3.1.5
  - Werkzeug 3.0.1
  - Jinja2 3.1.2

## Installation

### Option 1: Using the Startup Script (Recommended)

```bash
# Make the script executable
chmod +x start.sh

# Run the startup script
./start.sh
```

The script will automatically:
- Create a virtual environment if it doesn't exist
- Install all required dependencies
- Start the Flask application on `http://127.0.0.1:8080`

### Option 2: Manual Setup

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Usage

1. **Start the Application**
   - Run `./start.sh` or `python app.py`
   - Open your browser to `http://127.0.0.1:8080`

2. **Upload Your Armor Data**
   - Export your Destiny 2 armor inventory to CSV format
   - Drag and drop the CSV file onto the upload area, or click to browse
   - Click "Process Armor Data"

3. **Review the Results**
   - Browse armor by class using the tabs (Hunter, Warlock, Titan)
   - Toggle stat columns visibility as needed
   - Group by Tuning Stat for organized viewing
   - Review duplicate highlights to identify redundant armor

4. **Download Excel Report**
   - Click the "Download Excel File" button
   - Open the generated workbook to see:
     - Summary sheet with class-level statistics
     - Individual sheets per class with color-coded armor types
     - Highlighted duplicates for easy cleanup decisions

## CSV Format Requirements

Your CSV file must include the following columns:

| Column | Description |
|--------|-------------|
| `Name` | Full armor piece name (e.g., "Iron Fellowship Helm") |
| `Rarity` | Armor rarity (Legendary, Exotic, etc.) |
| `Tier` | Armor tier (1-5) |
| `Type` | Armor type (Helmet, Gauntlets, Chest Armor, Leg Armor, Class Item) |
| `Equippable` | Class restriction (Hunter, Warlock, Titan) |
| `Archetype` | Stat archetype (Resilient, Disciplined, etc.) |
| `Tertiary Stat` | Third priority stat |
| `Tuning Stat` | Masterwork/tuning stat focus |
| `Class`, `Weapons`, `Health`, `Grenade`, `Super`, `Melee`, `Total` | Stat values |

## Project Structure

```
destiny-armor-grid/
├── app.py                      # Application entry point
├── start.sh                    # Startup script
├── requirements.txt            # Python dependencies
├── app/
│   ├── __init__.py            # Flask app factory
│   ├── routes.py              # API endpoints
│   ├── services/
│   │   ├── csv_parser.py      # CSV validation and parsing
│   │   ├── data_processor.py  # Armor filtering and duplicate detection
│   │   └── excel_exporter.py  # Excel generation with styling
│   ├── static/
│   │   └── css/
│   │       └── style.css      # Application styles
│   └── templates/
│       └── index.html         # Main UI template
└── tests/                      # Unit tests
    ├── test_parser.py
    ├── test_filters.py
    ├── test_duplicates.py
    └── ...
```

## Testing

Run the test suite using pytest:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest

# Run specific test file
pytest tests/test_parser.py

# Run with verbose output
pytest -v
```

## Features in Detail

### Duplicate Detection

The application identifies two types of duplicates:

1. **Archetype + Tertiary Stat Duplicates**: Armor pieces from different sets with matching:
   - Class (Hunter/Warlock/Titan)
   - Armor Type (Helmet, Gauntlets, etc.)
   - Base Item name
   - Archetype
   - Tertiary Stat

2. **Exact Duplicates**: Same as above but also including matching Tuning Stat

### Excel Export Features

- **Color-Coded Armor Types**: Each armor type has a distinct color for quick identification
- **Duplicate Highlighting**: Duplicates are highlighted in orange for easy spotting
- **Summary Dashboard**: First sheet contains class-level statistics:
  - Total armor pieces per class
  - Average/highest/lowest total stats
  - Archetype distribution breakdown
  - Duplicate count
- **Organized Sheets**: Separate sheets for Hunter, Warlock, and Titan armor

## Troubleshooting

### Port Already in Use
If port 8080 is already in use, edit `app.py` and change the port number:
```python
app.run(debug=True, host='127.0.0.1', port=8081)  # Change to any available port
```

### CSV Upload Errors
- Ensure your CSV contains all required columns
- Check that column names match exactly (case-sensitive)
- Verify the CSV is not corrupted or improperly formatted

### Dependencies Not Installing
```bash
# Upgrade pip first
pip install --upgrade pip

# Then try installing requirements again
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please ensure:
- All tests pass before submitting PRs
- New features include corresponding tests
- Code follows existing style conventions

## License

This project is provided as-is for personal use by Destiny 2 players.

## Acknowledgments

Built for the Destiny 2 community to help manage and optimize armor collections.
