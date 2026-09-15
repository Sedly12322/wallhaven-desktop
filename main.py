import sys
from pathlib import Path

# Ensure package root is in sys.path
sys.path.insert(0, str(Path(__file__).parent))

from wallhaven.app import main

if __name__ == "__main__":
    main()
