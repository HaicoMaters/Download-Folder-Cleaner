# 📂 Download Folder Cleaner

A lightweight Python script that automatically organizes files in your **Downloads** folder (or any folder you specify) into logical categories.

##  Features

- **Automatic Categorization**: Sorts files by type into organized folders
- **Safe Operations**: Never overwrites existing files
- **Recursive Mode**: Option to clean subfolders
- **Configurable**: Specify custom folder paths and recursion depth
- **Hidden File Protection**: Preserves hidden files

##  Setup

1. Clone the repository
```bash
git clone https://github.com/HaicoMaters/Download-Folder-Cleaner.git
cd Download-Folder-Cleaner
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

##  Usage

### Basic Operation Cleaning Your Downloads Folder
```bash
python folder_cleaner.py
```

### Advanced Options
```bash
# Clean a specific folder
python folder_cleaner.py --path "path/to/your/folder"

# Clean folders recursively (infinite depth)
python folder_cleaner.py --recursive

# Clean with specific recursion depth
python folder_cleaner.py --recursive --depth 2  # Only process subdirectories up to 2 levels deep
python folder_cleaner.py --recursive --depth 0  # No recursion (same as without --recursive)
python folder_cleaner.py --recursive --depth -1 # Infinite recursion (default)
```

##  Testing

Run the test suite:
```bash
pytest tests/test_folder_cleaner.py -v
```

Tests cover:
- File categorization logic
- File movement operations
- Handling of duplicate files
- Path validation
- Recursive operations

##  Categories

Files are automatically sorted into these categories:

| Category    | Extensions |
|------------|------------|
| Audio      | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a` |
| Video      | `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm` |
| Documents  | `.pdf`, `.docx`, `.txt`, `.xlsx`, `.pptx`, `.odt`, `.rtf` |
| Images     | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.svg` |
| Archives   | `.zip`, `.rar`, `.tar`, `.gz`, `.7z` |
| Installers | `.exe`, `.msi`, `.dmg`, `.pkg` |
| Others     | Any unmatched extensions |


##  Notes

- Hidden files (starting with `.`) are preserved in their original location
- Files are never overwritten; duplicates are renamed automatically
- New category folders are created as needed
- Only processes files in the specified folder by default
- Logs for help with reverting accidental missuse of the tool are stored in `/logs`

## ⚠️ Important Safety Precautions

- **DO NOT** use on project directories or structured folders where file organization matters
- **Be extra careful** with recursive mode as it will reorganize all subdirectories
- **Avoid using** on:
  - Software development projects
  - Git repositories
  - Application folders
  - System directories
  - Photo albums with specific organization
- **Recommended uses**:
  - Downloads folder
  - Temporary file dumps
  - Unorganized media collections
  - Backup folders that need sorting

Always make sure you have backups of important files before running this tool.

##  Reverting Changes

To mitigate issues caused with accidental missuse of the tool it logs all file movements and folder creations to a JSON file that can be used to revert changes:

```bash
# Normal cleanup operation creates a log file
python folder_cleaner.py --path "your/folder"
# Output: Changes logged to: json file

# Revert changes using the log file
python revert_changes.py "Download-Folder-Cleaner/logs/thejsonfile"
```

**Note**: Keep the log files if you think you might need to revert changes later. File Changes logs are automatically deleted after reverting changes.
