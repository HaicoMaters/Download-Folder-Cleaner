import pytest
import os
import sys
import shutil

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Folder_Cleaner

test_path = os.path.join(os.path.dirname(__file__), 'test_folder')
test_subfolder = os.path.join(test_path, 'subfolder')

@pytest.fixture
def setup_paths():
    # Create test directory if it doesn't exist
    os.makedirs(test_path, exist_ok=True)
    os.makedirs(test_subfolder, exist_ok=True)

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
        with open(os.path.join(test_path, filename), 'w') as f:
            f.write(content)

    # Create a file in a subfolder to ensure it is ignored
    with open(os.path.join(test_subfolder, 'subfile.txt'), 'w') as f:
        f.write('subfolder file')
    
    # Create file that will cause a duplicate
    os.makedirs(os.path.join(test_path, 'Audio'), exist_ok=True)
    with open(os.path.join(test_path, 'Audio', 'song.mp3'), 'w') as f:
        f.write('existing audio')

    yield test_path

    # Cleanup after tests
    if os.path.exists(test_path):
        shutil.rmtree(test_path)

#--------------------------------------- Tests for create_directories ----------------------------------------

def test_create_directories(setup_paths):
    dirs = Folder_Cleaner.create_directories(setup_paths)
    for dir_name in ['Audio', 'Video', 'Documents', 'Images', 'Archives', 'Installers', 'Others']:
        assert os.path.exists(dirs[dir_name])

# --------------------------------------- Tests for get_files ----------------------------------------

def test_get_files(setup_paths):

    files = Folder_Cleaner.get_files(setup_paths)
    expected_files = ['song.mp3', 'video.mp4', 'document.pdf', 'image.jpg', 'archive.zip', 
                      'installer.exe', 'unknown.xyz', '.hiddenfile']
    assert sorted(files) == sorted(expected_files)

# --------------------------------------- Tests for map_file_to_category ----------------------------------------

def test_map_file_to_category():
    file_map = { 'Audio': [], 'Video': [], 'Documents': [], 'Images': [], 
                     'Archives': [], 'Installers': [], 'Others': [] }
        
    test_files = ['song.mp3', 'video.mp4', 'document.pdf', 'image.jpg', 
                      'archive.zip', 'installer.exe', 'unknown.xyz', '.hiddenfile']
        
    for file in test_files:
        Folder_Cleaner.map_file_to_category(file, file_map)
        
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
    test_file = os.path.join(test_path, 'newfile.txt')
    result = Folder_Cleaner.get_unique_filename(test_file)
    assert result == test_file

def test_get_unique_filename_existing(setup_paths):
    # Create initial file
    test_file = os.path.join(setup_paths, 'duplicate.txt')
    with open(test_file, 'w') as f:
        f.write('original file')
    
    result = Folder_Cleaner.get_unique_filename(test_file)
    assert result == os.path.join(setup_paths, 'duplicate(1).txt')

def test_get_unique_filename_multiple_existing(setup_paths):
    # Create multiple duplicate files
    base_file = os.path.join(setup_paths, 'multiple.txt')
    with open(base_file, 'w') as f:
        f.write('original file')
    with open(os.path.join(setup_paths, 'multiple(1).txt'), 'w') as f:
        f.write('first duplicate')
    
    result = Folder_Cleaner.get_unique_filename(base_file)
    assert result == os.path.join(setup_paths, 'multiple(2).txt')

# --------------------------------------- Tests for main ----------------------------------------
def test_main_function(setup_paths):
    Folder_Cleaner.main(setup_paths)
    
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
    remaining_files = Folder_Cleaner.get_files(setup_paths)
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
    assert len(os.listdir(os.path.join(setup_paths, 'subfolder'))) == 1  # subfolder file remains
