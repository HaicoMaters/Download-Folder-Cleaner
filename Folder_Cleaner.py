"""
Download Folder Cleaner - A utility to organize files into categorized directories.

This module provides functionality to automatically sort files into appropriate
directories based on their file extensions. It can handle various file types
including audio, video, documents, images, archives, and installers.

Usage:
    python folder_cleaner.py [--path PATH] [--recursive] [recursionDepth]
"""

import argparse
import os
import sys
from typing import Dict, List, Optional
from change_logger_singleton import initialize_logger, get_logger


# maps of file extensions to categories
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'}
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mpeg'}
DOCUMENT_EXTENSIONS = {'.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.odt', '.rtf'}
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'}
ARCHIVE_EXTENSIONS = {'.zip', '.rar', '.tar', '.gz', '.7z'}
INSTALLER_EXTENSIONS = {'.exe', '.msi', '.dmg', '.pkg'}
# Everything else goes into 'Others'

download_path = os.path.join(os.path.expanduser("~"), "Downloads")

def create_directories(base_path: str) -> Dict[str, str]:
    """
    Create category directories if they don't exist.

    Args:
        base_path: The root path where directories should be created

    Returns:
        Dict mapping category names to their full directory paths
    """
    directories = {
        'Audio': os.path.join(base_path, 'Audio'),
        'Video': os.path.join(base_path, 'Video'),
        'Documents': os.path.join(base_path, 'Documents'),
        'Images': os.path.join(base_path, 'Images'),
        'Archives': os.path.join(base_path, 'Archives'),
        'Installers': os.path.join(base_path, 'Installers'),
        'Others': os.path.join(base_path, 'Others')
    }

    for dir_path in directories.values():
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            get_logger().log_folder_creation(dir_path)

    return directories

def get_files(base_path: str) -> List[str]:
    """
    Get list of files in the specified directory (excluding directories).

    Args:
        base_path: Directory path to scan for files

    Returns:
        List of filenames found in the directory
    """
    # skip folders and get a list of each file name in the base path (skipping any folders)
    return [file for file in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, file))]

def map_file_to_category(file: str, file_map: Dict[str, List[str]]) -> None:
    """
    Map a file to its appropriate category based on extension.

    Args:
        file: Name of the file to categorize
        file_map: Dictionary to store categorized files

    Note:
        Hidden files (starting with '.') are ignored
    """
    if (file.startswith('.')): # skip hidden files
        return
    
    ext = os.path.splitext(file)[1].lower()
    if ext in AUDIO_EXTENSIONS:
        file_map['Audio'].append(file)
    elif ext in VIDEO_EXTENSIONS:
        file_map['Video'].append(file)
    elif ext in DOCUMENT_EXTENSIONS:
        file_map['Documents'].append(file)
    elif ext in IMAGE_EXTENSIONS:
        file_map['Images'].append(file)
    elif ext in ARCHIVE_EXTENSIONS:
        file_map['Archives'].append(file)
    elif ext in INSTALLER_EXTENSIONS:
        file_map['Installers'].append(file)
    else:
        file_map['Others'].append(file)
    return

def get_unique_filename(dst: str) -> str:
    """
    Generate a unique filename by appending a number if file exists.

    Args:
        dst: Destination path to check

    Returns:
        Modified path that doesn't conflict with existing files
    """
    # if dst already exists, append a number to the filename
    # e.g., file.txt -> file(1).txt

    base, ext = os.path.splitext(dst)
    counter = 1
    new_dst = dst
    while os.path.exists(new_dst):
        new_dst = f"{base}({counter}){ext}"
        counter += 1
    return new_dst


def main(base_path: Optional[str] = None, recursive: bool = False, recursionDepth: int = -1) -> None:
    """
    Main function to organize files into categories.

    Args:
        base_path: Directory to organize (defaults to user's Downloads)
        recursive: Whether to process subdirectories
        recursionDepth: How deep to recurse (-1 for infinite)
    """
    if base_path is None:
        base_path = download_path
    
    if get_logger() is None:
        initialize_logger(base_path)

    directories = create_directories(base_path)  # create dirs
    files = get_files(base_path)

    file_map = {
        'Audio': [], 'Video': [], 'Documents': [],
        'Images': [], 'Archives': [], 'Installers': [], 'Others': []
    }

    # map files to categories
    for file in files:
        map_file_to_category(file, file_map)

    # move files
    for category, files in file_map.items():
        for file in files:
            src = os.path.join(base_path, file)
            dst = os.path.join(directories[category], file)
            dst = get_unique_filename(dst)  # ensure no overwriting
            try:
                os.rename(src, dst)
                get_logger().log_move(src, dst)
            except Exception as e:
                print(f"Error moving {file}: {e}")
    
    if recursive and (recursionDepth != 0):
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path) and not item.endswith(tuple(directories.keys())):
                main(item_path, recursive=True, recursionDepth = recursionDepth - 1)

    log_file = get_logger().save_log()
    print(f"Changes logged to: {log_file}")
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and organize your Downloads folder.")
    parser.add_argument('--path', type=str, help='Path to the folder to clean')
    parser.add_argument('--recursive', action='store_true', help='Clean subdirectories recursively')
    parser.add_argument('--depth', type=int, default=-1, 
                       help='Maximum recursion depth (-1 for infinite, 0 for no recursion, 1 for immediate subdirectories only)')
    args = parser.parse_args()
    initialize_logger(args.path if args.path else download_path)
    main(args.path, args.recursive, args.depth)
    print("Finished Cleaning!")
