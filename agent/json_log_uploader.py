import requests
import json
import sys
import os

API_URL = "http://localhost:8000/logs"


def upload_json(
    file_path, level="info", source="file_upload", message="Uploaded from JSON file"
):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    try:
        with open(file_path, "r") as f:
            content = json.load(f)

        # If the file is a list of objects, upload each one
        if isinstance(content, list):
            print(f"Detected list of {len(content)} items. Uploading...")
            for i, item in enumerate(content):
                payload = {
                    "level": level,
                    "source": source,
                    "message": f"{message} (item {i + 1})",
                    "data": item,
                }
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    print(f" Successfully uploaded item {i + 1}")
                else:
                    print(f" Failed item {i + 1}: {response.text}")

        # If the file is a single object, upload it directly
        else:
            payload = {
                "level": level,
                "source": source,
                "message": message,
                "data": content,
            }
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                print("Successfully uploaded JSON object.")
            else:
                print(f"Failed to upload: {response.text}")

    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python json_uploader.py <path_to_json_file> [level] [source]")
        print("Example: python json_uploader.py my_data.json warning web_server")
    else:
        file = sys.argv[1]
        lvl = sys.argv[2] if len(sys.argv) > 2 else "info"
        src = sys.argv[3] if len(sys.argv) > 3 else "file_upload"

        upload_json(file, lvl, src)
