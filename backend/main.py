from fastapi import FastAPI
from backend.runner import run_all_tasks
from backend.leaderboard import save_score, get_leaderboard
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def root():
    return {"message": "Code Review OpenEnv API"}

@app.post("/run")
def run_agent(model_name: str):
    scores = run_all_tasks(model_name)
    save_score(model_name, scores)
    return {"model": model_name, "scores": scores}

@app.get("/leaderboard")
def leaderboard():
    return get_leaderboard()
