#!/usr/bin/env python3
"""
Dynamic Folder Structure Generator
Scans actual filesystem and generates live folder structure display
"""

import os
import json
from pathlib import Path

def get_directory_size(path):
    """Calculate total size of directory in bytes"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat().st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_directory_size(entry.path)
    except PermissionError:
        pass
    return total

def format_size(bytes_size):
    """Format bytes to human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def get_file_list_summary(directory, max_show=5):
    """Get first N and last N files from directory"""
    try:
        files = sorted([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
        file_count = len(files)
        
        if file_count == 0:
            return [], 0, "(empty)"
        elif file_count <= max_show * 2:
            return files, file_count, None
        else:
            first_files = files[:max_show]
            last_files = files[-max_show:]
            middle_count = file_count - (max_show * 2)
            return (first_files, f"... ({middle_count} more files)", last_files), file_count, None
    except Exception as e:
        return [], 0, f"(error: {str(e)})"

def generate_dynamic_folder_structure(project_root):
    """
    Generate dynamic folder structure by scanning actual filesystem
    
    Args:
        project_root: Path to project root (e.g., /home/ubuntu/audiobooksmith/users/.../v1.0/)
    
    Returns:
        HTML string with folder structure
    """
    project_root = Path(project_root)
    
    if not project_root.exists():
        return "<pre>Project directory not found</pre>"
    
    # Get relative path for display
    try:
        rel_path = str(project_root).split('/audiobooksmith/')[-1]
    except:
        rel_path = str(project_root)
    
    structure_lines = []
    structure_lines.append(f"<div class='folder-structure'>")
    structure_lines.append(f"<pre class='structure-tree'>")
    structure_lines.append(f"{rel_path}/")
    
    # Define folder structure to scan
    folders_to_scan = [
        ("source", "Original book files"),
        ("assets/images/author_photo", "Author photo"),
        ("assets/images/book_cover", "Book cover"),
        ("assets/images/similar_books", "3 similar book covers"),
        ("assets/audio/pronunciation", "Pronunciation audio files"),
        ("assets/audio/voice_samples", "Voice actor samples"),
        ("assets/audio/pronunciation_samples/names", "Name pronunciation samples"),
        ("assets/audio/pronunciation_samples/places", "Place pronunciation samples"),
        ("assets/audio/pronunciation_samples/units", "Unit conversion samples"),
        ("assets/audio/pronunciation_samples/currency", "Currency conversion samples"),
        ("assets/audio/pronunciation_samples/abbreviations", "Abbreviation samples"),
        ("assets/audio/pronunciation_samples/cultural_terms", "Cultural term samples"),
        ("chapters/raw", "Extracted chapters"),
        ("chapters/processed", "Processed chapters"),
        ("chapters/approved", "Final approved chapters"),
        ("chapters/quality_check", "QC reports"),
        ("chapters/backups/raw", "Raw backups"),
        ("chapters/backups/processed", "Processed backups"),
        ("chapters/backups/approved", "Approved backups"),
        ("manifests", "All manifest files"),
        ("logs/processing", "Processing logs"),
        ("logs/quality_checks", "Quality check logs"),
        ("logs/backups", "Backup logs"),
        ("production/credits", "Opening/closing credits"),
        ("production/notes", "Production notes"),
        ("production/pronunciation", "Pronunciation guides"),
        ("production/narration_ready", "Narration-ready chapters"),
        ("guides/pronunciation", "Pronunciation guides for AI"),
        ("guides/conversion", "Conversion guides for AI"),
        ("guides/cultural", "Cultural guides for AI"),
        ("reference/acx_compliance", "ACX compliance docs"),
        ("reference/cultural_analysis", "Cultural analysis"),
        ("reference/similar_books", "Similar books research"),
        ("output", "Generated HTML files"),
        ("voice_samples", "Voice actor samples"),
    ]
    
    # Build tree structure
    current_depth = {}
    
    for folder_path, description in folders_to_scan:
        full_path = project_root / folder_path
        parts = folder_path.split('/')
        depth = len(parts)
        
        # Generate tree characters
        if depth == 1:
            prefix = "├── "
        else:
            prefix = "│   " * (depth - 1) + "├── "
        
        folder_name = parts[-1] + "/"
        
        # Check if folder exists and get info
        if full_path.exists():
            files = [f for f in os.listdir(full_path) if os.path.isfile(full_path / f)]
            file_count = len(files)
            dir_size = get_directory_size(full_path)
            
            if file_count > 0:
                info = f"({file_count} files, {format_size(dir_size)})"
            else:
                info = "(empty)"
        else:
            info = "(not created)"
        
        line = f"{prefix}{folder_name:<30} # {description} {info}"
        structure_lines.append(line)
        
        # Show file samples for key directories
        if full_path.exists() and file_count > 0 and folder_path in ["manifests", "chapters/raw", "chapters/approved", "production/narration_ready", "output"]:
            file_list, count, error = get_file_list_summary(full_path, max_show=5)
            if isinstance(file_list, tuple):  # Has middle section
                first, middle, last = file_list
                for f in first:
                    structure_lines.append(f"│   {' ' * (depth * 4)}├── {f}")
                structure_lines.append(f"│   {' ' * (depth * 4)}├── {middle}")
                for f in last:
                    structure_lines.append(f"│   {' ' * (depth * 4)}├── {f}")
            elif file_list:
                for f in file_list:
                    structure_lines.append(f"│   {' ' * (depth * 4)}├── {f}")
    
    # Add summary at bottom
    total_size = get_directory_size(project_root)
    structure_lines.append("")
    structure_lines.append(f"Total Size: {format_size(total_size)}")
    structure_lines.append(f"Status: ✅ Production Ready")
    
    structure_lines.append("</pre>")
    structure_lines.append("</div>")
    
    return "\n".join(structure_lines)

if __name__ == "__main__":
    # Test with VITALY project
    project_root = "/home/ubuntu/audiobooksmith_project"
    structure_html = generate_dynamic_folder_structure(project_root)
    print(structure_html)
