#!/bin/bash

# Email Classifier Quick Start Script
# This script starts both backend and frontend services

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}     Email Classifier System Startup Script     ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Check if running from correct directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}✗ Error: Please run this script from the project root directory${NC}"
    echo -e "${YELLOW}  Current directory: $(pwd)${NC}"
    exit 1
fi

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${YELLOW}⚠ Port $1 is already in use${NC}"
        return 1
    fi
    return 0
}

# Check required ports
echo -e "\n${YELLOW}Checking ports...${NC}"
PORT_ISSUE=0

if ! check_port 8002; then
    echo -e "${RED}  Backend port 8002 is occupied${NC}"
    PORT_ISSUE=1
fi

if ! check_port 3000; then
    echo -e "${RED}  Frontend port 3000 is occupied${NC}"
    PORT_ISSUE=1
fi

if [ $PORT_ISSUE -eq 1 ]; then
    echo -e "${YELLOW}Kill existing processes? (y/n):${NC} "
    read -r KILL_PROCS
    if [ "$KILL_PROCS" = "y" ]; then
        lsof -ti:8002 | xargs kill -9 2>/dev/null
        lsof -ti:3000 | xargs kill -9 2>/dev/null
        echo -e "${GREEN}✓ Ports cleared${NC}"
    else
        echo -e "${RED}Cannot start services with occupied ports${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ All ports available${NC}"
fi

# Check MySQL
echo -e "\n${YELLOW}Checking MySQL...${NC}"
if command -v mysql &> /dev/null; then
    echo -e "${GREEN}✓ MySQL is installed${NC}"
    
    # Try to connect to MySQL
    if mysql -h 127.0.0.1 -u root -e "SELECT 1" &> /dev/null; then
        echo -e "${GREEN}✓ MySQL connection successful${NC}"
        
        # Create database if it doesn't exist
        mysql -h 127.0.0.1 -u root -e "CREATE DATABASE IF NOT EXISTS email_classifier;" 2>/dev/null
        echo -e "${GREEN}✓ Database 'email_classifier' ready${NC}"
    else
        echo -e "${YELLOW}⚠ MySQL authentication required${NC}"
        echo -e "${YELLOW}  Please ensure MySQL is running and accessible${NC}"
        echo -e "${YELLOW}  You may need to update backend/.env with correct credentials${NC}"
    fi
else
    echo -e "${YELLOW}⚠ MySQL not found. Using Docker is recommended${NC}"
fi

# Start Backend
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Starting Backend Service...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

cd backend

# Check for Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
    
    # Check for virtual environment
    if [ -d "venv" ]; then
        echo -e "${GREEN}✓ Virtual environment found${NC}"
        source venv/bin/activate
    else
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv venv
        source venv/bin/activate
        echo -e "${GREEN}✓ Virtual environment created${NC}"
    fi
    
    # Install/update dependencies
    echo -e "${YELLOW}Installing backend dependencies...${NC}"
    pip install --quiet --upgrade pip
    pip install --quiet -r requirements.txt
    echo -e "${GREEN}✓ Backend dependencies installed${NC}"
    
    # Check for .env file
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}Creating .env file...${NC}"
        cat > .env << 'EOF'
DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/email_classifier
API_PORT=8002
EOF
        echo -e "${YELLOW}⚠ Created .env with default values - update if needed${NC}"
    fi
    
    # Start backend
    echo -e "${GREEN}Starting FastAPI server on port 8002...${NC}"
    python main.py &
    BACKEND_PID=$!
    sleep 3
    
    # Check if backend started successfully
    if curl -s http://localhost:8002/api/health > /dev/null; then
        echo -e "${GREEN}✓ Backend started successfully (PID: $BACKEND_PID)${NC}"
    else
        echo -e "${RED}✗ Backend failed to start${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.11+${NC}"
    exit 1
fi

# Start Frontend
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Starting Frontend Service...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

cd ../frontend

# Check for Node.js
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    NODE_VERSION=$(node --version)
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"
    echo -e "${GREEN}✓ npm $NPM_VERSION found${NC}"
    
    # Install dependencies
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    npm install --silent
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
    
    # Start frontend
    echo -e "${GREEN}Starting React development server on port 3000...${NC}"
    BROWSER=none npm start &
    FRONTEND_PID=$!
    
    # Wait for frontend to start
    echo -e "${YELLOW}Waiting for frontend to start...${NC}"
    sleep 10
    
    echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
else
    echo -e "${RED}✗ Node.js/npm not found. Please install Node.js 18+${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Success message
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}     🚀 Email Classifier System is Running!     ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}Access the application at:${NC}"
echo -e "  ${BLUE}📧 Web Interface:${NC} http://localhost:3000"
echo -e "  ${BLUE}📡 API Documentation:${NC} http://localhost:8002/docs"
echo -e "  ${BLUE}🔌 API Endpoint:${NC} http://localhost:8002"
echo ""
echo -e "${YELLOW}Quick Test:${NC}"
echo -e "  ${BLUE}curl http://localhost:8002/api/health${NC}"
echo ""
echo -e "${RED}Press Ctrl+C to stop all services${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down services...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✓ All services stopped${NC}"
    exit 0
}

# Set up trap for Ctrl+C
trap cleanup INT

# Keep script running
wait