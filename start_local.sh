#!/bin/bash

# Clean Local Development Startup Script
# This script properly starts all components without conflicts

set -e

echo "🚀 Starting AWS Crypto Analytics Platform (Clean Start)..."
echo "========================================================"

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Virtual environment not activated!"
    echo "Please run: source venv/bin/activate"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo "🛑 Shutting down all services..."
    pkill -f "python.*local_setup.py" 2>/dev/null || true
    pkill -f "python.*app_local.py" 2>/dev/null || true
    pkill -f "npm.*start" 2>/dev/null || true
    echo "✅ Cleanup complete"
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Step 1: Kill any existing processes
echo "🧹 Step 1: Cleaning up existing processes..."
pkill -f "python.*local_setup.py" 2>/dev/null || true
pkill -f "python.*app_local.py" 2>/dev/null || true
pkill -f "npm.*start" 2>/dev/null || true
sleep 2

# Step 2: Start data producer
echo "📊 Step 2: Starting data producer..."
python local_setup.py &
DATA_PRODUCER_PID=$!
echo "✅ Data producer started (PID: $DATA_PRODUCER_PID)"

# Wait for data producer to initialize
sleep 5

# Step 3: Start backend API
echo "🔧 Step 3: Starting backend API..."
cd backend
python app_local.py &
BACKEND_PID=$!
cd ..
echo "✅ Backend API started (PID: $BACKEND_PID)"

# Wait for backend to start
sleep 5

# Step 4: Test backend
echo "🧪 Step 4: Testing backend..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is responding"
else
    echo "❌ Backend not responding, retrying..."
    sleep 5
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ Backend is now responding"
    else
        echo "❌ Backend still not responding"
        exit 1
    fi
fi

# Step 5: Start frontend
echo "🎨 Step 5: Starting frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..
echo "✅ Frontend started (PID: $FRONTEND_PID)"

# Wait for frontend to start
sleep 10

echo ""
echo "🎉 AWS Crypto Analytics Platform is Running!"
echo "============================================"
echo ""
echo "📊 Services Status:"
echo "  ✅ Data Producer: Running (PID: $DATA_PRODUCER_PID)"
echo "  ✅ Backend API: Running (PID: $BACKEND_PID)"
echo "  ✅ Frontend: Running (PID: $FRONTEND_PID)"
echo ""
echo "🌐 Access Points:"
echo "  • Dashboard: http://localhost:3000"
echo "  • Backend API: http://localhost:8000"
echo "  • API Docs: http://localhost:8000/docs"
echo "  • Health Check: http://localhost:8000/health"
echo ""
echo "📊 Test API Endpoints:"
echo "  • Latest Prices: http://localhost:8000/api/prices"
echo "  • Market Analytics: http://localhost:8000/api/analytics/market"
echo "  • Test Endpoint: http://localhost:8000/test"
echo ""
echo "📝 Local Database: local_crypto.db"
echo "💾 Cache: In-memory"
echo ""
echo "🛑 Press Ctrl+C to stop all services"
echo ""

# Keep script running and monitor processes
while true; do
    # Check if processes are still running
    if ! kill -0 $DATA_PRODUCER_PID 2>/dev/null; then
        echo "❌ Data producer stopped unexpectedly"
        break
    fi
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "❌ Backend stopped unexpectedly"
        break
    fi
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "❌ Frontend stopped unexpectedly"
        break
    fi
    sleep 10
done

cleanup 