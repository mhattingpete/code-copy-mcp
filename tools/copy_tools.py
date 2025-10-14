"""Main copy-paste tools for Code Copy MCP."""

import shutil
from pathlib import Path
from typing import Optional, Tuple

from fastmcp import FastMCP

from .validation import SecurityValidator


def setup_copy_tools(mcp: FastMCP, validator: SecurityValidator):
    """Setup all copy-paste tools for the MCP server."""
    
    @mcp.tool()
    def copy_code(
        source_file: str,
        start_line: int,
        end_line: Optional[int] = None,
        include_line_numbers: bool = False
    ) -> str:
        """Copy code lines from source file.
        
        Args:
            source_file: Path to source file
            start_line: Starting line number (1-based)
            end_line: Ending line number (1-based), defaults to start_line
            include_line_numbers: Whether to include line numbers in output
            
        Returns:
            Copied code content as string
        """
        if not validator.validate_path(source_file):
            return f"ERROR: Source file '{source_file}' is not in allowed directory"
        
        if not validator.validate_file_exists(source_file):
            return f"ERROR: Source file '{source_file}' does not exist"
        
        if not validator.validate_file_readable(source_file):
            return f"ERROR: Cannot read source file '{source_file}'"
        
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
            
            if end_line is None:
                end_line = start_line
            
            # Validate line numbers
            if start_line < 1 or end_line > len(all_lines) or start_line > end_line:
                return f"ERROR: Invalid line range {start_line}-{end_line} for file with {len(all_lines)} lines"
            
            selected_lines = all_lines[start_line - 1:end_line]
            
            if include_line_numbers:
                code_content = ''.join(
                    f"{start_line + i:4d}: {line}" 
                    for i, line in enumerate(selected_lines)
                )
            else:
                code_content = ''.join(selected_lines)
            
            return f"Successfully copied {len(selected_lines)} lines from {source_file}:\n\n{code_content}"
            
        except Exception as e:
            return f"ERROR copying from {source_file}: {str(e)}"
    
    @mcp.tool()
    def paste_code(
        target_file: str,
        line_number: int,
        code: str,
        create_backup: bool = True
    ) -> str:
        """Paste code at specific line in target file.
        
        Args:
            target_file: Path to target file
            line_number: Line number to paste at (1-based, inserts before this line)
            code: Code content to paste
            create_backup: Whether to create backup file before modification
            
        Returns:
            Success message with details
        """
        if not validator.validate_path(target_file):
            return f"ERROR: Target file '{target_file}' is not in allowed directory"
        
        if not validator.validate_directory_writable(target_file):
            return f"ERROR: Cannot write to target directory for '{target_file}'"
        
        try:
            # Read existing content
            if validator.validate_file_exists(target_file):
                with open(target_file, 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()
            else:
                # Create new file
                all_lines = []
            
            # Validate line number
            if line_number < 1 or line_number > len(all_lines) + 1:
                return f"ERROR: Line number {line_number} is out of range for file with {len(all_lines)} lines"
            
            # Create backup if requested and file exists
            if create_backup and validator.validate_file_exists(target_file):
                backup_path = f"{target_file}.backup"
                shutil.copy2(target_file, backup_path)
            
            # Insert code at specified position
            # Split code into lines if it's a block
            code_lines = code.splitlines(keepends=True)
            if not code_lines[-1].endswith('\n'):
                code_lines[-1] += '\n'
            
            # Insert code
            target_idx = line_number - 1  # Convert to 0-based
            all_lines[target_idx:target_idx] = code_lines
            
            # Write back to file
            with open(target_file, 'w', encoding='utf-8') as f:
                f.writelines(all_lines)
            
            action = "updated" if validator.validate_file_exists(target_file) else "created"
            backup_msg = f" (backup saved to {backup_path})" if create_backup and validator.validate_file_exists(target_file) else ""
            
            return f"Successfully {action} {target_file} by inserting code at line {line_number}{backup_msg}"
            
        except Exception as e:
            return f"ERROR pasting to {target_file}: {str(e)}"
    
    @mcp.tool()
    def copy_entire_file(source_file: str, include_line_numbers: bool = False) -> str:
        """Copy entire content of source file.
        
        Args:
            source_file: Path to source file
            include_line_numbers: Whether to include line numbers
            
        Returns:
            Full file content as string
        """
        if not validator.validate_path(source_file):
            return f"ERROR: Source file '{source_file}' is not in allowed directory"
        
        if not validator.validate_file_exists(source_file):
            return f"ERROR: Source file '{source_file}' does not exist"
        
        if not validator.validate_file_readable(source_file):
            return f"ERROR: Cannot read source file '{source_file}'"
        
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if include_line_numbers:
                lines = content.splitlines(keepends=True)
                content = ''.join(f"{i+1:4d}: {line}" for i, line in enumerate(lines))
            
            return f"Successfully copied entire file {source_file}:\n\n{content}"
            
        except Exception as e:
            return f"ERROR copying file {source_file}: {str(e)}"
    
    @mcp.tool()
    def search_and_replace(
        target_file: str,
        search_pattern: str,
        replacement: str,
        case_sensitive: bool = True,
        replace_all: bool = True,
        create_backup: bool = True
    ) -> str:
        """Search and replace text in target file.
        
        Args:
            target_file: Path to target file
            search_pattern: Text to search for
            replacement: Replacement text
            case_sensitive: Whether search is case sensitive
            replace_all: Whether to replace all occurrences or just first
            create_backup: Whether to create backup file
            
        Returns:
            Success message with replacement count
        """
        if not validator.validate_path(target_file):
            return f"ERROR: Target file '{target_file}' is not in allowed directory"
        
        if not validator.validate_file_exists(target_file):
            return f"ERROR: Target file '{target_file}' does not exist"
        
        if not validator.validate_file_readable(target_file):
            return f"ERROR: Cannot read target file '{target_file}'"
        
        if not validator.validate_directory_writable(target_file):
            return f"ERROR: Cannot write to target directory for '{target_file}'"
        
        try:
            # Create backup
            if create_backup:
                backup_path = f"{target_file}.backup"
                shutil.copy2(target_file, backup_path)
            
            # Read file
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Perform replacement
            import re
            if case_sensitive:
                pattern = re.escape(search_pattern)
                matched_count = len(re.findall(pattern, content))
                if replace_all:
                    new_content = re.sub(pattern, replacement, content)
                else:
                    new_content = re.sub(pattern, replacement, content, count=1)
            else:
                pattern = re.escape(search_pattern)
                matched_count = len(re.findall(pattern, content, re.IGNORECASE))
                if replace_all:
                    new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                else:
                    new_content = re.sub(pattern, replacement, content, count=1, flags=re.IGNORECASE)
            
            # Write back
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            occurences = "occurrence" if matched_count == 1 else "occurrences"
            backup_msg = f" (backup saved to {backup_path})" if create_backup else ""
            
            return f"Successfully replaced {matched_count} {occurences} in {target_file}{backup_msg}"
            
        except Exception as e:
            return f"ERROR in search and replace in {target_file}: {str(e)}"
    
    @mcp.tool()
    def get_file_info(file_path: str) -> str:
        """Get basic information about a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            File information as string
        """
        if not validator.validate_path(file_path):
            return f"ERROR: File '{file_path}' is not in allowed directory"
        
        if not validator.validate_file_exists(file_path):
            return f"ERROR: File '{file_path}' does not exist"
        
        try:
            path = Path(file_path)
            stat = path.stat()
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            info = f"""File Information for {file_path}:
  Size: {stat.st_size} bytes
  Lines: {len(lines)}
  Modified: {stat.st_mtime}
  Type: {path.suffix if path.suffix else 'Unknown'}
  Readable: {validator.validate_file_readable(file_path)}
  Directory Writable: {validator.validate_directory_writable(file_path)}
"""
            return info
            
        except Exception as e:
            return f"ERROR getting file info for {file_path}: {str(e)}"
