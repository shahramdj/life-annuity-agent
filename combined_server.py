#!/usr/bin/env python3
import os
import sys
sys.path.append('/workspace/backend')

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from agents.main_agent import annuity_recommendation_agent

app = FastAPI(title="Life Annuity Advisor", description="AI-powered annuity recommendations")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
@app.get("/api/")
async def api_root():
    return {"message": "Life Annuity Advisor API is running!"}

@app.post("/api/recommend")
async def recommend(request: Request):
    data = await request.json()
    response = annuity_recommendation_agent(data["input"])
    return {"response": response}

# Serve React build files (we'll create these)
@app.get("/")
async def serve_frontend():
    return FileResponse('/workspace/frontend/public/index.html')

# Static files
app.mount("/static", StaticFiles(directory="/workspace/frontend/src"), name="static")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting combined server on http://34.210.205.116:80")
    print("📱 Frontend: http://34.210.205.116:80")
    print("🔧 API: http://34.210.205.116:80/api/")
    uvicorn.run(app, host="0.0.0.0", port=80)