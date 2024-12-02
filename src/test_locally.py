from dotenv import load_dotenv

load_dotenv() 
import os
import json
from review_pr import PRReviewer
from unittest.mock import MagicMock, patch

class MockPR:
    def __init__(self):
        self.diff = """diff --git a/example.py b/example.py
--- a/example.py
+++ b/example.py
@@ -1,5 +1,5 @@
-def bad_func():
-    x = 1
+def calculate_total(items):
+    total = sum(items)
-    return x
+    return total"""
    
    def get_diff(self):
        return self.diff
        
    # Add new methods
    def create_review_comment(self, body, commit_id, path, line):
        print(f"Mock: Creating review comment - {body}")
        return None

    def get_commits(self):
        mock_commit = MagicMock()
        mock_commit.sha = "fake_sha"
        return MagicMock(reversed=[mock_commit])

    def create_review(self, body, event):
        print(f"Mock: Creating review - {body} with event {event}")
        return None

def mock_environment():
    """Set up mock environment variables"""
    os.environ['GITHUB_TOKEN'] = 'fake_token'
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    os.environ['OPENAI_MODEL'] = 'gpt-3.5-turbo'
    os.environ['PR_NUMBER'] = '1'
    os.environ['REPO_OWNER'] = 'test_owner'
    os.environ['REPO_NAME'] = 'test_repo'

def test_pr_review():
    """Test the PR review process"""
    mock_environment()
    
    with patch('review_pr.Github') as mock_github:
        # Set up mock objects
        mock_repo = MagicMock()
        mock_pr = MockPR()
        mock_github.return_value.get_repo.return_value = mock_repo
        mock_repo.get_pull.return_value = mock_pr
        
        # Run the review
        reviewer = PRReviewer()
        reviewer.review()

if __name__ == "__main__":
    test_pr_review() 