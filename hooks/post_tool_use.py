#!/usr/bin/env python3
import json
import os
import sys
import subprocess
from pathlib import Path

def run_linting(file_path):
    """
    Automatically perform code optimization and static analysis based on local configuration files.
    """
    # Only process existing Python files
    if not file_path.endswith('.py') or not os.path.exists(file_path):
        return None

    # 1. Execute auto-fixes (isort & black)
    # These tools will automatically locate and read pyproject.toml
    subprocess.run(["isort", file_path], capture_output=True)
    subprocess.run(["black", file_path], capture_output=True)
    
    # 2. Execute static analysis (flake8)
    # It will automatically locate and read .flake8
    result = subprocess.run(["flake8", file_path], capture_output=True, text=True)
    
    # If flake8 produces output, it indicates remaining logic or style issues for the AI to address
    if result.stdout.strip():
        return result.stdout.strip()
    
    return None

def main():
    try:
        # Read tool execution details passed from Claude via stdin
        input_data = json.load(sys.stdin)
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        error_to_feedback = None

        # Trigger condition: AI performed write-related operations
        if tool_name in ['Write', 'Edit', 'MultiEdit']:
            file_path = tool_input.get('file_path')
            if file_path:
                # Retrieve linting errors (if any)
                error_to_feedback = run_linting(file_path)

        # --- Logging Logic ---
        log_dir = Path.cwd() / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / 'post_tool_use.json'
        
        log_data = []
        if log_path.exists():
            with open(log_path, 'r') as f:
                try: 
                    log_data = json.load(f)
                except: 
                    pass
        
        log_data.append(input_data)
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

        # --- Feedback Loop ---
        if error_to_feedback:
            # Print errors to stderr; exit(2) prompts the AI to initiate self-correction
            print(f"\n[Quality Check Failed]\n{error_to_feedback}", file=sys.stderr)
            sys.exit(2) 

        sys.exit(0)
    except Exception:
        # Ensure the hook script itself doesn't block the AI workflow on failure
        sys.exit(0)

if __name__ == '__main__':
    main()