"""Migration runner script for the Data Ingestion Service."""

import sys
import os
from alembic.config import CommandLine

# --- Path Setup ---
# Ensures that the project's root directory is on the Python path,
# so that modules like 'data_ingestion_service' can be found by Alembic.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def main():
    """
    A wrapper for the Alembic command line interface.

    This script sets the correct Python path before invoking Alembic,
    passing through any command-line arguments.
    """
    print("--- Running Alembic with project path configured ---")
    CommandLine().main(argv=sys.argv[1:])


if __name__ == "__main__":
    main()
