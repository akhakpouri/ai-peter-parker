from dotenv import load_dotenv
load_dotenv()

import json
from pr_agent.github import list_pull_requests, view_pull_request, comment_on_pull_request, review_pull_request, merge_pull_request

import anthropic
client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"

TOOLS = [
    {
        "name": "list_prs",
        "description": "List open pull requests for a repo",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo": {"type": "string", "description": "owner/repo format"}
            },
            "required": ["repo"]
        }
    },
    {
        "name": "view_pr",
        "description": "View details, diff, and comments of a PR",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo": {"type": "string"},
                "pr_number": {"type": "integer"}
            },
            "required": ["repo", "pr_number"]
        }
    },
    {
        "name": "comment_pr",
        "description": "Post a general comment on a PR",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo": {"type": "string"},
                "pr_number": {"type": "integer"},
                "body": {"type": "string"}
            },
            "required": ["repo", "pr_number", "body"]
        }
    },
    {
        "name": "review_pr",
        "description": "Submit a formal review: COMMENT, APPROVE, or REQUEST_CHANGES",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo": {"type": "string"},
                "pr_number": {"type": "integer"},
                "body": {"type": "string"},
                "event": {
                    "type": "string",
                    "enum": ["COMMENT", "APPROVE", "REQUEST_CHANGES"]
                }
            },
            "required": ["repo", "pr_number", "body", "event"]
        }
    },
    {
        "name": "merge_pr",
        "description": "Merge a PR",
        "input_schema": {
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
    try:
        if name == "list_prs":
            return json.dumps(list_pull_requests(**inputs))
        elif name == "view_pr":
            result = view_pull_request(**inputs)
            return json.dumps(result)
        elif name == "comment_pr":
            comment_on_pull_request(**inputs)
            return "Comment added successfully."
        elif name == "review_pr":
            review_pull_request(**inputs)
            return "Review submitted successfully."
        elif name == "merge_pr":
            merge_pull_request(**inputs)
            return "Pull request merged successfully."
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        return f"Error calling tool {name}: {str(e)}"
    
def run_agent(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    while True:
        response = client.messages.create(
            model = MODEL,
            max_tokens=4096,
            tools = TOOLS,
            messages = messages
        )

        # If the stop reason is "end_turn", it means the model has finished its response and is not calling a tool
        if response.stop_reason == "end_turn":
                return next(b.text for b in response.content if hasattr(b, "text"))
        
        # If no tool calls, also return
        if response.stop_reason != "tool_use":
            return str(response.content)
        
        # Handle tool calls and collect results
        results = []
        for block in response.content:
            if block.type == "tool_use":
                result = tool_call(block.name, block.input)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })
        
        # Only append if we actually have results
        if not results:
            break

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": results})