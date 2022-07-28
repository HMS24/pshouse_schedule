import logging

from real_.process import process_real_estate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)10.19s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def main():
    process_real_estate()


if __name__ == "__main__":
    main()
