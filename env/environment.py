import json
from env.models import Observation, Action, Reward

class CodeReviewEnv:

    def __init__(self, data_path):
        self.data_path = data_path
        self.reset()

    def reset(self):
        with open(self.data_path, 'r') as f:
            self.data = json.load(f)

        self.comments = []
        self.step_count = 0
        self.max_steps = 10

        return self._get_obs()

    def _get_obs(self):
        return Observation(
            pr_id=self.data["pr_id"],
            files=self.data["files"],
            step_count=self.step_count,
            max_steps=self.max_steps
        )

    def step(self, action: Action):
        self.step_count += 1

        reward = 0
        done = False

        for act in action.actions:
            if act.action_type == "comment":
                self.comments.append({
                    "line": act.line,
                    "comment": act.comment
                })

                if self._is_correct_comment(act):
                    reward += 0.2
                else:
                    reward -= 0.1

            elif act.action_type == "approve":
                done = True
                if len(self.comments) >= len(self.data["issues"]):
                    reward += 1.0
                else:
                    reward -= 0.5

            elif act.action_type == "request_changes":
                done = True
                if len(self.comments) > 0:
                    reward += 0.5
                else:
                    reward -= 0.2

        if self.step_count >= self.max_steps:
            done = True

        return self._get_obs(), Reward(score=reward, reason="step reward"), done, {}

    def _is_correct_comment(self, action):
        for issue in self.data["issues"]:
            if issue["line"] == action.line:
                return True
        return False

    def state(self):
        return {
            "comments": self.comments,
            "step_count": self.step_count
        }
