#!/usr/bin/env python3
"""
Root entry point for the todo application.
Detects whether to run in interactive mode or traditional CLI mode.
"""

import sys
import os
# Add the src directory to the path so we can import from cli
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.main import app
from cli.interactive import interactive_main


def main():
    """
    Main entry point that determines mode based on command-line arguments.
    - If args provided -> Run Typer CLI (existing logic)
    - If no args -> Run Interactive Mode (new logic)
    """
    # If command-line arguments are provided, run the CLI mode
    if len(sys.argv) > 1:
        # Forward to the existing Typer CLI app
        app()
    else:
        # Run the interactive mode
        interactive_main()


if __name__ == "__main__":
    main()