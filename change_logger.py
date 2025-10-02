"""Module for logging and reverting file movements."""

import json
import os
from datetime import datetime
from typing import Dict, List

class ChangeLogger:
    def __init__(self, base_path: str):
        self.changes: List[Dict[str, str]] = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        self.log_file = os.path.join(self.logs_dir, f"file_changes_{self.timestamp}.json")
        self.base_path = base_path

    def log_move(self, src: str, dst: str) -> None:
        """Log a file movement. (also covers for renames)"""
        self.changes.append({
            "Type": "move",
            "source": src,
            "destination": dst
        }) 

    def log_folder_creation(self, folder_path: str) -> None:
        """Log a folder creation."""
        self.changes.append({
            "Type": "folder_creation",
            "source": "",
            "destination": folder_path
        })

    def save_log(self) -> str:
        """
        Save changes to JSON file in the logs directory and return filename.
        
        Creates the logs directory if it doesn't exist.
        """
        os.makedirs(self.logs_dir, exist_ok=True)
        
        with open(self.log_file, 'w') as f:
            json.dump({
                "base_path": self.base_path,
                "timestamp": self.timestamp,
                "changes": self.changes
            }, f, indent=2)
        return self.log_file
