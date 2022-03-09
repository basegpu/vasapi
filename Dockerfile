FROM python:3.6.5
RUN pip3 install requests beautifulsoup4
ADD main.py .
CMD [ "python", "./main.py" ]