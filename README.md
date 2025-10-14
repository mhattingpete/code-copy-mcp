# Code Copy MCP Server

A Model Context Protocol (MCP) server that enables code copy-paste operations between files with security controls and validation.

## Table of Contents

- [Features](#features)
- [Tools](#tools)
- [Installation & Configuration](#installation--configuration)
  - [Prerequisites](#prerequisites)
  - [Quick Setup](#quick-setup)
- [MCP Client Integration](#mcp-client-integration)
  - [1. Claude Desktop](#1-claude-desktop)
  - [2. Cursor (AI Code Editor)](#2-cursor-ai-code-editor)
  - [3. Claude Code](#3-claude-code)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Security Configuration](#security-configuration)
  - [Troubleshooting](#troubleshooting)
- [Usage Examples](#usage-examples)
  - [Example 1: Copy function from one file to another](#example-1-copy-function-from-one-file-to-another)
  - [Example 2: Replace code with backup](#example-2-replace-code-with-backup)
  - [Example 3: Copy entire file](#example-3-copy-entire-file)
- [Security Features](#security-features)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Logging](#logging)

## Features

- **Line-by-line code copying**: Extract specific line ranges from source files
- **Precise pasting**: Insert code at exact line positions in target files  
- **Entire file operations**: Copy complete file contents
- **Search and replace**: Find and replace text patterns with backup support
- **File information**: Get metadata and statistics about files
- **Security controls**: Restrict operations to allowed directories
- **Backup creation**: Automatic backups before file modifications

## Tools

### copy_code
Copy code lines from a source file with optional line numbers.

```python
copy_code(
    source_file: str,
    start_line: int,
    end_line: Optional[int] = None,
    include_line_numbers: bool = False
) -> str
```

### paste_code
Paste code at a specific line number in a target file.

```python
paste_code(
    target_file: str,
    line_number: int,
    code: str,
    create_backup: bool = True
) -> str
```

### copy_entire_file
Copy the complete content of a source file.

```python
copy_entire_file(
    source_file: str,
    include_line_numbers: bool = False
) -> str
```

### search_and_replace
Search and replace text patterns in files.

```python
search_and_replace(
    target_file: str,
    search_pattern: str,
    replacement: str,
    case_sensitive: bool = True,
    replace_all: bool = True,
    create_backup: bool = True
) -> str
```

### get_file_info
Get detailed information about a file.

```python
get_file_info(file_path: str) -> str
```

## Installation

### Prerequisites
- Python 3.11 or higher
- UV package manager

### Setup

1. Clone or create the project:
```bash
cd /Users/map/Documents/Repos/code-copy-mcp
```

2. Install dependencies:
```bash
uv install
```

3. Configure allowed directories (optional):
```bash
cp .env.example .env
# Edit .env to set your ALLOWED_DIRECTORIES
```

## Usage

### Running the Server

```bash
uv run python mcp_server.py
```

### Development Mode

```bash
# Activate virtual environment first
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run server
python mcp_server.py
```

### Configuration

Create a `.env` file in the project root:

```env
# Comma-separated list of allowed directories
ALLOWED_DIRECTORIES=/Users/yourname,/Users/yourname/Documents,/Users/yourname/Projects
```

If not specified, defaults to:
- User's home directory
- Documents folder
- Desktop folder  
- Projects folder (if exists)

### Security Features

- Path validation prevents directory traversal attacks
- File permission checks ensure read/write access
- Automatic backup creation before modifications
- Restricted operation to configured directories only

## Example Workflow

1. **Copy code lines from a source file:**
   ```
   copy_code("/path/to/source.py", start_line=10, end_line=20)
   ```

2. **Paste the code into target file:**
   ```
   paste_code("/path/to/target.py", line_number=5, code=" copied_code_content ")
   ```

3. **Get file information:**
   ```
   get_file_info("/path/to/target.py")
   ```

## Installation & Configuration

### Prerequisites
- Python 3.11 or higher
- UV package manager (recommended) or pip
- One of the supported MCP clients

### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mhattingpete/code-copy-mcp.git
   cd code-copy-mcp
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   # Or without UV: pip install -e .
   ```

3. **Configure allowed directories (optional):**
   ```bash
   cp .env.example .env
   # Edit .env to set your ALLOWED_DIRECTORIES
   ```

## MCP Client Integration

### 1. Claude Desktop

Add to your Claude Desktop configuration file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "code-copy": {
      "command": "/full/path/to/uv",
      "args": ["--directory", "/full/path/to/code-copy-mcp", "run", "python", "mcp_server.py"],
      "env": {
        "ALLOWED_DIRECTORIES": "/Users/yourname,/Users/yourname/Documents,/Users/yourname/Projects"
      }
    }
  }
}
```

### 2. Cursor (AI Code Editor)

1. Open Cursor settings (`Cmd/Ctrl + ,`)
2. Navigate to `Extensions` → `MCP Servers`
3. Add new server:
   ```
   Name: Code Copy MCP
   Command: full/path/to/uv
   Arguments: --directory /full/path/to/code-copy-mcp run python mcp_server.py
   Environment Variables:
     ALLOWED_DIRECTORIES=/Users/yourname,/Users/yourname/Documents,/Users/yourname/Projects
   ```

### 3. Claude Code

1. Install the Claude Code
2. Add server configuration:
   ```bash
   claude mcp add-json code-copy '{"type":"stdio","command":"full/path/to/uv","args":["--directory", "/full/path/to/code-copy-mcp", "run", "python", "mcp_server.py"],"env": {"ALLOWED_DIRECTORIES": "/Users/yourname,/Users/yourname/Documents,/Users/yourname/Projects"}}'
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Comma-separated list of directories where file operations are allowed
# Examples for different operating systems:

# macOS/Linux:
ALLOWED_DIRECTORIES=/Users/yourname,/Users/yourname/Documents,/Users/yourname/Projects

# Windows:
ALLOWED_DIRECTORIES=C:\Users\YourName,C:\Users\YourName\Documents,C:\Users\YourName\Projects

# If not specified, defaults to:
# - User's home directory
# - Documents folder  
# - Desktop folder
# - Projects folder (if exists)
```

### Security Configuration

The server only allows operations within the specified directories for security reasons. 
Make sure to include all directories where you want to perform code copy-paste operations.

### Troubleshooting

**Common Issues:**

1. **"Module not found" errors:**
   ```bash
   # Ensure dependencies are installed
   uv install
   # Or with pip:
   pip install -e .
   ```

2. **Permission denied errors:**
   - Check that the allowed directories are correctly configured
   - Ensure the directories exist and are accessible

3. **MCP Server not appearing:**
   - Verify the command path is correct
   - Check the client's logs for error messages
   - Restart the MCP client after configuration changes

## Usage Examples

Once configured, you can use the tools within your MCP client:

### Example 1: Copy function from one file to another
```
User: Copy the function calculate_total from utils.py and paste it into main.py at line 50
```

The assistant will:
1. Use `get_file_info` to examine the files
2. Use `copy_code` with appropriate line numbers
3. Use `paste_code` at the specified location

### Example 2: Replace code with backup
```
User: Replace all occurrences of "old_method" with "new_method" in all Python files and create backups
```

The assistant will:
1. Use `search_and_replace` on each file
2. Verify changes with `get_file_info`
3. Report the modifications made

### Example 3: Copy entire file
```
User: Make a copy of template.py as new_template.py
```

The assistant will:
1. Use `copy_entire_file` to get the content
2. Use `paste_code` to create the new file

## Project Structure

```
code-copy-mcp/
├── mcp_server.py          # Main MCP server
├── tools/
│   ├── __init__.py        # Package init
│   ├── validation.py      # Security validation
│   └── copy_tools.py      # Copy-paste tools
├── .env.example           # Configuration template
├── pyproject.toml         # UV project configuration
└── README.md              # This file
```

## Dependencies

- fastmcp: MCP server framework
- pydantic: Data validation
- loguru: Structured logging
- python-dotenv: Environment file support

## Logging

Logs are written to `~/.code-copy-mcp/mcp_server.log` with:
- Rotation at 1MB
- 7-day retention
- DEBUG level logging for troubleshooting
