import sys
import logging

from real_.fetch import fetch_real_estate

logger = logging.getLogger()


def process_real_estate():
    year, season = sys.argv[1:3]
    real_estate = fetch_real_estate(year, season)
    # save
    # upload local or s3
    # load into database
    logger.info(f'process_real_estate, {real_estate.status_code}')
