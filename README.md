# Life Annuity Agent

This repo implements a life annuity recommendation agent using FastAPI + React.

## 🚀 Local Setup

### Prerequisites
- Python 3.10+ 
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

## 🏃‍♂️ Running the Application

### Start Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

### Start Frontend (Terminal 2)
```bash
cd frontend
npm start
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🧪 Testing

Try these example inputs:
- "I'm 67 years old, recently retired, and looking for guaranteed income. I prefer low-risk investments."
- "I'm 45 years old, planning for retirement in 20 years, and willing to take moderate risk for growth."
- "I need immediate income and can't afford to lose any principal."

## 🏗️ Project Structure

```
├── backend/
│   ├── agents/
│   │   ├── main_agent.py      # Main orchestration agent
│   │   ├── profiler.py        # Customer profiling
│   │   ├── matcher.py         # Product matching
│   │   ├── calculator.py      # Income calculations
│   │   ├── explainer.py       # Product explanations
│   │   └── compliance.py      # Compliance checking
│   ├── api.py                 # FastAPI application
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   └── index.js          # React entry point
│   ├── public/
│   │   └── index.html        # HTML template
│   └── package.json          # Node.js dependencies
└── README.md
```

## 💡 Features

- **AI-Powered Recommendations**: Intelligent annuity product matching
- **Customer Profiling**: Analyzes retirement goals and risk tolerance
- **Product Database**: Comprehensive annuity product catalog
- **Income Calculations**: Real-time income projections
- **Compliance Checking**: Ensures suitable recommendations
- **Modern UI**: Beautiful, responsive React interface
