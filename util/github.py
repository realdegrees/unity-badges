import requests
import os
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
EXCLUDE_BRANCHES = {"main", "develop"}  # Branches to exclude
FILE_EXTENSION = ".unity"

# Headers for authenticated requests (if token is available)
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}


def fetch_branches(base_url):
    """
    Fetch all branches in the repository, excluding specific branches.
    """
    url = f"{base_url}/branches"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    branches = response.json()

    # Filter out excluded branches
    # Add other branches to exclude as needed
    EXCLUDE_BRANCHES = {"main", "develop"}
    return [branch["name"] for branch in branches if branch["name"] not in EXCLUDE_BRANCHES]


def fetch_branch_changes_against_develop(owner: str, repo: str, head_branch: str, base_branch: str = "develop", file_extension: str = ".unity"):
    """
    Compare changes in a specific branch to the 'develop' branch.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/compare/{base_branch}...{head_branch}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    diff_data = response.json()

    # Filter files with the specified extension
    changes = []
    for file in diff_data.get("files", []):
        if file["filename"].endswith(file_extension):
            
            changes.append({
                "branch": head_branch,
                "filename": os.path.basename(file["filename"]),
            })
    return changes


def find_changes(owner: str, repo: str, file_extension: str, base_branch: str = "develop"):
    """
    Find changes to files of a specific type in all branches compared to 'develop'.
    """
    base_url = f"https://api.github.com/repos/{owner}/{repo}"
    branches = fetch_branches(base_url)  # Reuse the `fetch_branches` function

    changes = []
    for branch in branches:
        print(f"Comparing branch {branch} against {base_branch}...")
        branch_changes = fetch_branch_changes_against_develop(
            owner, repo, branch, base_branch, file_extension)
        changes.extend(branch_changes)

    return changes
