import os
import sys
from pathlib import Path

# Repo root must be on path when running as `python3 baseline/run_agent.py`
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from openai import OpenAI
from env.environment import CodeReviewEnv
from env.models import Action


def _load_env_file() -> None:
    """Populate os.environ from repo-root .env if present (KEY=value lines)."""
    path = _REPO_ROOT / ".env"
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def _env_flag(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in ("1", "true", "yes")


def run(env_path):
    _load_env_file()
    # Baseline ignores the model output; actions are fixed below. Calling the API
    # only wastes quota unless you opt in (e.g. for future wiring to Action).
    use_openai = _env_flag("USE_OPENAI")
    client = None
    if use_openai:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "USE_OPENAI is set but OPENAI_API_KEY is missing. Set the key "
                "in your environment or in a .env file in the project root."
            )
        client = OpenAI(api_key=api_key)

    env = CodeReviewEnv(env_path)
    obs = env.reset()

    done = False
    total_reward = 0

    while not done:
        if client is not None:
            _ = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a strict code reviewer."},
                    {"role": "user", "content": str(obs)},
                ],
            )

        action = Action(action_type="comment", line=1, comment="Check this line")
        obs, reward, done, _ = env.step(action)
        total_reward += reward.score

    return total_reward

if __name__ == "__main__":
    def _data(name: str) -> str:
        return str(_REPO_ROOT / "data" / name)

    print("Easy:", run(_data("pr_easy.json")))
    print("Medium:", run(_data("pr_medium.json")))
    print("Hard:", run(_data("pr_hard.json")))
