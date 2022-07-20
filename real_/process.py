import sys
import logging
from pathlib import Path

from real_.fetch import fetch_real_estate

logger = logging.getLogger()


def process_real_estate():
    year, season = sys.argv[1:3]
    fetch_real_estate(year, season)
    # parse
    # upload local or s3
    # load into database
    logger.info(f'process_real_estate...')
