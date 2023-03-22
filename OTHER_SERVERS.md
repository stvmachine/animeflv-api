
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
