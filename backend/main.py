import os
from fastapi import FastAPI
from env.environment import CodeReviewEnv
from env.models import Action

app = FastAPI()

env_instance = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    global env_instance
    env_instance = CodeReviewEnv("data/pr_easy.json")
    obs = env_instance.reset()
    return obs.dict()

@app.post("/step")
def step(action: dict):
    global env_instance

    action_obj = Action(**action)
    obs, reward, done, info = env_instance.step(action_obj)

    return {
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    global env_instance
    if env_instance is None:
        return {"error": "env not initialized"}
    return env_instance.state()

