## Add to requirements
## selenium==4.1.3
## webdriver-manager

import time
import re


# selenium drivers: https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
# pip3 install selenium
# pip3 install webdriver-manager
# for custom firefox installation: link firefox to /usr/bin/firefox, example: ln -s /opt/firefox/firefox-bin /usr/bin/firefox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


def download_one(
    title: str,
    episode: int,
    url: str,
    output_path: str = ".",
):
    path = Path(output_path) / f"{title}-{episode}.mp4"
    print(f"Downloading {title} #{episode}")

    print("Opening Firefox (for later...)")
    options = Options()
    options.headless = True
    options.set_preference("browser.download.folderList", 2)  # custom location
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", "/tmp")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    print("Getting the URL")
    driver.get(url)

    elems = driver.find_elements(By.XPATH, "//a[@href]")
    video_url = ""
    for elem in elems:
        href = elem.get_attribute("href")

        # Expecting https://www.yourupload.com/download?file=XXXXXXXX
        if re.search("download\?file=", href):
            video_url = href
            break

    if video_url == "":
        print("Not Found video link. Exiting.")
        return

    print("Open secondary link for video")
    driver.get(video_url)
    time.sleep(3)

    print("Clicking the download button")
    driver.find_element(By.ID, "download").click()
