FROM python:3.10-slim-buster AS build

RUN mkdir /app
WORKDIR app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src/vasaloppet vasaloppet

FROM build AS test
RUN pip3 install pytest
COPY test/ test/
CMD pytest test/Test*.py -v --junitxml="output/testresults.xml"

FROM build AS runtime
COPY src/api api
COPY src/main.py .
CMD gunicorn -w 1 -b 0.0.0.0:$PORT "main:app"

FROM build AS load
COPY src/load.py .
CMD python load.py > data/out.log