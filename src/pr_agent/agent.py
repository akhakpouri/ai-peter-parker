import anthropic
import json
from pr_agent.github import list_pull_requests, view_pull_request, comment_on_pull_request, review_pull_request, merge_pull_request

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

TOOLS = [
    {
        "name": "list_prs",
        "description": "List open pull requests in the specified repository.",
        "parameters": {
            "type": "object",
            "properties": {
                "repo": {"type": "string", "description": "owner/repo"}
            },
            "required": ["repo"]
        }
    },
    {
        "name": "view_prs",
        "description": "View details of a specific pull request, and comments on the pull request.",
        "parameters": {
            "type": "object",
            "properties": {
                "repo": {"type": "string"},
                "pr_number": {"type": "integer"}
            },
            "required": ["repo", "pr_number"]
        }
    },
    {
        "name": "comment_on_prs",
        "description": "Add a comment to a specific pull request.",
        "parameters": {
            "type": "object",
            "properties": {
                "repo": {"type": "string"},
                "pr_number": {"type": "integer"},
                "comment": {"type": "string"}
            },
            "required": ["repo", "pr_number", "comment"]
        }
    },
    {
        "name": "review_prs",
        "description": "Submit a review on a specific pull request.",
        "parameters": {
            "type": "object",
            "properties": {
                "repo": {"type": "string"},
                "pr_number": {"type": "integer"},
                "comment": {"type": "string"},
                "event": {"type": "string", "enum": ["APPROVE", "REQUEST_CHANGES", "COMMENT"]}
            },
            "required": ["repo", "pr_number", "comment", "event"]
        }
    },
    {
        "name": "merge_prs",
        "description": "Merge a specific pull request.",
        "parameters": {
            "type": "object",
            "properties": {
                "repo": {"type": "string"},
                "pr_number": {"type": "integer"}
            },
            "required": ["repo", "pr_number"]
        }
    }
]

def tool_call(name: str, inputs: dict) -> str:
    if name == "list_prs":
        return json.dumps(list_pull_requests(**inputs))
    elif name == "view_prs":
        result = view_pull_request(**inputs)
        return json.dumps(result)
    elif name == "comment_on_prs":
        comment_on_pull_request(**inputs)
        return "Comment added successfully."
    elif name == "review_prs":
        review_pull_request(**inputs)
        return "Review submitted successfully."
    elif name == "merge_prs":
        merge_pull_request(**inputs)
        return "Pull request merged successfully."
    else:
        raise ValueError(f"Unknown tool: {name}")
    
def run_agent(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model = MODEL,
        tools = TOOLS,
        tool_choice = "auto",
        messages = messages
    )

    # If the stop reason is "end_turn", it means the model has finished its response and is not calling a tool
    if response.stop_reason == "end_turn":
            return next(b.text for b in response.content if hasattr(b, "text"))
    
    # Handle tool calls and collect results
    results = []
    for block in response.content:
        if hasattr(block, "tool_calls"):
            result = tool_call(block.name, block.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result
            })

    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": results})