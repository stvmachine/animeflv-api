# AnimeFLV API

> AnimeFLV is a python custom API for [animeflv.net](https://animeflv.net) a Spanish anime content website.

## Installation

Install from source:

```bash
git clone https://github.com/stvmachine/animeflv-api
cd animeflv
git install -r requirements.txt
pip install .
```

## Usage

```python
# Check for all the links
python3 -m animeflv get_all_links "made-in-abyss"

# Looking for the first episode until the last episode emitted
python3 -m animeflv get_all_links "made-in-abyss" 10

# Looking for specific interval of episodes
python3 -m animeflv get_all_links "made-in-abyss" 10 12

# Looking to not whitelist servers 
python3 -m animeflv get_all_links "made-in-abyss" 1 25 True
```

## TODO

- [X] Group episodes and links
- [X] Added whitelist of servers
- [ ] Generate the output as a file in a format that JDownloader can use.

## License

[MIT](./LICENSE)

## Forked from <https://github.com/jorgeajimenezl/animeflv-api>
