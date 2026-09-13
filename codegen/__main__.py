import argparse

import dotenv

from codegen import download, generate


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m codegen")
    parser.add_argument("command", nargs="?", choices=["download", "generate", "all"], default="all")
    args = parser.parse_args()

    dotenv.load_dotenv(dotenv.find_dotenv(usecwd=True))

    if args.command in ("download", "all"):
        download.download_all()
    if args.command in ("generate", "all"):
        generate.generate_all()


if __name__ == "__main__":
    main()
