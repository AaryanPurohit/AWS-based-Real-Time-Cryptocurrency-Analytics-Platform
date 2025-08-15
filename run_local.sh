#!/bin/bash

# Local Development Runner for AWS Crypto Analytics Platform
# This script runs all components locally for development and testing

set -e

echo "🚀 Starting Local Crypto Analytics Platform..."
echo "=============================================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Virtual environment not activated!"
    echo "Please run: source venv/bin/activate"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo "🛑 Shutting down local services..."
    if [[ -n "$DATA_PRODUCER_PID" ]]; then
        kill $DATA_PRODUCER_PID 2>/dev/null || true
    fi
    if [[ -n "$BACKEND_PID" ]]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [[ -n "$FRONTEND_PID" ]]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo "✅ Cleanup complete"
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Step 1: Initialize local data store and start data producer
echo "📊 Step 1: Initializing local data store..."
python local_setup.py &
DATA_PRODUCER_PID=$!

# Wait a moment for data producer to start
sleep 3

# Step 2: Start backend API
echo "🔧 Step 2: Starting backend API..."
cd backend
python app_local.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 5

# Step 3: Check if frontend dependencies are installed
echo "🎨 Step 3: Checking frontend dependencies..."
cd frontend
if [[ ! -d "node_modules" ]]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Step 4: Start frontend
echo "🌐 Step 4: Starting frontend..."
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Local Crypto Analytics Platform is running!"
echo "=============================================="
echo ""
echo "📊 Services:"
echo "  • Data Producer: Running (fetches real crypto data every 60s)"
echo "  • Backend API: http://localhost:8000"
echo "  • Frontend: http://localhost:3000"
echo "  • API Docs: http://localhost:8000/docs"
echo ""
echo "🔗 Quick Links:"
echo "  • Dashboard: http://localhost:3000"
echo "  • API Health: http://localhost:8000/health"
echo "  • Latest Prices: http://localhost:8000/api/prices"
echo "  • Market Analytics: http://localhost:8000/api/analytics/market"
echo ""
echo "📝 Local Database: local_crypto.db"
echo "💾 Cache: In-memory"
echo ""
echo "🛑 Press Ctrl+C to stop all services"
echo ""

# Wait for all processes
wait 