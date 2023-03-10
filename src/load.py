import json
import logging
import sys
import traceback
from vasaloppet.scraping import *
from vasaloppet.schemas import *

root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

dataProvider = VasaloppetScraper()

year = 2022
n = 0

for i,c in enumerate(dataProvider.GetInitList(year, n)):
    # load data
    try:
        result = c()
    except Exception:
        logging.error(f'something went wrong while loading {i}/{n}')
        logging.error(traceback.print_exc())
    else:
        # dump data
        try:
            data = ResultSchema().dump(result)
            with open(f'data/vasaloppet.json', 'a', encoding='utf8') as outfile:
                json.dump(data, outfile, ensure_ascii=False)
                outfile.write('\n')
        except Exception as e:
            logging.error(f'something went wrong while dumping {i}/{n}: {e}')
            logging.debug(f'{result}')
        else:
            logging.info(f'successfully processed {i}/{n}')
    
