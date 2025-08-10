#!/bin/bash

# Whisper Diarization SDK Installation Script

echo "🚀 Installing Whisper Diarization SDK..."

# Check if Python 3.10+ is available
python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.10+ is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg not found. Please install FFmpeg first:"
    echo "   macOS: brew install ffmpeg"
    echo "   Ubuntu/Debian: sudo apt install ffmpeg"
    echo "   Windows: choco install ffmpeg"
    exit 1
fi

echo "✅ FFmpeg found"

# UV will handle Cython installation automatically
echo "✅ Using UV for dependency management"

# Install the SDK using UV
echo "📦 Installing SDK using UV..."
uv sync --dev

echo "🔧 Installing SDK in development mode..."
uv pip install -e .

echo "✅ Installation complete!"
echo ""
echo "🎯 Quick start:"
echo "   cd examples"
echo "   python3 basic_usage.py"
echo ""
echo "📚 For more information, see README.md"
