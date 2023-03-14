from fastapi import FastAPI, HTTPException
import logging
from vasaloppet.models import ResultDetail, Sex
from vasaloppet.scraping import VasaloppetScraper

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title='Vasaloppet Results API',
    description='return results data from vasaloppet races, gathered from web scraping <a href=https://results.vasaloppet.se/>official site</a>.',
    version='2023',
    docs_url="/"
)

data_provider = VasaloppetScraper()
logging.info('Successfully initialized vasaloppet scraping instance.')

@app.get('/result/{year}/{sex}/{place}')
async def get_result(
    year: int,
    sex: str,
    place: int
) -> ResultDetail:
    try:
        logging.info('GET: result data for year %i, sex %s, and place %i'%(year, sex, place))
        result = data_provider.GetResult(year, Sex[sex.upper()], place)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
    return result