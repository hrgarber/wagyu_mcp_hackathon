#!/usr/bin/env python3
from typing import Dict, Any
import os
import re
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("file-analysis")

def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())

def count_lines(text: str) -> int:
    """Count lines in text."""
    return len(text.splitlines())

def find_patterns(text: str, pattern: str) -> list[str]:
    """Find all matches of a regex pattern in text."""
    try:
        regex = re.compile(pattern)
        return regex.findall(text)
    except re.error:
        return []

@mcp.tool()
async def analyze_file(file_path: str, pattern: str = None) -> str:
    """Analyze a file's content with optional pattern matching.
    
    Args:
        file_path: Path to the file to analyze
        pattern: Optional regex pattern to search for
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist"
        
        if not os.path.isfile(file_path):
            return f"Error: '{file_path}' is not a file"
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        analysis = []
        analysis.append(f"File: {os.path.basename(file_path)}")
        analysis.append(f"Size: {os.path.getsize(file_path)} bytes")
        analysis.append(f"Words: {count_words(content)}")
        analysis.append(f"Lines: {count_lines(content)}")
        
        if pattern:
            matches = find_patterns(content, pattern)
            if matches:
                analysis.append(f"\nPattern matches ({pattern}):")
                analysis.extend([f"- {match}" for match in matches[:10]])
                if len(matches) > 10:
                    analysis.append(f"... and {len(matches) - 10} more matches")
            else:
                analysis.append(f"\nNo matches found for pattern: {pattern}")
                
        return "\n".join(analysis)
        
    except Exception as e:
        return f"Error analyzing file: {str(e)}"

@mcp.tool()
async def list_files(directory: str) -> str:
    """List files in a directory with basic information.
    
    Args:
        directory: Path to directory to analyze
    """
    try:
        if not os.path.exists(directory):
            return f"Error: Directory '{directory}' does not exist"
            
        if not os.path.isdir(directory):
            return f"Error: '{directory}' is not a directory"
            
        files = []
        for entry in os.scandir(directory):
            if entry.is_file():
                size = entry.stat().st_size
                files.append(f"{entry.name} ({size} bytes)")
                
        if not files:
            return "No files found in directory"
            
        return "Files:\n" + "\n".join(f"- {f}" for f in sorted(files))
        
    except Exception as e:
        return f"Error listing files: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')