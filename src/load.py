import pandas as pd
from vasaloppet.scraping import *
from vasaloppet import logger


wrapper = VasaloppetScraper()

# 1. get all urls for all pages for all years
pages = pd.DataFrame(columns=['year', 'page', 'url'])
for year in range(1922, 2025):
    urls = wrapper.GetPageUrls(year)
    for i, url in enumerate(urls):
        pages.loc[len(pages),:] = (year, i, url)
pages.to_csv('data/urls.csv', index=False)


# def load_task(url: str, i: int, n: int) -> None:
#     # load data
#     try:
#         result = dataProvider.LoadResult(url)
#         year = result.Race.Year
#     except Exception:
#         logger.error(f'something went wrong while loading {i}/{n}')
#         logger.error(traceback.print_exc())
#     else:
#         # dump data
#         try:
#             with open(f'data/vasaloppet_{year}.json', 'a', encoding='utf8') as outfile:
#                 json.dump(result.flatten(), outfile, ensure_ascii=False)
#                 outfile.write('\n')
#         except Exception as e:
#             logger.error(f'something went wrong while dumping {i}/{n}: {e}')
#             logger.info(f'{results}')
#         else:
#             logger.info(f'successfully processed {i}/{n}')


