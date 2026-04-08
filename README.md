# Code Review OpenEnv

## Description
Simulates real-world code review tasks for AI agents.

## Tasks
- Easy: simple bug detection
- Medium: best practices
- Hard: security issues

## Run
pip install -r requirements.txt
python baseline/run_agent.py

## Docker
docker build -t code-review .
docker run code-review
