import json
import requests
import os

#ToDo: implement it fully (look up for bugs and complete it, done for today)
def get_current_version():
    with open("iris.json", "r") as f:
        data = json.load(f)
        return data["version"]


def get_latest_release():
    github_url = "https://api.github.com/repos/sl3meyy/irisDiscordBot/releases/latest"
    response = requests.get(github_url)
    if response.status_code == 200:
        release_data = response.json()
        return release_data["tag_name"]
    else:
        return None


def download_update(tag_name):
    download_url = f"https://github.com/sl3meyy/irisDiscordBot/archive/{tag_name}.zip"
    response = requests.get(download_url)
    if response.status_code == 200:
        with open("update.zip", "wb") as f:
            f.write(response.content)
        # Extract the zip file and replace main.py as needed
        # Implement this part based on your requirements
    else:
        print("Failed to download update.")


def update_program():
    current_version = get_current_version()
    latest_release = get_latest_release()
    if current_version and latest_release:
        if updateToDevVersion:
            prefix = "d-"
        else:
            prefix = "p-"

        # Check if the latest release is greater than the current version
        if latest_release.startswith(prefix):
            latest_version = float(latest_release.split("-")[1])
            current_version = float(current_version)
            if latest_version > current_version:
                download_update(latest_release)
                # Optionally, update the version in iris.json
                # Implement this part based on your requirements
            else:
                print("No update available.")
        else:
            print("No suitable release found.")
    else:
        print("Failed to fetch version information.")


# Set this variable based on your requirement
updateToDevVersion = False
update_program()
def run():
    updateToDevVersion = False
    update_program()