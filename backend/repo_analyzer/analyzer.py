import re
import numpy as np
from .github_api import GitHubAPI
from concurrent.futures import ThreadPoolExecutor, as_completed


class RepositoryAnalyzer:
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.github_api = GitHubAPI()


    def fetch_data(self):
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.github_api.get_repository, self.owner, self.repo): 'repo_data',
                executor.submit(self.github_api.get_readme, self.owner, self.repo): 'readme_data',
                executor.submit(self.github_api.get_commits, self.owner, self.repo): 'commits_data',
                executor.submit(self.github_api.get_issues, self.owner, self.repo): 'issues_data',
                executor.submit(self.github_api.get_pull_requests, self.owner, self.repo): 'prs_data',
                executor.submit(self.github_api.get_languages, self.owner, self.repo): 'languages_data',
                executor.submit(self.github_api.get_contributors, self.owner, self.repo): 'contributors_data',
                executor.submit(self.github_api.get_release_frequency, self.owner, self.repo): 'release_frequency',
                executor.submit(self.github_api.get_code_frequency, self.owner, self.repo): 'code_frequency',
                executor.submit(self.github_api.get_dependency_graph, self.owner, self.repo): 'dependency_graph',
            }

            data = {}
            for future in as_completed(futures):
                key = futures[future]
                try:
                    data[key] = future.result()
                except Exception as e:
                    print(f"Error fetching {key}: {str(e)}")
                    data[key] = None

            return data


    def analyze(self):
        try:
            data = self.fetch_data()

            scores = {
                'readme_quality': self.analyze_readme(data['readme_data']),
                'documentation': self.analyze_documentation(data['repo_data']),
                'code_quality': self.analyze_code_quality(data['repo_data']),
                'community_health': self.analyze_community_health(data['repo_data']),
                'contributor_analysis': self.analyze_contributors(data['contributors_data']),
            }

            other_scores = {
                'commit_history': self.analyze_commit_history(data['commits_data']),
                'issues_and_prs': self.analyze_issues_and_prs(data['issues_data'], data['prs_data']),
                'language_diversity': self.analyze_language_diversity(data['languages_data']),
                'code_churn': self.analyze_code_churn(data['code_frequency']),
                'dependency_health': self.analyze_dependencies(data['dependency_graph']),
            }
            # Ensure all scores are within 0-100 range
            scores = {k: max(0, min(v, 100)) for k, v in scores.items()}

            # Compute overall score
            overall_scores = sum(scores.values()) / len(scores)

            # Get category descriptions
            category_descriptions = self.get_category_descriptions()

            # Include details for each category
            detailed_results = []
            for category, score in scores.items():
                details = getattr(self, f"get_{category}_details")(data)  # Fetch details
                details['description'] = category_descriptions.get(category, "No description available")
                details['score'] = score  # Include score in details
                details['category'] = category.replace('_',' ').title(),
                detailed_results.append(details)
            
            optionals = []
            for category, score in other_scores.items():
                details = getattr(self, f"get_{category}_details")(data)  # Fetch details
                details['description'] = category_descriptions.get(category, "No description available")
                details['score'] = score  # Include score in details
                details['category'] = category.replace('_',' ').title()
                optionals.append(details)

            # Return all processed data
            return {
                "user": self.github_api.get_user_details(self.owner),
                "overall_score": overall_scores,
                "optionals": optionals,
                "detailed_results": detailed_results  # Includes scores + descriptions
            }

        except Exception as e:
            print(f"Error analyzing repository {self.owner}/{self.repo}: {str(e)}")
            return {"error": str(e), "overall_score": 0, "detailed_scores": {}}


    def analyze_readme(self, readme_content):
        if not readme_content:
            return 0

        score = 0
        max_score = 5

        # Check for presence of key sections
        sections = ['installation', 'usage', 'contributing', 'license']
        for section in sections:
            if re.search(rf'\b{section}\b', readme_content, re.IGNORECASE):
                score += 1

        # Check for code examples
        if re.search(r'```[\s\S]*?```', readme_content):
            score += 1

        return max(0, min((score / max_score) * 100, 100))


    def analyze_commit_history(self, commits_data):
        if not commits_data:
            return 0

        score = 0
        max_score = 5

        # Check commit frequency
        if len(commits_data) >= 50:
            score += 2
        elif len(commits_data) >= 20:
            score += 1

        # Check commit message quality
        good_messages = sum(1 for commit in commits_data if len(commit['commit']['message']) > 10)
        if good_messages / len(commits_data) >= 0.8:
            score += 2
        elif good_messages / len(commits_data) >= 0.5:
            score += 1

        # Check for recent activity
        if commits_data and (commits_data[0]['commit']['author']['date'] > '2023-01-01'):
            score += 1

        return max(0, min((score / max_score) * 100, 100))


    def analyze_issues_and_prs(self, issues_data, prs_data):
        score = 0
        max_score = 5

        # Check for presence of issues and PRs
        if issues_data:
            score += 1
        if prs_data:
            score += 1

        # Check for recent activity
        recent_issues = sum(1 for issue in issues_data if issue['created_at'] > '2023-01-01')
        recent_prs = sum(1 for pr in prs_data if pr['created_at'] > '2023-01-01')
        if recent_issues + recent_prs > 0:
            score += 1

        # Check for closed issues and merged PRs
        closed_issues = sum(1 for issue in issues_data if issue['state'] == 'closed')
        merged_prs = sum(1 for pr in prs_data if pr['state'] == 'closed' and pr['merged_at'])
        if closed_issues + merged_prs > 0:
            score += 1

        # Check for issue and PR templates
        if self.github_api.get_contents(self.owner, self.repo, '.github/ISSUE_TEMPLATE'):
            score += 0.5
        if self.github_api.get_contents(self.owner, self.repo, '.github/PULL_REQUEST_TEMPLATE.md'):
            score += 0.5

        return max(0, min((score / max_score) * 100, 100))


    def analyze_documentation(self, repo_data):
        score = 0
        max_score = 5

        # Check for wiki
        if repo_data['has_wiki']:
            score += 1

        # Check for GitHub Pages
        if repo_data['has_pages']:
            score += 1

        # Check for documentation folder
        if self.github_api.get_contents(self.owner, self.repo, 'docs'):
            score += 1

        # Check for API documentation (e.g., Swagger, OpenAPI)
        if self.github_api.get_contents(self.owner, self.repo, 'api-docs') or \
           self.github_api.get_contents(self.owner, self.repo, 'swagger.json') or \
           self.github_api.get_contents(self.owner, self.repo, 'openapi.yaml'):
            score += 1

        # Check for contributing guidelines
        if self.github_api.get_contents(self.owner, self.repo, 'CONTRIBUTING.md'):
            score += 1

        return max(0, min((score / max_score) * 100, 100))


    def analyze_code_quality(self, repo_data):
        score = 0
        max_score = 5

        # Check for presence of linter configuration files
        linter_files = ['.eslintrc', '.pylintrc', 'rubocop.yml', 'checkstyle.xml']
        for linter_file in linter_files:
            if self.github_api.get_contents(self.owner, self.repo, linter_file):
                score += 1
                break

        # Check for presence of formatter configuration files
        formatter_files = ['.prettierrc', 'black.toml', '.editorconfig']
        for formatter_file in formatter_files:
            if self.github_api.get_contents(self.owner, self.repo, formatter_file):
                score += 1
                break

        # Check for presence of test files
        if self.github_api.get_contents(self.owner, self.repo, 'tests') or \
           self.github_api.get_contents(self.owner, self.repo, 'spec'):
            score += 1

        # Check for CI configuration
        if self.github_api.get_contents(self.owner, self.repo, '.github/workflows') or \
           self.github_api.get_contents(self.owner, self.repo, '.travis.yml') or \
           self.github_api.get_contents(self.owner, self.repo, 'circle.yml'):
            score += 1

        # Check for dependency management files
        if self.github_api.get_contents(self.owner, self.repo, 'requirements.txt') or \
           self.github_api.get_contents(self.owner, self.repo, 'package.json') or \
           self.github_api.get_contents(self.owner, self.repo, 'Gemfile'):
            score += 1


        print(f"check score: {score}")

        return max(0, min((score / max_score) * 100, 100))


    def analyze_community_health(self, repo_data):
        score = 0
        max_score = 5

        # Check for code of conduct
        if self.github_api.get_contents(self.owner, self.repo, 'CODE_OF_CONDUCT.md'):
            score += 1

        # Check for license
        if repo_data['license']:
            score += 1

        # Check for security policy
        if self.github_api.get_contents(self.owner, self.repo, 'SECURITY.md'):
            score += 1

        # Check for issue templates
        if self.github_api.get_contents(self.owner, self.repo, '.github/ISSUE_TEMPLATE'):
            score += 1

        # Check for PR template
        if self.github_api.get_contents(self.owner, self.repo, '.github/PULL_REQUEST_TEMPLATE.md'):
            score += 1

        return max(0, min((score / max_score) * 100, 100))


    def analyze_language_diversity(self, languages_data):
        if not languages_data:
            return 0

        total_lines = sum(languages_data.values())
        language_percentages = {lang: lines / total_lines * 100 for lang, lines in languages_data.items()}
        
        # Calculate Shannon diversity index
        h = -sum((p/100) * np.log(p/100) for p in language_percentages.values() if p > 0)
        max_h = np.log(len(languages_data))
        diversity_index = h / max_h if max_h > 0 else 0

        # Scale the diversity index to a 0-100 score
        return max(0, min(diversity_index * 100, 100))


    def analyze_contributors(self, contributors_data):
        if not contributors_data:
            return 0

        num_contributors = len(contributors_data)
        contributions = [c['contributions'] for c in contributors_data]
        
        # Calculate Gini coefficient for contribution inequality
        sorted_contributions = sorted(contributions)
        cumulative_contributions = np.cumsum(sorted_contributions)
        lorenz_curve = cumulative_contributions / cumulative_contributions[-1]
        gini = (np.trapz(np.linspace(0, 1, len(contributions)), lorenz_curve) - 0.5) / 0.5

        # Score based on number of contributors and contribution equality
        score = (num_contributors / 10) * 50 + (1 - gini) * 50
        return max(0, min(score, 100))


    def analyze_release_management(self, release_frequency):
        if release_frequency is None:
            return 0

        # Score based on release frequency (releases per month)
        if release_frequency >= 2:
            return 100
        elif release_frequency >= 1:
            return 75
        elif release_frequency >= 0.5:
            return 50
        elif release_frequency > 0:
            return 25
        else:
            return 0


    def analyze_code_churn(self, code_frequency):
        if not code_frequency:
            return 0

        # Calculate net code growth and churn rate
        total_additions = sum(week[1] for week in code_frequency)
        total_deletions = sum(abs(week[2]) for week in code_frequency)
        net_growth = total_additions - total_deletions
        churn_rate = (total_additions + total_deletions) / (net_growth if net_growth > 0 else 1)

        # Score based on churn rate (lower is better)
        if churn_rate <= 1.5:
            return 100
        elif churn_rate <= 2:
            return 75
        elif churn_rate <= 3:
            return 50
        elif churn_rate <= 5:
            return 25
        else:
            return 0


    def analyze_dependencies(self, dependency_graph):
        if dependency_graph is None:
            return 0

        total_deps = sum(len(manifest['resolved']) for manifest in dependency_graph['manifests'].values())
        outdated_deps = sum(len(manifest['outdated']) for manifest in dependency_graph['manifests'].values())
        vulnerable_deps = sum(len(manifest['vulnerabilities']) for manifest in dependency_graph['manifests'].values())

        if total_deps == 0:
            return 0

        up_to_date_ratio = (total_deps - outdated_deps) / total_deps
        secure_ratio = (total_deps - vulnerable_deps) / total_deps

        score = (up_to_date_ratio * 50) + (secure_ratio * 50)
        return max(0, min(score, 100))


    def get_category_descriptions(self):
        return {
            'readme_quality': "Evaluates the completeness and clarity of the README file, which is often the first point of contact for new users and contributors.",
            'commit_history': "Analyzes the frequency, recency, and quality of commits, indicating the project's active development and maintenance.",
            'issues_and_prs': "Examines the management of issues and pull requests, reflecting the project's responsiveness to user feedback and external contributions.",
            'documentation': "Assesses the availability and comprehensiveness of project documentation, crucial for user understanding and contributor onboarding.",
            'code_quality': "Evaluates the presence of code quality tools and practices, which contribute to maintainable and reliable code.",
            'community_health': "Measures the presence of community guidelines and policies that foster a welcoming and productive open-source environment.",
            'language_diversity': "Analyzes the variety of programming languages used, which can indicate the project's complexity and potential for cross-platform support.",
            'contributor_analysis': "Examines the number and distribution of contributors, reflecting the project's collaborative nature and bus factor.",
            'release_management': "Evaluates the frequency and regularity of releases, indicating the project's stability and ongoing development.",
            'code_churn': "Measures the rate of code changes over time, which can indicate development activity and potential instability.",
            'dependency_health': "Assesses the status of project dependencies, crucial for security and compatibility."
        }


# get details 
    def get_readme_quality_details(self, data):
        readme_content = data['readme_data']
        details = {
            'has_installation': 'installation' in readme_content.lower(),
            'has_usage': 'usage' in readme_content.lower(),
            'has_contributing': 'contributing' in readme_content.lower(),
            'has_license': 'license' in readme_content.lower(),
            'has_code_examples': bool(re.search(r'```[\s\S]*?```', readme_content)),
        }
        recommendations = []
        if not details['has_installation']:
            recommendations.append({
                "text": "Add an installation section to your README",
                "link": "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes#adding-a-readme-to-your-repository"
            })
        if not details['has_usage']:
            recommendations.append({
                "text": "Include usage instructions in your README",
                "link": "https://www.makeareadme.com/#usage"
            })
        if not details['has_contributing']:
            recommendations.append({
                "text": "Add contributing guidelines to your README",
                "link": "https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors"
            })
        if not details['has_license']:
            recommendations.append({
                "text": "Include license information in your README",
                "link": "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository"
            })
        if not details['has_code_examples']:
            recommendations.append({
                "text": "Add code examples to your README",
                "link": "https://www.markdownguide.org/extended-syntax/#fenced-code-blocks"
            })
        
        final_data = {
            'criteria': details,
            'recommendations': recommendations
        }
        return final_data


    def get_commit_history_details(self, data):
        commits_data = data['commits_data']
        details = {
            'total_commits': len(commits_data),
            'recent_commits': sum(1 for commit in commits_data if commit['commit']['author']['date'] > '2023-01-01'),
            'avg_commit_message_length': sum(len(commit['commit']['message']) for commit in commits_data) / len(commits_data),
        }
        recommendations = []
        if details['total_commits'] < 50:
            recommendations.append({
                "text": "Increase the number of commits to show active development",
                "link": "https://github.com/git-guides/git-commit"
            })
        if details['recent_commits'] < 10:
            recommendations.append({
                "text": "Make more recent commits to show the project is actively maintained",
                "link": "https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/about-commits"
            })
        if details['avg_commit_message_length'] < 20:
            recommendations.append({
                "text": "Write more descriptive commit messages",
                "link": "https://cbea.ms/git-commit/"
            })

        final_data = {
            'criteria': details,
            'recommendations': recommendations
        }
        return final_data


    def get_issues_and_prs_details(self, data):
        issues_data, prs_data = data['issues_data'], data['prs_data']
        details = {
            'open_issues': sum(1 for issue in issues_data if issue['state'] == 'open'),
            'closed_issues': sum(1 for issue in issues_data if issue['state'] == 'closed'),
            'open_prs': sum(1 for pr in prs_data if pr['state'] == 'open'),
            'merged_prs': sum(1 for pr in prs_data if pr['state'] == 'closed' and pr['merged_at']),
        }
        recommendations = []
        if details['open_issues'] > details['closed_issues']:
            recommendations.append({
                "text": "Work on closing more open issues",
                "link": "https://docs.github.com/en/issues/tracking-your-work-with-issues/closing-issues"
            })
        if details['open_prs'] > 5:
            recommendations.append({
                "text": "Review and merge (or close) open pull requests",
                "link": "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews"
            })
        if not self.github_api.get_contents(self.owner, self.repo, '.github/ISSUE_TEMPLATE'):
            recommendations.append({
                "text": "Add issue templates to streamline issue creation",
                "link": "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository"
            })
        if not self.github_api.get_contents(self.owner, self.repo, '.github/PULL_REQUEST_TEMPLATE.md'):
            recommendations.append({
                "text": "Add a pull request template to guide contributors",
                "link": "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository"
            })
        
        final_data = {
            'criteria': details,
            'recommendations': recommendations
        }
        return final_data


    def get_documentation_details(self, data):
        repo_data = data['repo_data']
        details = {
            'has_wiki': repo_data['has_wiki'],
            'has_pages': repo_data['has_pages'],
            'has_docs_folder': self.github_api.get_contents(self.owner, self.repo, 'docs') is not None,
            'has_api_docs': (self.github_api.get_contents(self.owner, self.repo, 'api-docs') is not None or
                             self.github_api.get_contents(self.owner, self.repo, 'swagger.json') is not None or
                             self.github_api.get_contents(self.owner, self.repo, 'openapi.yaml') is not None),
            'has_contributing_guidelines': self.github_api.get_contents(self.owner, self.repo, 'CONTRIBUTING.md') is not None,
        }
        recommendations = []
        if not details['has_wiki']:
            recommendations.append({
                "text": "Consider enabling the Wiki for comprehensive documentation",
                "link": "https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis"
            })
        if not details['has_pages']:
            recommendations.append({
                "text": "Set up GitHub Pages for project documentation",
                "link": "https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site"
            })
        if not details['has_docs_folder']:
            recommendations.append({
                "text": "Create a 'docs' folder for detailed documentation",
                "link": "https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/"
            })
        if not details['has_api_docs']:
            recommendations.append({
                "text": "Add API documentation (e.g., Swagger, OpenAPI)",
                "link": "https://swagger.io/specification/"
            })
        if not details['has_contributing_guidelines']:
            recommendations.append({
                "text": "Create a CONTRIBUTING.md file with guidelines for contributors",
                "link": "https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors"
            })
        
        final_data = {
            'criteria': details,
            'recommendations': recommendations
        }
        return final_data


    def get_code_quality_details(self, data):
        repo_data = data['repo_data']
        details = {
            'has_linter': any(self.github_api.get_contents(self.owner, self.repo, lf) for lf in ['.eslintrc', '.pylintrc', 'rubocop.yml', 'checkstyle.xml']),
            'has_formatter': any(self.github_api.get_contents(self.owner, self.repo, ff) for ff in ['.prettierrc', 'black.toml', '.editorconfig']),
            'has_tests': (self.github_api.get_contents(self.owner, self.repo, 'tests') is not None or
                          self.github_api.get_contents(self.owner, self.repo, 'spec') is not None),
            'has_ci': (self.github_api.get_contents(self.owner, self.repo, '.github/workflows') is not None or
                       self.github_api.get_contents(self.owner, self.repo, '.travis.yml') is not None or
                       self.github_api.get_contents(self.owner, self.repo, 'circle.yml') is not None),
            'has_dependency_management': (self.github_api.get_contents(self.owner, self.repo, 'requirements.txt') is not None or
                                          self.github_api.get_contents(self.owner, self.repo, 'package.json') is not None or
                                          self.github_api.get_contents(self.owner, self.repo, 'Gemfile') is not None),
        }
        recommendations = []
        if not details['has_linter']:
            recommendations.append({
                "text": "Add a linter configuration file (e.g., .eslintrc, .pylintrc)",
                "link": "https://sourcelevel.io/blog/what-is-a-linter-and-why-your-team-should-use-it"
            })
        if not details['has_formatter']:
            recommendations.append({
                "text": "Add a code formatter configuration file (e.g., .prettierrc, black.toml)",
                "link": "https://prettier.io/docs/en/why-prettier.html"
            })
        if not details['has_tests']:
            recommendations.append({
                "text": "Add unit tests and integration tests",
                "link": "https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration"
            })
        if not details['has_ci']:
            recommendations.append({
                "text": "Set up Continuous Integration (CI) for automated testing",
                "link": "https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration"
            })
        if not details['has_dependency_management']:
            recommendations.append({
                "text": "Add a dependency management file (e.g., requirements.txt, package.json)",
                "link": "https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry#installing-a-package"
            })
        
        final_data = {
            'criteria': details,
            'recommendations': recommendations
        }
        return final_data


    def get_community_health_details(self, data):
        repo_data = data['repo_data']
        details = {
            'has_code_of_conduct': self.github_api.get_contents(self.owner, self.repo, 'CODE_OF_CONDUCT.md') is not None,
            'has_license': repo_data['license'] is not None,
            'has_security_policy': self.github_api.get_contents(self.owner, self.repo, 'SECURITY.md') is not None,
            'has_issue_templates': self.github_api.get_contents(self.owner, self.repo, '.github/ISSUE_TEMPLATE') is not None,
            'has_pr_template': self.github_api.get_contents(self.owner, self.repo, '.github/PULL_REQUEST_TEMPLATE.md') is not None,
        }
        recommendations = []
        if not details['has_code_of_conduct']:
            recommendations.append({
                "text": "Add a CODE_OF_CONDUCT.md file",
                "link": "https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project"
            })
        if not details['has_license']:
            recommendations.append({
                "text": "Add a license to your repository",
                "link": "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository"
            })
        if not details['has_security_policy']:
            recommendations.append({
                "text": "Create a SECURITY.md file with security guidelines",
                "link": "https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository"
            })
        if not details['has_issue_templates']:
            recommendations.append({
                "text": "Add issue templates to streamline issue creation",
                "link": "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository"
            })
        if not details['has_pr_template']:
            recommendations.append({
                "text": "Add a pull request template to guide contributors",
                "link": "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository"
            })
        
        final_data = {
            'criteria': details,
            'recommendations': recommendations
        }
        return final_data


    def get_language_diversity_details(self, data):
        languages_data = data['languages_data']
        total_lines = sum(languages_data.values())
        details = {
            'languages': {lang: lines / total_lines * 100 for lang, lines in languages_data.items()},
            'total_lines': total_lines,
        }
        recommendations = []
        if len(details['languages']) < 2:
            recommendations.append({"text":"Consider using multiple languages to increase project versatility"})
        if max(details['languages'].values()) > 80:
            recommendations.append({"text":"Reduce reliance on a single language to improve maintainability"})

        final_data = {
            'criteria': details,
            'recommendations': recommendations
        }
        return final_data


    def get_contributor_analysis_details(self, data):
        contributors_data = data['contributors_data']
        recommendations = []
        details = {
            'num_contributors': len(contributors_data),
            'top_contributors': [
                {'login': c['login'], 'contributions': c['contributions']}
                for c in sorted(contributors_data, key=lambda x: x['contributions'], reverse=True)[:5]
            ],
        }
       
        final_data = {
            'criteria': details,
            'recommendations': recommendations
        }
        return final_data


    def get_release_management_details(self, data):
        release_frequency = data['release_frequency']
        details = {
            'release_frequency': release_frequency,
        }
        recommendations = []
        if release_frequency is None or release_frequency < 0.5:
            recommendations.append({
                "text": "Establish a regular release schedule (aim for at least one release every two months)",
                "link": "https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases"
            })
        elif release_frequency < 1:
            recommendations.append({
                "text": "Consider increasing your release frequency to at least once a month",
                "link": "https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository"
            })

        final_data = {
            'criteria': details,
            'recommendations': recommendations
        }
        return final_data


    def get_code_churn_details(self, data):
        code_frequency = data['code_frequency']
        if not code_frequency:
            return {'recommendations': [{
                "text": "Start tracking code changes to analyze code churn",
                "link": "https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/understanding-repository-activity"
            }]}
        
        total_additions = sum(week[1] for week in code_frequency)
        total_deletions = sum(abs(week[2]) for week in code_frequency)
        net_growth = total_additions - total_deletions
        churn_rate = (total_additions + total_deletions) / (net_growth if net_growth > 0 else 1)
        
        details = {
            'churn_rate': churn_rate,
            'net_growth': net_growth,
        }
        recommendations = []
        if churn_rate > 3:
            recommendations.append({
                "text": "Reduce code churn by focusing on code stability and refactoring",
                "link": "https://understandlegacycode.com/blog/reduce-codebase-churn-with-boy-scout-rule/"
            })
        if net_growth < 0:
            recommendations.append({
                "text": "The codebase is shrinking. Consider if this aligns with project goals",
                "link": "https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/analyzing-changes-to-a-repositorys-content"
            })

        final_data = {
            'criteria': details,
            'recommendations': recommendations
        }
        return final_data


    def get_dependency_health_details(self, data):
        dependency_graph = data['dependency_graph']
        if dependency_graph is None:
            return {'recommendations': [{
                "text": "Enable dependency graph in your repository settings to analyze dependencies",
                "link": "https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-the-dependency-graph"
            }]}
        
        total_deps = sum(len(manifest['resolved']) for manifest in dependency_graph['manifests'].values())
        outdated_deps = sum(len(manifest['outdated']) for manifest in dependency_graph['manifests'].values())
        vulnerable_deps = sum(len(manifest['vulnerabilities']) for manifest in dependency_graph['manifests'].values())
        
        details = {
            'total_dependencies': total_deps,
            'outdated_dependencies': outdated_deps,
            'vulnerable_dependencies': vulnerable_deps,
        }
        recommendations = []
        if outdated_deps > 0:
            recommendations.append({
                "text": f"Update {outdated_deps} outdated dependencies",
                "link": "https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-dependencies-updated-automatically"
            })
        if vulnerable_deps > 0:
            recommendations.append({
                "text": f"Address {vulnerable_deps} vulnerable dependencies immediately",
                "link": "https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts"
            })
        if total_deps > 100:
            recommendations.append({
                "text": "Consider reducing the number of dependencies to improve maintainability",
                "link": "https://blog.npmjs.org/post/141577284765/kik-left-pad-and-npm"
            })
        
        final_data = {
            'criteria': details,
            'recommendations': recommendations
        }
        return final_data