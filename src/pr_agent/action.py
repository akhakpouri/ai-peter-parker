import os
import json
from pr_agent.agent import run_agent

def main():
    repo = os.environ.get("GITHUB_REPO")
    if not repo:
        raise RuntimeError("GITHUB_REPO environment variable is not set")

    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        raise RuntimeError("GITHUB_EVENT_PATH environment variable is not set")
    
    with open(event_path) as f:
        event = json.load(f)

    pr_number = event.get("pull_request", {}).get("number")
    prmpt = (
        f"Review pull request #{pr_number} in repository {repo}. "
        "Read the PR description and comments, then provide a summary and your recommendation (approve, request changes, or comment)."
    )
    result = run_agent(prmpt)
    print(result)

if __name__ == "__main__":
    main()