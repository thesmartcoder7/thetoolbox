from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import re
from .analyzer import RepositoryAnalyzer

def extract_repo_name(repo_input: str) -> str:
    """Extracts 'owner/repo' from a full GitHub URL or returns the input if already formatted."""
    pattern = r"https://github\.com/([^/]+/[^/]+)"
    match = re.match(pattern, repo_input)
    return match.group(1) if match else repo_input

@api_view(["POST"])
def analyze_repository(request):
    repo_input = request.data["repository"]
    
    if not repo_input:
        return Response({"error": "Repository is required"}, status=status.HTTP_400_BAD_REQUEST)

    repo_full_name = extract_repo_name(repo_input)
    print(f"Running Repository Analysis on {repo_full_name} . . .\n")

    if '/' not in repo_full_name:
        return Response({"error": "Invalid repository format. Use 'owner/repo' or a valid GitHub URL"}, status=status.HTTP_400_BAD_REQUEST)

    owner, repo_name = repo_full_name.split('/', 1)

    # Perform real-time analysis
    analyzer = RepositoryAnalyzer(owner, repo_name)
    analysis_data = analyzer.analyze()
    
    print(f"{repo_full_name} analysis complete!\n")


    return Response({
        "repository": repo_full_name,
        "analysis_results": analysis_data
    }, status=status.HTTP_200_OK)
