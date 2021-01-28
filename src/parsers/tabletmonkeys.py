from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re
from src.parsers.base import BaseParser
from src.resources import Tablet
from typing import Union, List


class TabletMonkeysTablets(BaseParser):
    scrape_source = "tabletmonkeys.com"
    url = "https://tabletmonkeys.com/tablet-comparison/"

    def get_all_tablet_results(self):
        columns = [
            "Tablet",
            "Tablet Prices",
            "Size",
            "Resolution",
            "OS",
            "Weight(gram)",
            "Processor",
            "Cameras",
            "Batt. Life",
        ]
        tables = pd.read_html(self.url)
        dfs = []
        for i in range(len(tables)):
            try:
                df_aux = tables[i][1:]
                df_aux.columns = columns
                dfs.append(df_aux)
            except:
                pass

        df = pd.concat(dfs)
        df.reset_index(
            drop=True,
        )
        return df

    
    @staticmethod
    def _parse_brand(brand: str) -> Union[str, str]:
        tablet_brand = brand.split()[0]
        tablet_model = ' '.join(brand.split()[1:])
        return tablet_brand, tablet_model

    @staticmethod
    def _parse_price(price):
        price = re.search(r".(\d{1,4}[.]{0,1}\d{0,2})", price).group(1)
        price = float(price)
        return price


    def _scrape_source(self) -> str:
        return self.scrape_source


    def cast_tablets(self, df: pd.DataFrame):
        tablets = []
        for i, r in tqdm(df.iterrows(), total=len(df)):
            brand, model = self._parse_brand(r['Tablet'])
            processor = r['Processor']
            screen_size = r['Size']
            screen_resolution = r['Resolution']
            storage = None
            release_year = None
            price = self._parse_price(r['Tablet Prices'])
            currency = "USD$"
            scrape_source = self._scrape_source()
            scrape_url = self.url

            t = Tablet(
                brand,
                model,
                processor,
                screen_size,
                screen_resolution,
                storage,
                release_year,
                price,
                currency,
                scrape_source,
                scrape_url
                )
            tablets.append(t)
        return tablets

    def parse(self) -> List[Tablet]:
        tablets = []
        df_results = self.get_all_tablet_results()
        tablets = self.cast_tablets(df_results)

        return tablets
