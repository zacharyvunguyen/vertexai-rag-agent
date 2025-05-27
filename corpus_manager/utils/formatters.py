"""
Formatting utilities for the RAG Corpus Manager.
Contains helper functions for formatting data for display.
"""

from datetime import datetime
from typing import Any


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    sizes = ["B", "KB", "MB", "GB", "TB"]
    size = size_bytes
    unit_index = 0
    
    while size >= 1024 and unit_index < len(sizes) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.1f} {sizes[unit_index]}"


def format_date(date_obj: Any) -> str:
    """Format datetime object to readable string."""
    if date_obj is None:
        return "Unknown"
    
    if hasattr(date_obj, 'strftime'):
        return date_obj.strftime("%Y-%m-%d %H:%M")
    else:
        return str(date_obj)


def format_document_name(name: str, max_length: int = 30) -> str:
    """Format document name for display, truncating if necessary."""
    if len(name) <= max_length:
        return name
    return name[:max_length] + "..."


def get_file_extension(filename: str) -> str:
    """Extract file extension from filename."""
    if '.' not in filename:
        return 'unknown'
    return filename.lower().split('.')[-1]


def format_resource_id(resource_name: str) -> str:
    """Extract and format the resource ID from full resource name."""
    return resource_name.split('/')[-1]


def format_percentage(value: float, total: float) -> str:
    """Format a percentage from value and total."""
    if total == 0:
        return "0%"
    return f"{(value / total * 100):.1f}%"


def pluralize(count: int, singular: str, plural: str = None) -> str:
    """Return singular or plural form based on count."""
    if plural is None:
        plural = singular + "s"
    return singular if count == 1 else plural


def format_count_with_label(count: int, label: str) -> str:
    """Format count with appropriate singular/plural label."""
    return f"{count} {pluralize(count, label)}" 