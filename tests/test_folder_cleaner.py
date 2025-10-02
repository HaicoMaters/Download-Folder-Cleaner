"""
Test suite for Download Folder Cleaner.

This module contains comprehensive tests for the folder cleaning functionality,
including tests for file categorization, recursion handling, and edge cases.
"""

import pytest
import os
import sys
import shutil
from typing import Generator

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from folder_cleaner import create_directories, get_files, map_file_to_category, get_unique_filename, main
from change_logger_singleton import initialize_logger, get_logger

TEST_PATH = os.path.join(os.path.dirname(__file__), 'test_folder')
TEST_SUBFOLDER = os.path.join(TEST_PATH, 'subfolder')
TEST_SUB_SUBFOLDER = os.path.join(TEST_SUBFOLDER, 'sub_subfolder')

@pytest.fixture
def setup_paths() -> Generator[str, None, None]:
    """
    Test fixture that creates a temporary directory structure for testing.

    Creates:
        - Base test directory
        - Subfolder with test files
        - Sub-subfolder with test files
        - Various test files of different types

    Yields:
        Path to the test directory
    
    Cleanup:
        Removes all test directories and files after test completion
        Regardless of test outcome
    """
    # Create test directory if it doesn't exist
    os.makedirs(TEST_PATH, exist_ok=True)
    os.makedirs(TEST_SUBFOLDER, exist_ok=True)
    os.makedirs(TEST_SUB_SUBFOLDER, exist_ok=True)

    # Initialize logger for tests
    initialize_logger(TEST_PATH)

    # Create test files
    test_files = {
        'song.mp3': 'test audio',
        'video.mp4': 'test video',
        'document.pdf': 'test doc',
        'image.jpg': 'test image',
        'archive.zip': 'test archive',
        'installer.exe': 'test installer',
        'unknown.xyz': 'test unknown',
        '.hiddenfile': 'hidden'
    }

    for filename, content in test_files.items():
        with open(os.path.join(TEST_PATH, filename), 'w') as f:
            f.write(content)

    # Create a file in a subfolder to ensure it is ignored
    with open(os.path.join(TEST_SUBFOLDER, 'subfile.txt'), 'w') as f:
        f.write('subfolder file')

    # Create file in sub-subfolder to ensure it is ignored
    with open(os.path.join(TEST_SUB_SUBFOLDER, 'subsubfile.txt'), 'w') as f:
        f.write('sub-subfolder file')
    
    # Create file that will cause a duplicate
    os.makedirs(os.path.join(TEST_PATH, 'Audio'), exist_ok=True)
    with open(os.path.join(TEST_PATH, 'Audio', 'song.mp3'), 'w') as f:
        f.write('existing audio')

    yield TEST_PATH

    # Cleanup after tests
    if os.path.exists(TEST_PATH):
        shutil.rmtree(TEST_PATH)

    # Remove logs created
    logFile = get_logger().log_file
    if os.path.exists(logFile):
        os.remove(logFile)

#--------------------------------------- Tests for create_directories ----------------------------------------

def test_create_directories(setup_paths):
    """Test the creation of directory structure."""
    # setup_paths fixture will already have initialized the logger
    dirs = create_directories(setup_paths)
    for dir_name in ['Audio', 'Video', 'Documents', 'Images', 'Archives', 'Installers', 'Others']:
        assert os.path.exists(dirs[dir_name])

# --------------------------------------- Tests for get_files ----------------------------------------

def test_get_files(setup_paths):
    """Test retrieval of files from the directory."""

    files = get_files(setup_paths)
    expected_files = ['song.mp3', 'video.mp4', 'document.pdf', 'image.jpg', 'archive.zip', 
                      'installer.exe', 'unknown.xyz', '.hiddenfile']
    assert sorted(files) == sorted(expected_files)

# --------------------------------------- Tests for map_file_to_category ----------------------------------------

def test_map_file_to_category():
    """Test the mapping of files to their respective categories."""
    file_map = { 'Audio': [], 'Video': [], 'Documents': [], 'Images': [], 
                     'Archives': [], 'Installers': [], 'Others': [] }
        
    test_files = ['song.mp3', 'video.mp4', 'document.pdf', 'image.jpg', 
                      'archive.zip', 'installer.exe', 'unknown.xyz', '.hiddenfile']
        
    for file in test_files:
        map_file_to_category(file, file_map)
        
    assert file_map['Audio'] == ['song.mp3']
    assert file_map['Video'] == ['video.mp4']
    assert file_map['Documents'] == ['document.pdf']
    assert file_map['Images'] == ['image.jpg']
    assert file_map['Archives'] == ['archive.zip']
    assert file_map['Installers'] == ['installer.exe']
    assert file_map['Others'] == ['unknown.xyz']
    assert '.hiddenfile' not in sum(file_map.values(), [])

#--------------------------------------- Tests for get_unique_filename ----------------------------------------
def test_get_unique_filename_nonexistent():
    """Test getting a unique filename when the file does not exist."""
    test_file = os.path.join(TEST_PATH, 'newfile.txt')
    result = get_unique_filename(test_file)
    assert result == test_file

def test_get_unique_filename_existing(setup_paths):
    """Test getting a unique filename when a single duplicate exists."""
    # Create initial file
    test_file = os.path.join(setup_paths, 'duplicate.txt')
    with open(test_file, 'w') as f:
        f.write('original file')
    
    result = get_unique_filename(test_file)
    assert result == os.path.join(setup_paths, 'duplicate(1).txt')

def test_get_unique_filename_multiple_existing(setup_paths):
    """Test getting a unique filename when multiple duplicates exist."""
    # Create multiple duplicate files
    base_file = os.path.join(setup_paths, 'multiple.txt')
    with open(base_file, 'w') as f:
        f.write('original file')
    with open(os.path.join(setup_paths, 'multiple(1).txt'), 'w') as f:
        f.write('first duplicate')
    
    result = get_unique_filename(base_file)
    assert result == os.path.join(setup_paths, 'multiple(2).txt')

# --------------------------------------- Tests for main ----------------------------------------
def test_main_function(setup_paths):
    """Test the main folder cleaning function."""
    main(setup_paths)
    
    # Check if files are moved to correct directories
    assert os.path.exists(os.path.join(setup_paths, 'Audio', 'song.mp3'))
    assert os.path.exists(os.path.join(setup_paths, 'Video', 'video.mp4'))
    assert os.path.exists(os.path.join(setup_paths, 'Documents', 'document.pdf'))
    assert os.path.exists(os.path.join(setup_paths, 'Images', 'image.jpg'))
    assert os.path.exists(os.path.join(setup_paths, 'Archives', 'archive.zip'))
    assert os.path.exists(os.path.join(setup_paths, 'Installers', 'installer.exe'))
    assert os.path.exists(os.path.join(setup_paths, 'Others', 'unknown.xyz'))

    # Check that duplicate file was not overwritten
    assert os.path.exists(os.path.join(setup_paths, 'Audio', 'song(1).mp3'))

    # Check that hidden file remains in original location
    assert os.path.exists(os.path.join(setup_paths, '.hiddenfile'))

    # Check that subfolder file remains in original location
    assert os.path.exists(os.path.join(setup_paths, 'subfolder', 'subfile.txt'))
    
    # Ensure original files are removed from base path
    remaining_files = get_files(setup_paths)
    assert 'song.mp3' not in remaining_files
    assert 'video.mp4' not in remaining_files
    assert 'document.pdf' not in remaining_files
    assert 'image.jpg' not in remaining_files
    assert 'archive.zip' not in remaining_files
    assert 'installer.exe' not in remaining_files
    assert 'unknown.xyz' not in remaining_files
    
    assert '.hiddenfile' in remaining_files
    assert len(remaining_files) == 1  # Only the hidden file should remain
    assert len(os.listdir(os.path.join(setup_paths, 'Audio'))) == 2  # original + duplicate
    assert len(os.listdir(os.path.join(setup_paths, 'Video'))) == 1
    assert len(os.listdir(os.path.join(setup_paths, 'Documents'))) == 1
    assert len(os.listdir(os.path.join(setup_paths, 'Images'))) == 1
    assert len(os.listdir(os.path.join(setup_paths, 'Archives'))) == 1
    assert len(os.listdir(os.path.join(setup_paths, 'Installers'))) == 1
    assert len(os.listdir(os.path.join(setup_paths, 'Others'))) == 1
    assert len(os.listdir(os.path.join(setup_paths, 'subfolder'))) == 2  # subfolder file and sub_subfolder remains

# --------------------------------------- Tests for main with recursion ----------------------------------------
def test_main_function_recursive(setup_paths):
    """Test with infinite recursion (recursionDepth=-1)"""
    main(setup_paths, recursive=True, recursionDepth=-1)

    # Check base path files
    assert os.path.exists(os.path.join(setup_paths, 'Audio', 'song.mp3'))
    assert os.path.exists(os.path.join(setup_paths, 'Audio', 'song(1).mp3'))
    assert os.path.exists(os.path.join(setup_paths, '.hiddenfile'))

    # Check subfolder files are processed
    assert os.path.exists(os.path.join(setup_paths, 'subfolder', 'Documents', 'subfile.txt'))
    assert not os.path.exists(os.path.join(setup_paths, 'subfolder', 'subfile.txt'))

    # Check sub-subfolder files are processed (due to infinite recursion)
    assert os.path.exists(os.path.join(setup_paths, 'subfolder', 'sub_subfolder', 'Documents', 'subsubfile.txt'))
    assert not os.path.exists(os.path.join(setup_paths, 'subfolder', 'sub_subfolder', 'subsubfile.txt'))

def test_main_function_recursive_limited_depth(setup_paths):
    """Test with recursion depth of 1"""
    main(setup_paths, recursive=True, recursionDepth=1)

    # Check base path files
    assert os.path.exists(os.path.join(setup_paths, 'Audio', 'song.mp3'))
    assert os.path.exists(os.path.join(setup_paths, 'Audio', 'song(1).mp3'))
    assert os.path.exists(os.path.join(setup_paths, '.hiddenfile'))

    # Check first level subfolder files are processed
    assert os.path.exists(os.path.join(setup_paths, 'subfolder', 'Documents', 'subfile.txt'))
    assert not os.path.exists(os.path.join(setup_paths, 'subfolder', 'subfile.txt'))

    # Check sub-subfolder files are NOT processed (due to depth=1)
    assert os.path.exists(os.path.join(setup_paths, 'subfolder', 'sub_subfolder', 'subsubfile.txt'))
    assert not os.path.exists(os.path.join(setup_paths, 'subfolder', 'sub_subfolder', 'Documents', 'subsubfile.txt'))