#!/bin/bash

# Movie & TV Show Recommendation System - Quick Start Script

echo "🎬 Starting Movie & TV Show Recommendation System..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.deps_installed" ]; then
    echo "📥 Installing dependencies..."
    pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
    touch venv/.deps_installed
fi

# Start Flask application
echo "🚀 Starting Flask server..."
echo ""
echo "✅ Application is running!"
echo "🌐 Open your browser: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py

