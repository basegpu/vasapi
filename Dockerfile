FROM python:3.10-slim-buster AS build

RUN mkdir /app
WORKDIR app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src/$APPNAME $APPNAME

CMD /bin/bash

FROM build AS test
RUN pip3 install pytest
COPY test/ test/
CMD pytest test/*test*.py -v --junitxml="output/testresults.xml"

FROM build AS runtime
COPY src/main.py .
CMD gunicorn -w 2 -b 0.0.0.0:$PORT "main:app"