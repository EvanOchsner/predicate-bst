#!/bin/bash
set -e

# Colors for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Installing package in development mode...${NC}"
pip install -e ".[dev]"

echo -e "${YELLOW}Running tests...${NC}"
pytest -v --cov=predicate_bst

echo -e "${GREEN}All tests passed!${NC}"