#!/bin/bash

# D2ArmorSorter Startup Script

echo "================================================"
echo "  Destiny 2 Armor Sorter - Starting Server"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠ Virtual environment not found. Creating one..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "→ Activating virtual environment..."
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "→ Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the application
echo ""
echo "→ Starting Flask application..."
echo "→ Open your browser to: http://127.0.0.1:8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py

