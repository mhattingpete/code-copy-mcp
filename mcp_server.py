"""Code Copy MCP Server - Enable code copy-paste operations between files."""

import os
from pathlib import Path
from typing import List

import dotenv
from fastmcp import FastMCP
from loguru import logger

# Load environment variables from .env file if it exists
if os.path.exists(".env"):
    dotenv.load_dotenv()

# Setup logging
log_file = Path.home() / ".code-copy-mcp" / "mcp_server.log"
log_file.parent.mkdir(exist_ok=True)
logger.add(
    log_file,
    rotation="1 MB",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
)

from tools.copy_tools import setup_copy_tools
from tools.validation import SecurityValidator


def create_mcp_server() -> FastMCP:
    """Create MCP server with code copy-paste tools."""

    # Get allowed directories from environment or use defaults
    allowed_dirs_env = os.getenv("ALLOWED_DIRECTORIES", "").split(",") if os.getenv("ALLOWED_DIRECTORIES") else None
    if not allowed_dirs_env:
        # Default to user's home directory and common project directories
        home_dir = Path.home()
        default_dirs = [
            str(home_dir),
            str(home_dir / "Documents"),
            str(home_dir / "Desktop"),
            str(home_dir / "Projects"),
        ]
        allowed_dirs = [d for d in default_dirs if Path(d).exists()]
    else:
        allowed_dirs = [d for d in allowed_dirs_env if d.strip()]
    
    logger.info(f"Allowed directories: {allowed_dirs}")
    
    # Initialize security validator
    validator = SecurityValidator(allowed_dirs)

    # Create server
    server = FastMCP(
        name="CodeCopyMCP",
        instructions="Code copy-paste server that enables copying code snippets from one file and pasting them into another. "
        "Supports line-by-line copying, entire file operations, search and replace, and file information. "
        "All operations are restricted to allowed directories for security. "
        f"Allowed directories: {', '.join(allowed_dirs)}",
    )

    # Setup copy-paste tools
    setup_copy_tools(server, validator)

    logger.info("MCP server created with 6 tools")
    return server


def main():
    """Main entry point for the MCP server."""
    logger.info("Starting Code Copy MCP server")
    mcp = create_mcp_server()
    mcp.run()


if __name__ == "__main__":
    main()
