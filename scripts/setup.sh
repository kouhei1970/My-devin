#!/bin/bash

# My-devin Setup Script
# This script sets up the development environment

set -e

echo "========================================="
echo "My-devin Setup Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}Error: This script is designed for macOS${NC}"
    exit 1
fi

# Check for Homebrew
echo -e "${YELLOW}Checking for Homebrew...${NC}"
if ! command -v brew &> /dev/null; then
    echo -e "${YELLOW}Installing Homebrew...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo -e "${GREEN}✓ Homebrew already installed${NC}"
fi

# Install required tools
echo -e "${YELLOW}Installing required tools...${NC}"

# Python 3.11
if ! command -v python3.11 &> /dev/null; then
    echo -e "${YELLOW}Installing Python 3.11...${NC}"
    brew install python@3.11
else
    echo -e "${GREEN}✓ Python 3.11 already installed${NC}"
fi

# Node.js 20
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}Installing Node.js...${NC}"
    brew install node@20
else
    echo -e "${GREEN}✓ Node.js already installed${NC}"
fi

# Ollama
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}Installing Ollama...${NC}"
    brew install ollama
else
    echo -e "${GREEN}✓ Ollama already installed${NC}"
fi

# Git
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}Installing Git...${NC}"
    brew install git
else
    echo -e "${GREEN}✓ Git already installed${NC}"
fi

echo ""
echo -e "${GREEN}All required tools installed!${NC}"
echo ""

# Setup backend
echo -e "${YELLOW}Setting up backend...${NC}"
cd backend
if [ ! -d "venv" ]; then
    python3.11 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
deactivate
echo -e "${GREEN}✓ Backend setup complete${NC}"

# Setup frontend
echo -e "${YELLOW}Setting up frontend...${NC}"
cd ../frontend
npm install
echo -e "${GREEN}✓ Frontend setup complete${NC}"

# Setup CLI
echo -e "${YELLOW}Setting up CLI...${NC}"
cd ../cli
pip install -e .
echo -e "${GREEN}✓ CLI setup complete${NC}"

cd ..

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
fi

# Create workspace directory
if [ ! -d "workspace" ]; then
    mkdir -p workspace
    echo -e "${GREEN}✓ Workspace directory created${NC}"
fi

# Create logs directory
if [ ! -d "logs" ]; then
    mkdir -p logs
    echo -e "${GREEN}✓ Logs directory created${NC}"
fi

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Setup complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Download LLM models:"
echo -e "   ${YELLOW}ollama pull qwen2.5-coder:32b${NC}"
echo ""
echo "2. Start Ollama (in a separate terminal):"
echo -e "   ${YELLOW}ollama serve${NC}"
echo ""
echo "3. Start backend server (in a separate terminal):"
echo -e "   ${YELLOW}cd backend && source venv/bin/activate && python -m uvicorn src.api.main:app --reload${NC}"
echo ""
echo "4. Start frontend (in a separate terminal):"
echo -e "   ${YELLOW}cd frontend && npm run dev${NC}"
echo ""
echo "5. Use CLI:"
echo -e "   ${YELLOW}my-devin chat${NC}"
echo ""
echo -e "${GREEN}Happy coding!${NC}"
