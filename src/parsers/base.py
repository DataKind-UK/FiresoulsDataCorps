from typing import Dict, Any
import pandas as pd
from bs4 import BeautifulSoup
from src.downloader import downloadHTML, downloadZipFile


class BaseParser:
    @staticmethod
    def _make_soup(url: str, use_proxy: bool = True):
        html = downloadHTML(url, use_proxy)
        soup = BeautifulSoup(html, "html.parser")
        return soup

    @staticmethod
    def _download_excel_from_zip(url: str, fname: str, sheet_name: str, use_proxy: bool = False) -> pd.DataFrame:
        print(url)
        zipf = downloadZipFile(url, use_proxy=False)
        for n in zipf.namelist():
            if fname in n:
                data = zipf.open(n).read()
                break
        df = pd.read_excel(data, sheet_name='All')
        return df

    def parse(self) -> Dict[str, Any]:
        raise NotImplementedError(
            "This method needs to be implemented in child classes"
        )
