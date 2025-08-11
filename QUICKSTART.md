# 🚀 Quick Start Guide

## Option 1: Automated Setup

### On macOS/Linux:
```bash
./setup.sh
```

### On Windows:
```cmd
setup.bat
```

## Option 2: Manual Setup

### 1. Install Prerequisites
- **Python 3.10+**: https://python.org
- **Node.js 16+**: https://nodejs.org

### 2. Setup Backend
```bash
cd backend
python -m venv venv

# Activate virtual environment:
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
```

### 3. Setup Frontend
```bash
cd frontend
npm install
```

### 4. Run the Application

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn api:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm start
```

### 5. Open Your Browser
Go to: **http://localhost:3000**

## 🧪 Test Scenarios

Try these inputs to test the AI recommendations:

### Low Risk (Retired)
```
I'm 67 years old, recently retired, and looking for guaranteed income. 
I prefer low-risk investments and want to ensure steady monthly payments for life.
```

### Moderate Risk (Pre-retirement)
```
I'm 45 years old, planning for retirement in 20 years. 
I'm willing to take moderate risk for potential growth but want some guarantees.
```

### Conservative (Risk Averse)
```
I need immediate income and can't afford to lose any principal. 
Safety is my top priority over growth.
```

## 📊 Expected Results

The application will provide:
- ✅ Personalized product recommendations
- ✅ Income calculations and projections  
- ✅ Matched insurance providers
- ✅ Compliance and suitability checks
- ✅ Detailed product explanations

## 🔧 API Endpoints

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Recommendation Endpoint**: POST http://localhost:8000/recommend

## 🐛 Troubleshooting

### Backend Issues
- Ensure Python 3.10+ is installed
- Check virtual environment is activated
- Verify all dependencies installed: `pip list`

### Frontend Issues  
- Ensure Node.js 16+ is installed
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

### CORS Issues
- The backend includes CORS middleware
- Ensure backend is running on port 8000
- Check browser console for error messages