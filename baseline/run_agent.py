import os
import json
from openai import OpenAI
from env.environment import CodeReviewEnv
from env.models import Action

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an expert senior software engineer performing a code review.

Think carefully before responding.

Your job:
1. Analyze the code deeply
2. Identify ALL issues (bugs, security, bad practices)
3. Add comments for each issue
4. Decide final action:
   - approve → if code is perfect
   - request_changes → if issues found

Output STRICT JSON:

{
  "actions": [
    {"action_type": "comment", "line": int, "comment": "text"},
    ...
    {"action_type": "approve"} OR {"action_type": "request_changes"}
  ]
}

Rules:
- Multiple comments allowed
- ALWAYS include final decision
- No text outside JSON
"""

def get_action_from_llm(obs):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Code Review Task:

{obs}

Respond ONLY in JSON.
"""
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    try:
        action_dict = json.loads(content)
        return Action(**action_dict)
    except Exception:
        print("Invalid JSON from model:\n", content)
        return Action(actions=[{"action_type": "approve"}])

def run(env_path):
    env = CodeReviewEnv(env_path)
    obs = env.reset()

    done = False
    total_reward = 0

    while not done:
        action = get_action_from_llm(obs)
        obs, reward, done, _ = env.step(action)
        total_reward += reward.score

    return total_reward

if __name__ == "__main__":
    print("\nRunning Smart Agent...\n")

    print("Easy:", run("data/pr_easy.json"))
    print("Medium:", run("data/pr_medium.json"))
    print("Hard:", run("data/pr_hard.json"))
