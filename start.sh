#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Email Classifier Startup Script${NC}"
echo "================================"

# Check if MySQL is installed and running
echo -e "\n${YELLOW}Checking MySQL...${NC}"
if command -v mysql &> /dev/null; then
    echo -e "${GREEN}✓ MySQL is installed${NC}"
    
    # Try to create database if it doesn't exist
    mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS email_classifier;" 2>/dev/null && \
    echo -e "${GREEN}✓ Database ready${NC}" || \
    echo -e "${YELLOW}! Please ensure MySQL is running and database 'email_classifier' exists${NC}"
else
    echo -e "${RED}✗ MySQL not found. Please install MySQL or use Docker setup${NC}"
fi

# Start backend
echo -e "\n${YELLOW}Starting Backend...${NC}"
cd backend

# Check for Python
if command -v python3 &> /dev/null; then
    echo "Installing backend dependencies..."
    
    # Try with virtual environment first
    if [ ! -d "venv" ]; then
        python3 -m venv venv 2>/dev/null || python3.12 -m venv venv 2>/dev/null || python3.11 -m venv venv
    fi
    
    if [ -d "venv" ]; then
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        echo -e "${GREEN}✓ Backend dependencies installed${NC}"
        
        # Start backend in background
        echo "Starting FastAPI server..."
        python main.py &
        BACKEND_PID=$!
        echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
    else
        echo -e "${YELLOW}! Using system Python (may need sudo)${NC}"
        pip3 install --user -r requirements.txt 2>/dev/null || pip3 install -r requirements.txt --break-system-packages
        python3 main.py &
        BACKEND_PID=$!
    fi
else
    echo -e "${RED}✗ Python 3 not found${NC}"
fi

# Start frontend
echo -e "\n${YELLOW}Starting Frontend...${NC}"
cd ../frontend

if command -v npm &> /dev/null; then
    echo "Installing frontend dependencies..."
    npm install
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
    
    echo "Starting React development server..."
    npm start &
    FRONTEND_PID=$!
    echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
else
    echo -e "${RED}✗ Node.js/npm not found${NC}"
fi

echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}Application is starting up!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Access the application at:"
echo -e "  ${YELLOW}Frontend:${NC} http://localhost:3000"
echo -e "  ${YELLOW}API Docs:${NC} http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo 'Shutting down...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait