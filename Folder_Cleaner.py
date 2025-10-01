import argparse
import os
import sys

# maps of file extensions to categories
Audio_Extensions = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'}
Video_Extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mpeg'}
Document_Extensions = {'.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.odt', '.rtf'}
Image_Extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'}
Archive_Extensions = {'.zip', '.rar', '.tar', '.gz', '.7z'}
Installer_Extensions = {'.exe', '.msi', '.dmg', '.pkg'}
# Everything else goes into 'Others'

download_path = os.path.join(os.path.expanduser("~"), "Downloads")

def create_directories(base_path):
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
        os.makedirs(dir_path, exist_ok=True)

    return directories

def get_files(base_path):
    # skip folders and get a list of each file name in the base path (skipping any folders)
    return [file for file in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, file))]

def map_file_to_category(file, file_map):
    if (file.startswith('.')): # skip hidden files
        return
    
    ext = os.path.splitext(file)[1].lower()
    if ext in Audio_Extensions:
        file_map['Audio'].append(file)
    elif ext in Video_Extensions:
        file_map['Video'].append(file)
    elif ext in Document_Extensions:
        file_map['Documents'].append(file)
    elif ext in Image_Extensions:
        file_map['Images'].append(file)
    elif ext in Archive_Extensions:
        file_map['Archives'].append(file)
    elif ext in Installer_Extensions:
        file_map['Installers'].append(file)
    else:
        file_map['Others'].append(file)
    return

def get_unique_filename(dst):
    # if dst already exists, append a number to the filename
    # e.g., file.txt -> file(1).txt

    base, ext = os.path.splitext(dst)
    counter = 1
    new_dst = dst
    while os.path.exists(new_dst):
        new_dst = f"{base}({counter}){ext}"
        counter += 1
    return new_dst


def main(base_path=None):
    if base_path is None:
        base_path = download_path

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
            except Exception as e:
                print(f"Error moving {file}: {e}")

    print("Finished Cleaning!")
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and organize your Downloads folder.")
    parser.add_argument('--path', type=str, help='Path to the folder to clean.')
    args = parser.parse_args()

    main(args.path)