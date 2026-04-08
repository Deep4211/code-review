import os
import json
from openai import OpenAI
from env.environment import CodeReviewEnv
from env.models import Action
from graders.grader import grade

API_BASE_URL = os.getenv("API_BASE_URL") or "https://api.openai.com/v1"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN or os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
You are a strict code reviewer.

Return ONLY JSON:
{
  "actions": [
    {"action_type": "comment", "line": int, "comment": "text"},
    {"action_type": "request_changes"}
  ]
}
"""

def get_action(obs):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": str(obs)}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        return Action(**json.loads(content))
    except:
        return Action(actions=[{"action_type": "approve"}])

def run_task(name, path):
    print(f"[START] task={name}")

    env = CodeReviewEnv(path)
    obs = env.reset()

    done = False
    total_reward = 0
    step_count = 0

    while not done:
        action = get_action(obs)

        obs, reward, done, _ = env.step(action)

        total_reward += reward.score
        step_count += 1

        print(f"[STEP] task={name} step={step_count} reward={reward.score}")

    print(f"[END] task={name} total_reward={total_reward} score={final_score}")

    return total_reward


def main():
    results = {
        "easy": run_task("easy", "data/pr_easy.json"),
        "medium": run_task("medium", "data/pr_medium.json"),
        "hard": run_task("hard", "data/pr_hard.json"),
    }

    print("FINAL RESULTS:", results)
    return results


if __name__ == "__main__":
    main()
