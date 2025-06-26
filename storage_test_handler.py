import runpod
import time
import os
from datetime import datetime

def handler(event):
    """
    Simple handler to test network storage by writing a text file to /runpod-volume
    """
    print("=== Storage Test Handler Started ===")
    
    input_data = event['input']
    message = input_data.get('message', 'Hello from RunPod!')
    filename = input_data.get('filename', 'test_file.txt')
    
    # Use /runpod-volume for network storage
    network_storage_path = "/runpod-volume"
    
    # Create a test directory
    test_dir = os.path.join(network_storage_path, "test_files")
    os.makedirs(test_dir, exist_ok=True)
    
    # Create the full file path
    file_path = os.path.join(test_dir, filename)
    
    # Write content to the file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"""
Storage Test File
================
Created at: {timestamp}
Message: {message}
Worker ID: {os.environ.get('RUNPOD_POD_ID', 'unknown')}

This file is stored in network storage at: {file_path}
Files written to /runpod-volume persist across worker restarts!
"""
    
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        
        # Get file info
        file_size = os.path.getsize(file_path)
        
        print(f"Successfully wrote file to network storage:")
        print(f"Path: {file_path}")
        print(f"Size: {file_size} bytes")
        
        # List all files in the test directory
        files_in_dir = os.listdir(test_dir)
        
        return {
            "status": "success",
            "message": f"File written to network storage",
            "file_path": file_path,
            "file_size": file_size,
            "files_in_directory": files_in_dir,
            "content": content
        }
        
    except Exception as e:
        print(f"Error writing file: {e}")
        return {
            "status": "error",
            "message": f"Failed to write file: {str(e)}"
        }

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler}) 