from env.environment import CodeReviewEnv
from env.models import Action

def run_task(data_path):
    env = CodeReviewEnv(data_path)
    obs = env.reset()

    done = False
    total_reward = 0

    while not done:
        # simple baseline action
        action = Action(actions=[{"action_type": "approve"}])
        obs, reward, done, _ = env.step(action)
        total_reward += reward.score

    return total_reward


def main():
    results = {
        "easy": run_task("data/pr_easy.json"),
        "medium": run_task("data/pr_medium.json"),
        "hard": run_task("data/pr_hard.json"),
    }

    return results


if __name__ == "__main__":
    print(main())
