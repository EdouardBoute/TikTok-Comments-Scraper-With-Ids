import re
import os
import click
import json
import csv
import time
import os

from loguru import logger

from tiktokcomment import TiktokComment
from tiktokcomment.typing import Comments

__title__ = 'TikTok Comment Scraper With Ids'
__version__ = '1.0.0'

@click.command(
    help=__title__
)
@click.version_option(
    version=__version__,
    prog_name=__title__
)
@click.option(
    "--aweme_id",
    help='id video tiktok',
    callback=lambda _, __, value: match.group(0) if (value and (match := re.match(r"^\d+$", value))) else None
)
@click.option(
    "--file",
    default=None,
    help="File containing list of videos"
)
@click.option(
    "--sleep",
    default=0,
    type=int,
    help="Waiting time in seconds between each video (can be useful with --file)"
)

def main(aweme_id: str, file, sleep): 
    if file:
        with open(file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Ignore l'en-tête

            for row in reader:
                video_id = row[0]
                output_file = f"output/{video_id}.json"

                if os.path.exists(output_file):
                    logger.info(f"File {output_file} already exists, skipping...")
                    continue  # Passe à la vidéo suivante
                
                logger.info(f"Processing video: {video_id}...")
                process_video(video_id)
                
                if sleep > 0:
                    logger.info(f"Sleeping for {sleep} seconds before next video...")
                    time.sleep(sleep)  # Pause avant la prochaine vidéo

    elif aweme_id:
        process_video(aweme_id)
    else:
        raise ValueError("You must specify either --aweme_id or --file. The file must contain the list of ids in the first column.")



def process_video(aweme_id):
    try:
        logger.info(f"Start scraping comments for {aweme_id}")
        try:
            comments: Comments = TiktokComment()(aweme_id=aweme_id)
        except TypeError as e:
            logger.warning(f"Video {aweme_id} is unavailable or has no comments. Creating unknown JSON.")
            output_dir = "output/"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            unknown_path = f"{output_dir}{aweme_id}_unknown.json"
            with open(unknown_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
            logger.info(f"Created unknown JSON for {aweme_id} at {unknown_path}")
            return
        if comments is None or not comments.dict:
            logger.warning(f"No comments found for {aweme_id}. Creating unknown JSON.")
            output_dir = "output/"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            unknown_path = f"{output_dir}{aweme_id}_unknown.json"
            with open(unknown_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
            logger.info(f"Created unknown JSON for {aweme_id} at {unknown_path}")
            return
        output_dir = "output/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        final_path = f"{output_dir}{aweme_id}.json"
        with open(final_path, 'w', encoding='utf-8') as f:
            json.dump(comments.dict, f, ensure_ascii=False, indent=4)
        logger.info(f"Saved comments for {aweme_id} in {final_path}")
    except Exception as e:
        logger.error(f"Unexpected error processing {aweme_id}: {str(e)}")
        # Créer aussi un fichier unknown pour les autres types d'erreurs
        output_dir = "output/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        unknown_path = f"{output_dir}{aweme_id}_unknown.json"
        with open(unknown_path, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=4)
        logger.info(f"Created unknown JSON for {aweme_id} after error at {unknown_path}")

if(__name__ == '__main__'):
    main()