import os
import shutil
import zipfile
import requests
import webbrowser

def get_latest_release(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    version = data["tag_name"]
    asset_url = data["assets"][0]["browser_download_url"]
    return version, asset_url

def download_and_unzip(url, repo):
    download_folder = "tools"
    zip_path = f"{download_folder}/{repo}.zip"
    extract_dir = f"{download_folder}/{repo}"
    if not os.path.exists(download_folder): os.mkdir(download_folder)
    if not os.path.exists(extract_dir): os.mkdir(extract_dir)
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, "wb") as f:
            shutil.copyfileobj(response.raw, f)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    os.remove(zip_path)

def download_Witchy():
    owner = "ividyon"
    repo = "WitchyBND"
    version, url = get_latest_release(owner, repo)
    download_and_unzip(url, repo)
    return version

def download_ME2():
    owner = "soulsmods"
    repo = "ModEngine2"
    version, url = get_latest_release(owner, repo)
    download_and_unzip(url, repo)
    version, url = get_latest_release("soulsmods", "ModEngine2")
    return version

def download_UXM():
    url = "https://www.nexusmods.com/eldenring/mods/1651?tab=files"
    webbrowser.open(url)

def open_url(): 
    git_url = "https://github.com/tfb-sv/ER-SFXRecolorTool.git"
    nexus_url = "https://www.nexusmods.com/eldenring/mods/6795"
    webbrowser.open(nexus_url)
