#!/bin/bash
# Run the bot hunting analysis for IMC Prosperity Round 1.
# Dependencies are pinned in the repository root requirements.txt.
cd "$(dirname "$0")"
echo "Installing dependencies..."
pip install -r ../requirements.txt -q
echo "Running bot hunter analysis..."
python analyze_bot.py
