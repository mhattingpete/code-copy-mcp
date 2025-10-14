"""Security and validation utilities for Code Copy MCP."""

import os
from pathlib import Path
from typing import List, Set


class SecurityValidator:
    def __init__(self, allowed_directories: List[str] = None):
        """Initialize security validator with allowed directories."""
        self.allowed_directories = set(allowed_directories or [str(Path.home())])
    
    def validate_path(self, file_path: str) -> bool:
        """Validate if file path is within allowed directories."""
        try:
            abs_path = Path(file_path).resolve()
            
            # Check if path is within allowed directories
            for allowed_dir in self.allowed_directories:
                allowed_abs = Path(allowed_dir).resolve()
                try:
                    abs_path.relative_to(allowed_abs)
                    return True
                except ValueError:
                    continue
            
            return False
        except (OSError, ValueError):
            return False
    
    def validate_file_exists(self, file_path: str) -> bool:
        """Check if file exists."""
        return Path(file_path).exists()
    
    def validate_file_readable(self, file_path: str) -> bool:
        """Check if file is readable."""
        return os.access(file_path, os.R_OK)
    
    def validate_directory_writable(self, file_path: str) -> bool:
        """Check if target directory is writable."""
        try:
            parent_dir = Path(file_path).parent
            return os.access(parent_dir, os.W_OK)
        except (OSError, ValueError):
            return False
    
    def get_safe_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        # Remove dangerous characters
        safe_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")
        return ''.join(c for c in filename if c in safe_chars)
