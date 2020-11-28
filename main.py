import typer
from src.downloader import downloadHTML


def main(url: str):
    html = downloadHTML(url)
    print(html)


if __name__ == "__main__":
    typer.run(main)
