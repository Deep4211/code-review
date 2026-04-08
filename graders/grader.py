def grade(agent_comments, expected_issues):
    correct = 0

    for issue in expected_issues:
        for c in agent_comments:
            if c["line"] == issue["line"]:
                correct += 1
                break

    precision = correct / len(agent_comments) if agent_comments else 0
    recall = correct / len(expected_issues)

    return (precision + recall) / 2
