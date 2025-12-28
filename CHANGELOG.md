# Changelog

All notable changes to the Destiny 2 Armor Sorter project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-28

### Added
- Initial release of Destiny 2 Armor Sorter
- Flask-based web application with drag-and-drop file upload
- CSV parsing with schema validation and error handling
- Intelligent armor filtering (Legendary Tier 5 only)
- Duplicate detection system:
  - Archetype + Tertiary Stat duplicate identification across different armor sets
  - Exact duplicate detection including Tuning Stat
- Armor set and base item derivation from armor names
- Excel export functionality with:
  - Color-coded armor types for visual organization
  - Duplicate highlighting in orange
  - Separate sheets per class (Hunter, Warlock, Titan)
  - Summary dashboard with class-level statistics
- Modern responsive UI with Material Design:
  - Class-based tabs for Hunter, Warlock, and Titan
  - Interactive data preview before download
  - Toggle switches for stat column visibility
  - Tuning stat grouping option
  - Real-time metrics display
- Automated startup script (start.sh) for easy deployment
- Complete project structure with:
  - Modular service layer (CSV parser, data processor, Excel exporter)
  - Separation of concerns with blueprints and routes
  - Static assets (CSS) and templates
  - Comprehensive test coverage

### Technical Details
- Python 3.7+ support
- Flask 3.0.0 web framework
- pandas 2.2.3 for data manipulation
- openpyxl 3.1.5 for Excel generation
- pytest 7.4.3 for testing
- Session-based file handling for downloads
- Temporary file management with automatic cleanup

### Features
- **CSV Upload**: Drag-and-drop or file browser support
- **Data Validation**: Ensures all required columns are present
- **Smart Filtering**: Automatically removes non-Legendary and non-Tier 5 armor
- **Duplicate Detection**: Identifies redundant armor pieces across sets
- **Excel Reports**: Generate styled workbooks with summary statistics
- **Class Organization**: Separate views and sheets for each Guardian class
- **Stat Analysis**: Calculate averages, highs, lows, and distributions
- **Archetype Breakdown**: View armor distribution by stat archetype
- **Visual Indicators**: Color-coding for armor types and duplicate highlighting

### Security
- File type validation (CSV only)
- Secure file handling with temporary storage
- Session-based download management
- Error handling for malformed or invalid data

## Contributing

When making contributions, please:
1. Update this CHANGELOG.md with your changes under the [Unreleased] section
2. Follow the format: Added, Changed, Deprecated, Removed, Fixed, Security
3. Include the date when releasing a new version
4. Update version numbers according to Semantic Versioning

## Version History

- **1.0.0** - Initial release with full feature set

