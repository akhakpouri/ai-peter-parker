import subprocess
import json

def run_gh(args: list[str]) -> str:
    """Run a gh command and return the output."""
    result = subprocess.run(
        ["gh"] + args, 
        capture_output=True, text=True, check=True
    )
    if result.returncode != 0:
        raise Exception(f"gh command failed: {result.stderr}")
    return result.stdout.strip()

def list_pull_requests(repo: str) -> list[dict]:
    """List open pull requests in the specified repository."""
    output = run_gh(["pr", "list", "--repo", repo, "--json", 
                     "number,title,body"])
    return json.loads(output)

def view_pull_request(repo: str, pr_number: int) -> dict:
    """View details of a specific pull request."""
    output = run_gh(["pr", "view", str(pr_number), "--repo", repo, "--json", 
                     "number,title,body"])
    return json.loads(output)

def comment_on_pull_request(repo: str, pr_number: int, comment: str) -> None:
    """Add a comment to a specific pull request."""
    run_gh(["pr", "comment", str(pr_number), "--repo", repo, "--body", comment])

def review_pull_request(repo: str, pr_number: int, comment: str) -> None:
    """Submit a review on a specific pull request."""
    run_gh(["pr", "review", str(pr_number), "--repo", repo, "--body", comment])

def merge_pull_request(repo: str, pr_number: int) -> None:
    """Merge a specific pull request."""
    run_gh(["pr", "merge", str(pr_number), "--repo", repo, "--merge"])