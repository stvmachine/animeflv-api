from animeflv import AnimeFLV
import pprint
import fire


def list_mega_links_by_anime(anime_name: str):
    api = AnimeFLV()
    pp = pprint.PrettyPrinter(indent=4)

    # Calculate number of episodes
    episodes = api.get_anime_info(anime_name).episodes
    num_episodes = 0 if episodes is None else len(episodes)
    result_t = []

    for episode_i in range(1, num_episodes):
        links = api.get_video_servers(anime_name, episode_i)
        mega_link = [e for e in links[0] if e["server"] == "mega"]
        pp.pprint(mega_link)
        if mega_link is not None and mega_link[0].get("url") is not None:
            result_t.__iadd__([mega_link[0].get("url")])

    pp.pprint(result_t)


if __name__ == "__main__":
    fire.Fire(
        dict(
            get_list=list_mega_links_by_anime,
        )
    )
