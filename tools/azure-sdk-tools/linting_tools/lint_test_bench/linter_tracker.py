#!/usr/bin/env python

# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Script to generate a benchmark table of packages that have pylint issues."""

import os
import re
import json
import argparse
import datetime
import subprocess
import tempfile
import concurrent.futures
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from github import Github, Issue
from tabulate import tabulate


class LintingIssueTracker:
    """Class to track linting issues from GitHub and generate benchmark reports."""

    def __init__(
        self,
        github_token: str,
        repo_name: str = "Azure/azure-sdk-for-python",
        repo_path: Optional[str] = None,
    ):
        """Initialize the LintingIssueTracker.

        :param github_token: GitHub personal access token for API authentication
        :param repo_name: GitHub repository in format 'owner/repo'
        :param repo_path: Local path to the repository
        """
        self.repo_name = repo_name
        self.repo_path = repo_path or os.getcwd()
        
        # Create Github instance with token
        self.github = Github(github_token)
            
        # Get the repository
        self.repo = self.github.get_repo(repo_name)

    def fetch_linting_issues(self, search_term: str = "needs linting for pylint") -> List[Issue.Issue]:
        """Fetch GitHub issues that have the specified search term in the title.

        :param search_term: The term to search for in issue titles
        :return: List of GitHub Issue objects
        """
        # Search for open issues with the search term in the title
        query = f"repo:{self.repo_name} is:issue is:open {search_term} in:title"
        issues = self.github.search_issues(query=query)
        
        return list(issues)

    def extract_package_names(self, issues: List[Issue.Issue]) -> Set[str]:
        """Extract package names from linting issue titles.

        :param issues: List of GitHub Issue objects
        :return: Set of package names with linting issues
        """
        package_names = set()
        
        # Updated pattern to match formats like:
        # "needs linting for pylint - azure-xxx-yyy"
        # "needs linting for pylint: azure-xxx-yyy" 
        # Look for any text containing "azure-" followed by package name
        pattern = r"(azure-[a-zA-Z0-9][a-zA-Z0-9-]*)"
        
        for issue in issues:
            # First try to find in the title
            matches = re.search(pattern, issue.title)
            if matches:
                package_name = matches.group(1).lower()
                package_names.add(package_name)
            # Also check the body for more context
            elif issue.body:
                body_matches = re.search(pattern, issue.body)
                if body_matches:
                    package_name = body_matches.group(1).lower()
                    package_names.add(package_name)
        
        return package_names
        
    def _find_package_path(self, package_name: str) -> Optional[str]:
        """Find the path to a package in the repository.
        
        :param package_name: The name of the package
        :return: The path to the package or None if not found
        """
        sdk_dir = os.path.join(self.repo_path, "sdk")
        direct_path = os.path.join(sdk_dir, package_name)
        
        if os.path.exists(direct_path):
            return direct_path
            
        # Try to find by searching through subdirectories
        parts = package_name.split("-")
        if len(parts) >= 3 and parts[0] == "azure":
            service_dir = os.path.join(sdk_dir, parts[1])
            if os.path.exists(service_dir):
                direct_path = os.path.join(service_dir, package_name)
                if os.path.exists(direct_path):
                    return direct_path
        
        # Try other common directory structures
        if len(parts) >= 2:
            service_dir = os.path.join(sdk_dir, parts[1])
            if os.path.exists(service_dir):
                direct_path = os.path.join(service_dir, package_name)
                if os.path.exists(direct_path):
                    return direct_path
        
        return None
        
    def get_pylint_score(self, package_name: str) -> str:
        """Run pylint on a package using tox and extract the score.
        
        :param package_name: The name of the package to lint
        :return: The pylint score as a string (e.g. "8.45/10") or "N/A" if not available
        """
        package_path = self._find_package_path(package_name)
        
        if not package_path:
            return "N/A (path not found)"
            
        try:
            # Change to package directory
            original_dir = os.getcwd()
            os.chdir(package_path)
            
            # Run tox with pylint environment and capture output
            # Using the recommended command from https://github.com/Azure/azure-sdk-for-python/blob/main/doc/dev/pylint_checking.md
            result = subprocess.run(
                ["tox", "-e", "next-pylint", "-c", "../../../eng/tox/tox.ini", "--root", "."],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )
            
            # Extract the score using regex
            # Looking for pattern like: "Your code has been rated at 8.45/10"
            score_pattern = r"Your code has been rated at (\d+\.\d+/\d+)"
            match = re.search(score_pattern, result.stdout)
            
            if match:
                return match.group(1)
            else:
                return "Error (score not found)"
                
        except subprocess.TimeoutExpired:
            return "Error (timeout)"
        except subprocess.SubprocessError:
            return "Error (process failed)"
        except Exception as e:
            return f"Error ({str(e)})"
        finally:
            # Return to original directory
            os.chdir(original_dir)
            
    def _get_pylint_score_wrapper(self, package_name: str) -> Tuple[str, str]:
        """Wrapper around get_pylint_score for parallel processing.
        
        :param package_name: The name of the package to lint
        :return: A tuple of (package_name, score)
        """
        score = self.get_pylint_score(package_name)
        return package_name, score

    def generate_benchmark_table(self, package_names: Set[str], include_scores: bool = True, max_workers: int = 4) -> str:
        """Generate a benchmark table with package names and pylint scores.

        :param package_names: Set of package names with linting issues
        :param include_scores: Whether to include pylint scores in the table
        :param max_workers: Maximum number of parallel processes to run tox
        :return: Formatted table as string
        """
        if not package_names:
            return "No packages with linting issues found."
            
        sorted_packages = sorted(package_names)
        
        if include_scores:
            # Get scores in parallel
            package_scores = {}
            print(f"Running pylint on {len(sorted_packages)} packages in parallel (max {max_workers} workers)...")
            
            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
                # Start the pylint operations and mark each future with its package
                future_to_package = {
                    executor.submit(self._get_pylint_score_wrapper, package): package 
                    for package in sorted_packages
                }
                
                # Process results as they complete
                completed = 0
                for future in concurrent.futures.as_completed(future_to_package):
                    package = future_to_package[future]
                    completed += 1
                    print(f"Progress: {completed}/{len(sorted_packages)} packages processed")
                    try:
                        package_name, score = future.result()
                        package_scores[package_name] = score
                    except Exception as exc:
                        print(f"{package} generated an exception: {exc}")
                        package_scores[package] = f"Error: {exc}"
            
            # Generate table data with scores
            table_data = [
                [idx + 1, package, "Needs Pylint Linting", package_scores.get(package, "Error")]
                for idx, package in enumerate(sorted_packages)
            ]
            headers = ["#", "Package Name", "Status", "Pylint Score"]
        else:
            # Generate table without scores (much faster)
            table_data = [
                [idx + 1, package, "Needs Pylint Linting"]
                for idx, package in enumerate(sorted_packages)
            ]
            headers = ["#", "Package Name", "Status"]
            
        return tabulate(table_data, headers=headers, tablefmt="grid")

    def generate_report(
        self, 
        search_term: str = "needs linting for pylint", 
        output_file: Optional[str] = None,
        include_scores: bool = True,
        max_workers: int = 4,
    ) -> str:
        """Generate a full benchmark report of packages with linting issues.

        :param search_term: Term to search for in issue titles
        :param output_file: Optional file to save the report to
        :param include_scores: Whether to include pylint scores in the table
        :param max_workers: Maximum number of parallel processes to run tox
        :return: Report as string
        """
        issues = self.fetch_linting_issues(search_term)
        package_names = self.extract_package_names(issues)
        
        report = []
        report.append(f"# Linting Benchmark Report - {datetime.datetime.now().strftime('%Y-%m-%d')}")
        report.append(f"Repository: {self.repo_name}")
        report.append(f"Issues found with '{search_term}' in title: {len(issues)}")
        report.append(f"Unique packages with linting issues: {len(package_names)}")
        report.append("\n## Benchmark Table")
        report.append(self.generate_benchmark_table(package_names, include_scores, max_workers))
        
        full_report = "\n\n".join(report)
        
        if output_file:
            with open(output_file, "w") as f:
                f.write(full_report)
            print(f"Report saved to {output_file}")
            
        return full_report


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate a benchmark table of packages with pylint linting issues"
    )
    parser.add_argument(
        "--token", "-t", 
        help="GitHub personal access token (or set GITHUB_TOKEN env var)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file to save the report to"
    )
    parser.add_argument(
        "--search", "-s",
        default="needs linting for pylint",
        help="Search term to look for in issue titles"
    )
    parser.add_argument(
        "--repo-path", "-p",
        help="Local path to the azure-sdk-for-python repository",
        default=os.getcwd()
    )
    parser.add_argument(
        "--no-scores", 
        action="store_true",
        help="Skip running tox to get pylint scores (faster but less information)"
    )
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=4,
        help="Maximum number of parallel workers for running tox (default: 4)"
    )
    
    args = parser.parse_args()
    
    # Get token from args or environment
    token = args.token or os.environ.get("GITHUB_TOKEN")
    
    if not token:
        print("Warning: No GitHub token provided. API rate limits may apply.")
        print("Set a token with --token or the GITHUB_TOKEN environment variable.")
        
    tracker = LintingIssueTracker(github_token=token, repo_path=args.repo_path)
    report = tracker.generate_report(
        search_term=args.search, 
        output_file=args.output,
        include_scores=not args.no_scores,
        max_workers=args.workers
    )
    
    print(report)


if __name__ == "__main__":
    main()