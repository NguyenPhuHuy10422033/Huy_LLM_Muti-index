#!/usr/bin/env python3
"""
Start script for Node 4 of the distributed vector store.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data.storage.vector_node_server import create_node_server

if __name__ == "__main__":
    print(" Starting Vector Node 4 on localhost:8004")
    server = create_node_server("node4", "localhost", 8004)
    server.run() 