from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents.main_agent import annuity_recommendation_agent

app = FastAPI(title="Life Annuity Advisor API", description="AI-powered annuity recommendations")

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Life Annuity Advisor API is running! Visit /docs for API documentation."}

@app.post("/recommend")
async def recommend(request: Request):
    data = await request.json()
    response = annuity_recommendation_agent(data["input"])
    return {"response": response}
