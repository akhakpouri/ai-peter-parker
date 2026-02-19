# 🕷️ PR Agent (Peter Parker)

An AI-powered assistant that helps you read, comment, review, and work with GitHub pull requests effortlessly using Claude AI.

## Features

- 📋 List open pull requests for any repository
- 👀 View PR details, diffs, and comments
- 💬 Comment on pull requests
- ✅ Submit formal reviews (COMMENT, APPROVE, REQUEST_CHANGES)
- 🔀 Merge pull requests
- 🤖 Natural language interface powered by Claude Haiku 4.5

## Prerequisites

- **Python 3.11+**
- **GitHub CLI (`gh`)**: Must be installed and authenticated
  ```bash
  # Install GitHub CLI (macOS)
  brew install gh
  
  # Authenticate with GitHub
  gh auth login
  ```
- **Anthropic API Key**: Get one from [Anthropic Console](https://console.anthropic.com/)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/peter-parker.git
cd peter-parker
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install the package in editable mode
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Required: Your Anthropic API key
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

**⚠️ Important**: Never commit your `.env` file or expose your API key!

## Usage

The PR Agent uses natural language to interact with pull requests:

```bash
# List open PRs
python -m pr_agent.main "list open PRs for owner/repo"

# View a specific PR
python -m pr_agent.main "show me PR #5 from owner/repo"

# Comment on a PR
python -m pr_agent.main "comment on PR #5 in owner/repo saying 'LGTM!'"

# Review a PR
python -m pr_agent.main "approve PR #5 in owner/repo with comment 'Great work!'"

# Merge a PR
python -m pr_agent.main "merge PR #5 in owner/repo"
```

### Example Commands

```bash
# Complex review request
python -m pr_agent.main "review PR #12 from myorg/myrepo and provide feedback on code quality"

# List and analyze
python -m pr_agent.main "list all open PRs for myorg/myrepo and tell me which ones need attention"

# Detailed analysis
python -m pr_agent.main "analyze PR #8 from myorg/myrepo and suggest improvements"
```

## Project Structure

```
peter-parker/
├── src/
│   └── pr_agent/
│       ├── __init__.py
│       ├── main.py          # CLI entry point
│       ├── agent.py         # Claude AI agent with tool calling
│       └── github.py        # GitHub CLI integration
├── tests/                   # Test files (coming soon)
├── .env                     # Environment variables (create this)
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Project configuration
├── requirements.txt        # Python dependencies
├── LICENSE
└── README.md
```

## How It Works

1. **Natural Language Input**: You provide instructions in plain English
2. **Claude AI Processing**: The agent uses Claude Haiku 4.5 to understand your intent
3. **Tool Selection**: Claude decides which GitHub operations to perform
4. **GitHub CLI Execution**: Commands are executed via the `gh` CLI tool
5. **Response**: Results are formatted and returned to you

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key for Claude AI |

## Dependencies

- **anthropic** (0.82.0): Anthropic's Python SDK for Claude AI
- **python-dotenv** (1.2.1): Environment variable management
- **pydantic** (2.12.5): Data validation and settings management

## Development

### Install in Development Mode

```bash
pip install -e .
```

### Running Tests

```bash
pytest tests/
```

### Code Style

Follow PEP 8 guidelines. Consider using:
```bash
pip install black isort
black src/
isort src/
```

## Troubleshooting

### GitHub CLI Not Found
```bash
# Install GitHub CLI
brew install gh  # macOS
# or visit: https://cli.github.com/

# Authenticate
gh auth login
```

### API Key Issues
- Ensure your `.env` file exists in the project root
- Verify the `ANTHROPIC_API_KEY` is set correctly
- Check that your API key is active in the Anthropic Console

### Permission Errors
- Ensure you have the necessary GitHub permissions for the repository
- Check that `gh auth status` shows you're authenticated

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Powered by [Anthropic's Claude AI](https://www.anthropic.com/)
- Built on [GitHub CLI](https://cli.github.com/)
