import os
import sys
import json
from github import Github
import openai

class PRReviewer:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.pr_number = int(os.getenv('PR_NUMBER'))
        self.repo_owner = os.getenv('REPO_OWNER')
        self.repo_name = os.getenv('REPO_NAME')
        
        if not all([self.github_token, self.openai_key, self.pr_number, 
                   self.repo_owner, self.repo_name]):
            raise ValueError("Missing required environment variables")
        
        self.gh = Github(self.github_token)
        self.repo = self.gh.get_repo(f"{self.repo_owner}/{self.repo_name}")
        self.pr = self.repo.get_pull(self.pr_number)
        self.client = openai.Client(api_key=self.openai_key)

    def get_pr_diff(self):
        """Fetch the PR diff from GitHub"""
        return self.pr.get_diff()

    def analyze_diff(self, diff):
        """Send diff to OpenAI API for analysis"""
        system_prompt = """You are a code reviewer. Analyze the provided diff and:
        1. Identify potential issues in:
           - Code quality
           - Best practices
           - Logic errors
           - Variable/function/class naming
        2. Provide specific, actionable feedback
        3. Decide whether to approve or request changes
        
        Format your response as JSON:
        {
            "comments": [
                {"path": "file_path", "line": line_number, "body": "comment"},
                ...
            ],
            "decision": "approve|request_changes",
            "summary": "Overall review summary"
        }
        """

        print(f"Sending diff to OpenAI API with model: {self.openai_model}")

        response = self.client.chat.completions.create(
            model=self.openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": diff}
            ],
            response_format={ "type": "json_object" }
        )
        
        return json.loads(response.choices[0].message.content)

    def submit_review(self, analysis):
        """Submit the review to GitHub"""
        # Post individual comments
        for comment in analysis['comments']:
            self.pr.create_review_comment(
                body=comment['body'],
                commit_id=self.pr.get_commits().reversed[0].sha,
                path=comment['path'],
                line=comment['line']
            )
        
        # Submit the overall review
        review_event = 'APPROVE' if analysis['decision'] == 'approve' else 'REQUEST_CHANGES'
        self.pr.create_review(
            body=analysis['summary'],
            event=review_event
        )

    def review(self):
        """Main review process"""
        try:
            diff = self.get_pr_diff()
            analysis = self.analyze_diff(diff)
            print("PR review analysis:")
            print(analysis)
            self.submit_review(analysis)
            
        except Exception as e:
            print(f"Error during review process: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    reviewer = PRReviewer()
    reviewer.review()