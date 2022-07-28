import sys
import logging

from presale.process import process_actual_price_registration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)10.19s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def main():
    year, season = sys.argv[1:3]
    process_actual_price_registration(year, season)


if __name__ == "__main__":
    main()
