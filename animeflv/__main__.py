import pprint
import fire

from animeflv import AnimeFLV

pp = pprint.PrettyPrinter(indent=4)


def _get_episodes(anime_name: str, episode_begin: int, episode_end: int):
    api = AnimeFLV()

    # Calculate number of episodes
    _episode_end = episode_end
    if _episode_end is None:
        _episode_end = api.get_anime_info(anime_name).num_episodes + 1

    episodes = range(episode_begin, _episode_end)
    return episodes


def get_all_links(
    anime_name: str,
    episode_begin: int = 1,
    episode_end: int = None,
    white_list_servers_off: bool = False,
):
    api = AnimeFLV()
    episodes = _get_episodes(
        anime_name=anime_name, episode_begin=episode_begin, episode_end=episode_end
    )
    white_list_servers = [
        "yu",  # YU yourupload
        "okru",  # Okru ok.ru
        # TODO: Maru adds double extension for some reason e.g. xx.mp4.mp4.
        # Not fixable through python
        # "maru",  # Maru my.mail.ru
        "stape",  # Streamtape
    ]
    result = {k: [] for k in episodes}

    for episode_i in episodes:
        servers = api.get_video_servers(anime_name, episode_i)

        if len(servers) != 0:
            for s in servers[0]:
                if white_list_servers_off or s["server"] in white_list_servers:
                    if not result[episode_i]:
                        result[episode_i] = []

                    result[episode_i].append(s)

    return result


if __name__ == "__main__":
    fire.Fire(
        dict(
            get_all_links=get_all_links,
        )
    )
