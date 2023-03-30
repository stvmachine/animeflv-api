
# Potentially other servers

```python
   import re
   
   elems = driver.find_elements(By.XPATH, "//a[@href]")
    video_url = ""
    for elem in elems:
        href = elem.get_attribute("href")

        # Expecting https://www.yourupload.com/download?file=4007631
        if re.search("download\?file=", href):
            video_url = href
            break

    if video_url == "":
        print("Not Found video link. Exiting.")
        return
```

```python

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
```
