import sys
from dotenv import load_dotenv
from pr_agent.agent import run_agent

load_dotenv()

def main():
    prompt = " ".join(sys.argv[1:]) or "list open PRs for owner/repo"
    print(run_agent(prompt))
    
if __name__ == "__main__":
    main()