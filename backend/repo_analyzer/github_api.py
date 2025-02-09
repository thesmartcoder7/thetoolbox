import requests
import base64
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
import os

class GitHubAPI:
    BASE_URL = 'https://api.github.com'
    GITHUB_TOKEN = os.getenv('GITHUB_API_TOKEN')

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {self.GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
        })

    def get_repository(self, owner, repo):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_readme(self, owner, repo):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/readme'
        response = self.session.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        content = response.json()['content']
        return base64.b64decode(content).decode('utf-8')

    def get_commits(self, owner, repo, per_page=100):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/commits'
        params = {'per_page': per_page}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_issues(self, owner, repo, state='all', per_page=100):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/issues'
        params = {'state': state, 'per_page': per_page}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_pull_requests(self, owner, repo, state='all', per_page=100):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/pulls'
        params = {'state': state, 'per_page': per_page}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_contents(self, owner, repo, path):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/contents/{path}'
        response = self.session.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    
    # def file_exists_in_repo(self, owner, repo, filename):
    #     url = f"{self.BASE_URL}/search/code"
    #     params = {"q": f"repo:{owner}/{repo} filename:{filename}"}
    #     response = self.session.get(url, params=params)
    #     response.raise_for_status()
    #     return response.json()["total_count"] > 0

    # def directory_exists_in_repo(self, owner, repo, dir_path):
    #     url = f"{self.BASE_URL}/search/code"
    #     params = {"q": f"repo:{owner}/{repo} path:{dir_path}/"}
    #     response = self.session.get(url, params=params)
    #     response.raise_for_status()
    #     return response.json()["total_count"] > 0

    def get_languages(self, owner, repo):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/languages'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_contributors(self, owner, repo):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/contributors'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_release_frequency(self, owner, repo):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/releases'
        response = self.session.get(url)
        response.raise_for_status()
        releases = response.json()
        if len(releases) < 2:
            return None
        first_release = datetime.strptime(releases[-1]['published_at'], '%Y-%m-%dT%H:%M:%SZ')
        last_release = datetime.strptime(releases[0]['published_at'], '%Y-%m-%dT%H:%M:%SZ')
        days_between = (last_release - first_release).days
        return len(releases) / (days_between / 30)  # releases per month

    def get_commit_frequency(self, owner, repo):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/stats/commit_activity'
        response = self.session.get(url)
        response.raise_for_status()
        commit_activity = response.json()
        if not commit_activity:
            return 0  # Return 0 if there's no commit activity
        return sum(week['total'] for week in commit_activity) / len(commit_activity)

    def get_code_frequency(self, owner, repo):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/stats/code_frequency'
        response = self.session.get(url)
        response.raise_for_status()
        code_frequency = response.json()
        return code_frequency

    def get_dependency_graph(self, owner, repo):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/dependency-graph/compare/HEAD'
        response = self.session.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def get_commit_details(self, owner, repo, commit_sha):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/commits/{commit_sha}'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_contributor_details(self, owner, repo, username):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/contributors/{username}'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_code_frequency_by_file(self, owner, repo):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/stats/code_frequency'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_branches(self, owner, repo):
        url = f'{self.BASE_URL}/repos/{owner}/{repo}/branches'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    # Add more methods for other GitHub API endpoints as needed