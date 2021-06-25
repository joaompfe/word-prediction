import os
import gdown
import json
from subprocess import run


def download_data():
    file_urls_url = "https://drive.google.com/uc?id=12F-Fgo4pqXHGpuPe_ebRG1qCM6kx6ZUO"

    gdown.download(file_urls_url, "file_urls.json", quiet=False)

    f = open("file_urls.json")
    urls = json.load(f)

    data_url = urls["data"]
    gdown.download(data_url, "data.tar.gz", quiet=False)

    run(["tar", "-xvzf", "data.tar.gz"])
    os.remove("file_urls.json")
    os.remove("data.tar.gz")


def download_models():
    file_urls_url = "https://drive.google.com/uc?id=12F-Fgo4pqXHGpuPe_ebRG1qCM6kx6ZUO"

    gdown.download(file_urls_url, "file_urls.json", quiet=False)

    f = open("file_urls.json")
    urls = json.load(f)

    url = urls["models"]
    gdown.download(url, "models.tar.gz", quiet=False)

    run(["tar", "-xvzf", "models.tar.gz"])
    os.remove("file_urls.json")
    os.remove("models.tar.gz")
