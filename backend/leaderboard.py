import json
import os

FILE = "leaderboard.json"

def save_score(model, scores):
    data = []

    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            data = json.load(f)

    data.append({
        "model": model,
        "score": scores["total"]
    })

    data = sorted(data, key=lambda x: x["score"], reverse=True)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_leaderboard():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)
