# 🏠 Local Development Guide

This guide will help you run the AWS Crypto Analytics Platform locally for development and testing.

## 📋 Prerequisites

- ✅ Python 3.13+ installed
- ✅ Node.js 16+ installed
- ✅ Virtual environment activated (`source venv/bin/activate`)
- ✅ All Python dependencies installed (`pip install -r requirements.txt`)

## 🚀 Quick Start

### Option 1: Run Everything at Once (Recommended)

```bash
# Make sure you're in the project directory and virtual environment is activated
./run_local.sh
```

This will:
- ✅ Start the data producer (fetches real crypto data)
- ✅ Start the backend API (FastAPI)
- ✅ Install frontend dependencies (if needed)
- ✅ Start the React frontend

### Option 2: Run Components Individually

#### Step 1: Start Data Producer
```bash
python local_setup.py
```

#### Step 2: Start Backend API
```bash
cd backend
python app_local.py
```

#### Step 3: Start Frontend
```bash
cd frontend
npm install  # First time only
npm start
```

## 🌐 Access Points

Once everything is running, you can access:

- **Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📊 API Endpoints

### Real-time Data
- `GET /api/prices` - Get all cryptocurrency prices
- `GET /api/prices/{symbol}` - Get specific crypto price
- `GET /api/history/{symbol}` - Get historical data

### Analytics
- `GET /api/analytics/market` - Market overview and analytics
- `POST /api/predict` - ML price prediction (simulated)

### System
- `GET /health` - Health check
- `POST /api/cache/refresh` - Refresh cache

## 🗄️ Local Database

The application uses SQLite for local development:
- **Database file**: `local_crypto.db`
- **Tables**: `crypto_prices`, `historical_data`
- **Cache**: In-memory cache

## 🔧 Development Features

### Real-time Data
- ✅ Fetches real cryptocurrency data from CoinGecko API
- ✅ Updates every 60 seconds automatically
- ✅ Stores historical data for analysis

### Simulated AWS Services
- ✅ **DynamoDB** → SQLite database
- ✅ **Redis** → In-memory cache
- ✅ **Kinesis** → Direct API calls
- ✅ **SageMaker** → Simple ML prediction

### Frontend Features
- ✅ Real-time price updates
- ✅ Interactive charts
- ✅ Market analytics
- ✅ Price predictions
- ✅ Responsive design

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using the port
lsof -i :8000
lsof -i :3000

# Kill the process
kill -9 <PID>
```

#### 2. Frontend Dependencies
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### 3. Database Issues
```bash
# Reset local database
rm local_crypto.db
python local_setup.py
```

#### 4. Virtual Environment
```bash
# Make sure you're in the virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

### Logs

- **Data Producer**: Check terminal output for data fetching logs
- **Backend**: Check terminal output for API logs
- **Frontend**: Check browser console for frontend logs

## 🔄 Development Workflow

1. **Start local environment**: `./run_local.sh`
2. **Make code changes** in any component
3. **Test changes** in the browser/API
4. **Stop services**: `Ctrl+C`
5. **Restart**: `./run_local.sh`

## 📁 Project Structure (Local)

```
aws-crypto-analytics/
├── local_setup.py          # Local data producer
├── run_local.sh            # Local runner script
├── local_crypto.db         # SQLite database
├── backend/
│   ├── app_local.py        # Local backend API
│   └── app.py              # AWS backend API
├── frontend/
│   ├── src/                # React components
│   └── package.json        # Frontend dependencies
└── venv/                   # Python virtual environment
```

## 🎯 Next Steps

After testing locally:

1. **Configure AWS CLI**: `aws configure`
2. **Deploy to AWS**: `./deploy.sh dev us-east-1`
3. **Monitor**: Check AWS CloudWatch logs
4. **Scale**: Use AWS services for production

## 💡 Tips

- **API Testing**: Use http://localhost:8000/docs for interactive API testing
- **Data Validation**: Check `local_crypto.db` with SQLite browser
- **Performance**: Monitor memory usage during development
- **Debugging**: Use browser dev tools for frontend debugging

---

**Ready to run locally?** 🚀

```bash
./run_local.sh
``` 