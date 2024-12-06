import requests
import os
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
FILE_EXTENSION = ".unity"

# Headers for authenticated requests (if token is available)
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}


def fetch_branches(base_url,) -> List[str]:
    url = f"{base_url}/branches"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    if response.status_code != 200:
        return []
    branches = response.json()

    return [branch["name"] for branch in branches]


def fetch_branch_changes_against(base_url: str, head_branch: str, base_branch: str = "develop", file_extension: str = ".unity") -> List[str]:
    url = f"{base_url}/compare/{base_branch}...{head_branch}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return []
    diff_data = response.json()

    # Filter files with the specified extension
    scenes_modified = []
    for file in diff_data.get("files", []):
        if file["filename"].endswith(file_extension):

            scenes_modified.append(os.path.splitext(
                os.path.basename(file["filename"]))[0])
    return scenes_modified


def find_changes(owner: str, repo: str, file_extension: str, base_branch: str) -> Dict[str, Dict[str, any]]:
    base_url = f"https://api.github.com/repos/{owner}/{repo}"
    branches = fetch_branches(base_url)
    changes = {}
    
    if base_branch not in branches:
        if "develop" in branches:
            changes["Warning"] = {
                "scenes_modified": ["Base branch not found, using 'develop' as default"],
                "conflicts": [base_branch],
            }
            base_branch = "develop"
        elif "main" in branches:
            changes["Warning"] = {
                "scenes_modified": ["Base branch not found, using 'main' as default"],
                "conflicts": [base_branch],
            }
            base_branch = "main"
        else:
            changes["Error"] = {
                "scenes_modified": ["Base branch not found"],
                "conflicts": [base_branch],
            }
            return changes

    
    for branch in branches:
        if (branch == base_branch):
            continue

        print(f"Comparing branch {branch} against {base_branch}...")
        branch_changes = fetch_branch_changes_against(
            base_url, branch, base_branch, file_extension)

        if (branch_changes):
            changes[branch] = {}
            changes[branch]["scenes_modified"] = branch_changes

    return changes
