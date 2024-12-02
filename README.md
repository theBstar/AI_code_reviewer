# AI PR Reviewer

This GitHub Action automatically reviews pull requests using OpenAI's GPT-4 API.

## Usage

Add this to your workflow:

```yaml
- uses: thebstar/pr-reviewer@v1
  with:
    openai-api-key: ${{ secrets.OPENAI_API_KEY }}
    # Optional: specify a different model
    # model: 'gpt-4-turbo-preview'
```

## Features

- Automatically triggers on new pull requests
- Analyzes code changes for:
  - Code quality
  - Best practices
  - Logic errors
  - Naming conventions
- Provides inline comments with specific suggestions
- Automatically approves or requests changes

## Development

### Prerequisites

- Python 3.10+
- Poetry

### Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   poetry install
   ```

3. Set up environment variables:
   ```bash
   export GITHUB_TOKEN=your_github_token
   export OPENAI_API_KEY=your_openai_key
   export PR_NUMBER=1
   export REPO_OWNER=owner
   export REPO_NAME=repo
   ```

4. Run locally:
   ```bash
   poetry run python src/review_pr.py
   ```

## License

MIT 
