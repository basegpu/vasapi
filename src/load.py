import json
import traceback
from multiprocessing import Pool
from vasaloppet.scraping import *
from vasaloppet import logger

config = [
    (2022, 10),
    #(2020, 0),
    #(2019, 0),
    #(2018, 0),
    #(2017, 0),
    #(2016, 0),
    #(2015, 0),
    #(2014, 0),
    #(2013, 0),
    #(2012, 0)
]

dataProvider = VasaloppetScraper()

def load_task(url: str, i: int, n: int) -> None:
    # load data
    try:
        result = dataProvider.LoadResult(url)
        year = result.Race.Year
    except Exception:
        logger.error(f'something went wrong while loading {i}/{n}')
        logger.error(traceback.print_exc())
    else:
        # dump data
        try:
            with open(f'data/vasaloppet_{year}.json', 'a', encoding='utf8') as outfile:
                json.dump(result.flatten(), outfile, ensure_ascii=False)
                outfile.write('\n')
        except Exception as e:
            logger.error(f'something went wrong while dumping {i}/{n}: {e}')
            logger.info(f'{results}')
        else:
            logger.info(f'successfully processed {i}/{n}')


urls = []
with Pool(len(config)) as pool:
    for u in pool.starmap(dataProvider.GetInitList, config):
        urls.extend(u)

with Pool(16) as pool:
    n = len(urls)
    items = [(u, i+1, n) for i,u in enumerate(urls)]
    pool.starmap(load_task, items)