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
git clone https://github.com/HaicoMaters/Download_Folder_Cleaner.git
cd Download_Folder_Cleaner
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

##  Usage

### Basic Operation Cleaning Your Downloads Folder
```bash
python Folder_Cleaner.py
```

### Advanced Options
```bash
# Clean a specific folder
python Folder_Cleaner.py --path "path/to/your/folder"

# Clean folders recursively (infinite depth)
python Folder_Cleaner.py --recursive

# Clean with specific recursion depth
python Folder_Cleaner.py --recursive --depth 2  # Only process subdirectories up to 2 levels deep
python Folder_Cleaner.py --recursive --depth 0  # No recursion (same as without --recursive)
python Folder_Cleaner.py --recursive --depth -1 # Infinite recursion (default)
```

##  Testing

Run the test suite:
```bash
pytest Tests/Folder_Cleaner_Tests.py -v
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
