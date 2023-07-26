FROM python:3.8 
RUN apt-get update && apt-get -y dist-upgrade
WORKDIR /code
COPY . /code
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
CMD ["uvicorn", "--host", "0.0.0.0", "main:app"]
