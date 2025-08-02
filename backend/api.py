from fastapi import FastAPI, Request
from agents.main_agent import annuity_recommendation_agent

app = FastAPI()

@app.post("/recommend")
async def recommend(request: Request):
    data = await request.json()
    return {"response": annuity_recommendation_agent(data["input"])}
