from baseline.run_agent import run

def run_all_tasks(model_name):
    results = {
        "easy": run("data/pr_easy.json"),
        "medium": run("data/pr_medium.json"),
        "hard": run("data/pr_hard.json")
    }

    results["total"] = sum(results.values()) / 3
    return results
