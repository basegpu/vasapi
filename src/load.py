from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import pandas as pd
from vasaloppet.scraping import *
from vasaloppet import logger


wrapper = VasaloppetScraper()

# 1. get all urls for all pages for all years
if os.path.exists('data/page_urls.csv'):
    pages = pd.read_csv('data/page_urls.csv')
else:
    pages = pd.DataFrame(columns=['year', 'page', 'url'])
    for year in range(1922, 2025):
        urls = wrapper.GetPageUrls(year)
        for i, url in enumerate(urls):
            pages.loc[len(pages),:] = (year, i, url)
    pages.to_csv('data/page_urls.csv', index=False)
print(f'found {len(pages)} page urls')

# 2. get all urls for all results
results = pd.DataFrame(columns=['year', 'page', 'row', 'url'])
try:
    start = -1#pages.index[(pages['year'] == 2025) & (pages['page'] == 1)][0]
    for _, page in pages[start::].iterrows():
        urls = wrapper.GetResultsFromTableUrl(page.url)
        for iRow, url in enumerate(urls):
            results.loc[len(results)] = [page.year, page.page, iRow+1, url]
        logger.info(f'recorded {len(results)} result urls until year {page.year} and page {page.page}')
except Exception as e:
    logger.error(e)
finally:
    if os.path.exists('data/result_urls.csv'):
        results_cache = pd.read_csv('data/result_urls.csv')
        results = pd.concat([results_cache, results], ignore_index=True)
    #results.to_csv('data/result_urls_new.csv', index=False)

print(f'found {len(results)} result urls')

# 3. get all results
nThreads = 16
if os.path.exists('data/results.csv'):
    data = pd.read_csv('data/results.csv', index_col=0, low_memory=False)
else:
    data = pd.DataFrame()
try:
    start = 0
    n = 750000
    with ThreadPoolExecutor(max_workers=nThreads) as executor:
        futures = {}
        for i, row in results[start:start+n].iterrows():
            h = hash((row.year, row.page, row.row))
            if h in data.index:
                continue
            logger.info(f'loading result {row.year},{row.page},{row.row} ({i}/{start+n})')
            futures[executor.submit(VasaloppetScraper.LoadResult, url=row.url)] = h
        data_new = []
        for future in as_completed(futures):
            result = future.result()
            entry = {'index': futures[future]}
            entry.update(result.flatten())
            data_new.append(entry)
            logger.info(f'loaded result {entry["index"]}: {result.Race.Year} {result.Lopper.Name} ({len(data_new)}/{len(futures)})')
except Exception as e:
    logger.error(e)
finally:
    if len(data_new) > 0:
        df_new = pd.DataFrame(data_new)
        df_new.set_index('index', inplace=True)
        data = pd.concat([data, df_new])
        # type conversion
        data.Time_Finish =  pd.to_timedelta(data.Time_Finish)
        data.Place_Finish = pd.to_numeric(data.Place_Finish, downcast='integer')
        data.to_csv('data/results.csv')
print(f'having {len(data)} results')
