"""Script to revert changes made by the Download Folder Cleaner."""

import json
import os
import argparse
from typing import Dict, List

def revert_changes(log_file: str) -> None:
    """Revert changes from a log file."""
    with open(log_file, 'r') as f:
        data = json.load(f)

    changes: List[Dict[str, str]] = data["changes"]
    
    # Revert in reverse order to handle any potential cascading moves
    for change in reversed(changes):
        src = change["source"]
        dst = change["destination"]
        type = change.get("Type")

        if type == "folder_creation":
            # Remove the created folder if it's empty
            if os.path.exists(dst) and os.path.isdir(dst) and not os.listdir(dst):
                try:
                    os.rmdir(dst)
                    print(f"Removed empty folder: {dst}")
                except Exception as e:
                    print(f"Error removing folder {dst}: {e}")
            continue  # Skip to next change

        if type == "move" and os.path.exists(dst):
            try:
                # Ensure the original directory exists
                os.makedirs(os.path.dirname(src), exist_ok=True)
                os.rename(dst, src)
                print(f"Reverted: {dst} -> {src}")
            except Exception as e:
                print(f"Error reverting {dst}: {e}")
        else:
            print(f"Warning: File not found: {dst}")
        
    # Auto delete log file if reverted successfully
    try:
        os.remove(log_file)
        print(f"Log file {log_file} deleted after successful reversion.")
    except Exception as e:
        print(f"Error deleting log file {log_file}: {e}")
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Revert changes made by Download Folder Cleaner")
    parser.add_argument('log_file', type=str, help='Path to the change log file')
    args = parser.parse_args()

    revert_changes(args.log_file)
    print("Reversion complete!")
