"""Main module for ragaman."""
import argparse
import logging

from ragaman.core.config import settings
from ragaman.mcp_server import run_mcp_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Run the main program with option to start API or MCP server."""
    parser = argparse.ArgumentParser(description="Ragaman - RAG system for notes")
    parser.add_argument(
        "--transport", 
        type=str, 
        choices=["stdio", "http"], 
        default="stdio",
        help="MCP transport method (only used when mode=mcp)"
    )
    
    args = parser.parse_args()
    run_mcp_server(transport=args.transport)


if __name__ == "__main__":
    main()
