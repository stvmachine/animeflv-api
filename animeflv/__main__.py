import pprint
import fire
import time
import requests
import shutil

from animeflv import AnimeFLV
from tqdm import tqdm
from pathlib import Path

# selenium drivers: https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
# pip3 install selenium
# pip3 install webdriver-manager
# for custom firefox installation: link firefox to /usr/bin/firefox, example: ln -s /opt/firefox/firefox-bin /usr/bin/firefox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

pp = pprint.PrettyPrinter(indent=4)


def get_episodes(anime_name: str, episode_begin, episode_end):
    api = AnimeFLV()

    # Calculate number of episodes
    episodes = (
        range(episode_begin, episode_end + 1)
        if episode_end is not None
        else api.get_anime_info(anime_name).num_episodes
    )
    return episodes


def get_mega_links(anime_name: str, episode_begin: int = 1, episode_end: int = 1):
    api = AnimeFLV()
    episodes = get_episodes(
        anime_name=anime_name, episode_begin=episode_begin, episode_end=episode_end
    )
    result = []

    for episode_i in episodes:
        pp.pprint(episode_i)
        links = api.get_video_servers(anime_name, episode_i)
        mega_link = [e[0] for e in links[0] if e["server"] == "mega"]
        if mega_link is not None and mega_link.get("url") is not None:
            pp.pprint(mega_link.get("url"))
            result.__iadd__(mega_link.get("url"))

    pp.pprint(result)
    return result


def get_all_links(anime_name: str, episode_begin: int = 1, episode_end: int = 1):
    api = AnimeFLV()
    episodes = get_episodes(
        anime_name=anime_name, episode_begin=episode_begin, episode_end=episode_end
    )
    result = {}

    for episode_i in episodes:
        servers = api.get_video_servers(anime_name, episode_i)
        result[episode_i] = servers

    pp.pprint(result)
    return result


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
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    print("Getting the URL")
    driver.get(url)

    print("Clicking the play button")
    play = driver.find_element(By.CSS_SELECTOR, "body")
    play.click()

    time.sleep(3)
    video_obj = driver.find_element(By.CSS_SELECTOR, "video.jw-video")
    video_url = video_obj.get_attribute("src")

    print("Found video link")
    print(video_url)
    driver.close()
    print("Downloading video")

    stream = requests.get(video_url, stream=True)
    total_size = int(stream.headers.get("content-length", 0))

    if path.exists():
        print(f"(!) Overwriting {path}")

    try:
        with path.open("wb") as f:
            with tqdm(
                total=total_size, unit="B", unit_scale=True, unit_divisor=1024
            ) as pbar:
                for chunk in stream.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
    except:
        path.unlink()
        raise

    return path


if __name__ == "__main__":
    fire.Fire(
        dict(
            get_mega_links=get_mega_links,
            get_all_links=get_all_links,
            download_one=download_one,
        )
    )
