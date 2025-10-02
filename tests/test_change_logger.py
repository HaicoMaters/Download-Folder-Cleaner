import os
import json
import shutil
import pytest
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from change_logger import ChangeLogger
from revert_changes import revert_changes

TEST_PATH = os.path.join(os.path.dirname(__file__), 'test_folder')

@pytest.fixture
def test_dir():
    """Create a temporary test directory."""
    os.makedirs(TEST_PATH, exist_ok=True)
    yield TEST_PATH
    if os.path.exists(TEST_PATH):
        shutil.rmtree(TEST_PATH)

@pytest.fixture
def logger(test_dir):
    """Create a ChangeLogger instance for testing."""
    return ChangeLogger(str(test_dir))

# ------------------------------ Test move logging ------------------------------

def test_log_move(logger, test_dir):
    """Test logging file movement."""
    src = os.path.join(test_dir, "source.txt")
    dst = os.path.join(test_dir, "dest.txt")
    logger.log_move(src, dst)
    assert len(logger.changes) == 1
    assert logger.changes[0]["Type"] == "move"
    assert logger.changes[0]["source"] == src
    assert logger.changes[0]["destination"] == dst

# ------------------------------ Test folder creation logging ------------------------------

def test_log_folder_creation(logger, test_dir):
    """Test logging folder creation."""
    folder_path = os.path.join(test_dir, "new_folder")
    logger.log_folder_creation(folder_path)
    assert len(logger.changes) == 1
    assert logger.changes[0]["Type"] == "folder_creation"
    assert logger.changes[0]["destination"] == folder_path

# ------------------------------ Test saving log ------------------------------

def test_save_log(logger, test_dir):
    """Test saving changes to log file."""
    src = os.path.join(test_dir, "source.txt")
    dst = os.path.join(test_dir, "dest.txt")
    logger.log_move(src, dst)
    
    log_file = logger.save_log()
    assert os.path.exists(log_file)
    
    with open(log_file, 'r') as f:
        data = json.load(f)
        assert "changes" in data
        assert len(data["changes"]) == 1
    
    # Cleanup
    os.remove(log_file)

# ------------------------------ Test reverting changes ------------------------------

def test_revert_changes(test_dir):
    """Test reverting file changes."""
    # Create test files and directories
    src = os.path.join(test_dir, "original.txt")
    dst_folder = os.path.join(test_dir, "category")
    dst = os.path.join(dst_folder, "original.txt")
    
    # Create initial file
    with open(src, 'w') as f:
        f.write("test content")
    
    # Create logger and log operations
    logger = ChangeLogger(test_dir)
    logger.log_folder_creation(dst_folder)
    logger.log_move(src, dst)
    
    # Perform actual file operations
    os.makedirs(dst_folder, exist_ok=True)
    shutil.move(src, dst)

    # Verify file operations occured correctly
    assert not os.path.exists(src)
    assert os.path.exists(dst_folder)
    assert os.path.exists(dst)
    with open(dst, 'r') as f:
        assert f.read() == "test content"

    # Save log and revert changes
    log_file = logger.save_log()
    revert_changes(log_file)
    
    # Verify reversion
    assert not os.path.exists(dst_folder)
    assert os.path.exists(src)
    with open(src, 'r') as f:
        assert f.read() == "test content"
