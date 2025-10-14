# Code Copy MCP Server

A Model Context Protocol (MCP) server that enables code copy-paste operations between files with security controls and validation.

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

## Integration with Claude Desktop

Add to Claude Desktop configuration:

```json
{
  "mcpServers": {
    "code-copy": {
      "command": "uv",
      "args": ["run", "python", "/path/to/code-copy-mcp/mcp_server.py"]
    }
  }
}
```

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