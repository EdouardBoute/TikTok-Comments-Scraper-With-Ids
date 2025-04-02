# TOCSWIFT - TikTok Comment Scraper With Ids

Get all comments from tiktok videos. Operational in April 2025.

All comments and comments on comments are collected. If there's a difference between the number of comments displayed on TikTok and the number of comments collected, it's because these comments have disappeared from TikTok. Everything posted is collected.

The original project I forked is [here](https://github.com/RomySaputraSihananda/tiktok-comment-scrapper).

I forked it to fix bugs, readme and add features.

## Requirements

- **Python >= 3.11.4**
- **Requests >= 2.31.0**
- **loguru>=0.7.3**

## Installation

```sh
# Clonig Repository
git clone https://github.com/romysaputrasihananda/tiktok-comment-scrapper

# Change Directory
cd tiktok-comment-scrapper

# Install Requirement
pip install -r requirements.txt
```

## Example Usages

This scraper requires an id or a list of ids in a csv as input. As output, a json file per video will be created in a folder named 'output'. Two possibilities, then, to be written in the command prompt: 

```sh
python main.py --aweme_id=7475428421678419222
python main.py --file="C:\Documents\videos_id.csv"

```

## License

This project is licensed under the [MIT License](LICENSE).
