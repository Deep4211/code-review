from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.runner import run_all_tasks
from backend.leaderboard import save_score, get_leaderboard

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run_agent(model_name: str):
    scores = run_all_tasks(model_name)
    save_score(model_name, scores)
    return {"model": model_name, "scores": scores}

@app.get("/leaderboard")
def leaderboard():
    return get_leaderboard()

# 👇 IMPORTANT: mount frontend at /ui instead of /
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="frontend")