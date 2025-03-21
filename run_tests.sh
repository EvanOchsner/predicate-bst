#!/bin/bash
set -e

echo "Installing package in development mode..."
pip install -e .

echo "Running tests..."
pytest -v
