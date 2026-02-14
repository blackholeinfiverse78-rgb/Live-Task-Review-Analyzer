import requests
import re
import logging
import os
from typing import Dict, Any, Optional
from fastapi import HTTPException

logger = logging.getLogger("task_review_system.repo_analyzer")

class RepoAnalyzer:
    """
    Deterministic GitHub repository analyzer using REST API.
    Extracts metrics without AI or external dependencies beyond requests.
    """

    BASE_URL = "https://api.github.com"

    @staticmethod
    def _parse_url(url: str) -> tuple[str, str]:
        """Extracts owner and repo from GitHub URL."""
        pattern = r"github\.com/([\w.-]+)/([\w.-]+)"
        match = re.search(pattern, url)
        if not match:
            raise ValueError("Invalid GitHub URL format")
        owner, repo = match.groups()
        # Clean up .git suffix if present
        if repo.endswith(".git"):
            repo = repo[:-4]
        return owner, repo

    @staticmethod
    def _get_commit_count(owner: str, repo: str, headers: Dict) -> int:
        """Heuristic to get total commit count using Link header."""
        url = f"{RepoAnalyzer.BASE_URL}/repos/{owner}/{repo}/commits?per_page=1"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                return 0
            
            if "Link" in response.headers:
                # Format: <...page=123>; rel="last"
                links = response.headers["Link"]
                match = re.search(r'page=(\d+)>; rel="last"', links)
                if match:
                    return int(match.group(1))
            
            # If no link header, there's likely only 1 page
            return len(response.json())
        except Exception as e:
            logger.warning(f"Could not fetch commit count: {e}")
            return 0

    @staticmethod
    def analyze_repo(url: str) -> Dict[str, Any]:
        """
        Main analysis entry point.
        Returns structured metrics for the repository.
        """
        try:
            owner, repo = RepoAnalyzer._parse_url(url)
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Task-Review-Agent"
            }
            
            # Use GITHUB_TOKEN if available to avoid rate limits
            token = os.getenv("GITHUB_TOKEN")
            if token and token != "your_github_token_here":
                headers["Authorization"] = f"token {token}"

            # 1. Fetch Basic Metadata
            repo_res = requests.get(f"{RepoAnalyzer.BASE_URL}/repos/{owner}/{repo}", headers=headers, timeout=10)
            
            if repo_res.status_code == 404:
                raise HTTPException(status_code=404, detail="Repository not found or is private.")
            elif repo_res.status_code == 403:
                raise HTTPException(status_code=429, detail="GitHub API rate limit exceeded. Please try again later.")
            
            repo_res.raise_for_status()
            repo_data = repo_res.json()

            default_branch = repo_data.get("default_branch", "main")
            
            # 2. Fetch Languages
            lang_res = requests.get(f"{RepoAnalyzer.BASE_URL}/repos/{owner}/{repo}/languages", headers=headers, timeout=10)
            languages = lang_res.json() if lang_res.status_code == 200 else {}

            # 3. Fetch Commit Count
            commit_count = RepoAnalyzer._get_commit_count(owner, repo, headers)

            # 4. Fetch Tree for Files/Structure Analysis
            tree_url = f"{RepoAnalyzer.BASE_URL}/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
            tree_res = requests.get(tree_url, headers=headers, timeout=10)
            
            has_readme = False
            has_tests = False
            file_count = 0
            
            if tree_res.status_code == 200:
                tree_data = tree_res.json().get("tree", [])
                for item in tree_data:
                    path = item.get("path", "").lower()
                    if item.get("type") == "blob":
                        file_count += 1
                        if "readme" in path:
                            has_readme = True
                    
                    if item.get("type") == "tree":
                        if any(t in path for t in ["test", "tests", "spec", "specs"]):
                            has_tests = True

            metrics = {
                "repo_name": repo_data.get("full_name"),
                "default_branch": default_branch,
                "commit_count": commit_count,
                "has_readme": has_readme,
                "has_tests": has_tests,
                "file_count": file_count,
                "languages": list(languages.keys()),
                "stars": repo_data.get("stargazers_count", 0),
                "forks": repo_data.get("forks_count", 0),
                "is_private": repo_data.get("private", False),
                "last_updated": repo_data.get("updated_at")
            }

            logger.info(f"Analyzed repository: {metrics['repo_name']} with {file_count} files.")
            return metrics

        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API Error: {str(e)}")
            raise HTTPException(status_code=502, detail="External service (GitHub) error.")
        except Exception as e:
            logger.error(f"Unexpected error analyzing repo: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal analysis failure: {str(e)}")

if __name__ == "__main__":
    # Local dry run
    import json
    try:
        test_url = "https://github.com/fastapi/fastapi"
        print(f"Testing analysis for: {test_url}")
        result = RepoAnalyzer.analyze_repo(test_url)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Analysis failed: {e}")
