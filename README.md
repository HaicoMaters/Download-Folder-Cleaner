# 📂 Download Folder Cleaner

A lightweight Python script that automatically organizes files in your **Downloads** folder (or any folder you specify and specifically within the root folder not any subfolders) into categories such as **Audio, Video, Documents, Images, Archives, Installers,** and **Others**.  

## Setup

1. Clone the repository
```bash
git clone https://github.com/HaicoMaters/Download_Folder_Cleaner.git
cd Download_Folder_Cleaner
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Clean your Downloads folder
```bash
python Folder_Cleaner.py
```

### Clean a specific folder
Provide the folder path as an argument:
```bash
python Folder_Cleaner.py --path "path/to/your/folder"
```
---

## Testing

Run the tests using pytest:
```bash
pytest Tests/Folder_Cleaner_Tests.py -v
```

The tests verify:
- File categorization logic
- File movement operations
- Handling of duplicate files
- Path validation

## Categories

Files are sorted into these categories based on their extensions:

- **Audio**: `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a`  
- **Video**: `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`, `.mpeg`  
- **Documents**: `.pdf`, `.docx`, `.txt`, `.xlsx`, `.pptx`, `.odt`, `.rtf`  
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.svg`  
- **Archives**: `.zip`, `.rar`, `.tar`, `.gz`, `.7z`  
- **Installers**: `.exe`, `.msi`, `.dmg`, `.pkg`  
- **Others**: Any file not in the above categories  

---

## Notes

- Hidden files (those starting with `.`) are ignored.   
-  New category folders are created automatically if they don’t already exist.  
-  If a file with the same name already exists in the destination folder, the script will automatically rename the file (e.g., `file.txt` → `file(1).txt`) to avoid overwriting.

---