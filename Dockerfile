FROM python:3.8 
WORKDIR /code
COPY . /code
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
ENV TRIPLESTORE_URL https://graphdb.ejprd.semlab-leiden.nl/repositories/unifiedCDE_model
ENV TRIPLESTORE_USERNAME pabloa
ENV TRIPLESTORE_PASSWORD ejprdejprd
CMD ["uvicorn", "--host", "0.0.0.0", "main:app"]