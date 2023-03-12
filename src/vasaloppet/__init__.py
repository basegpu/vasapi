import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)