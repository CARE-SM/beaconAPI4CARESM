FROM python:3.8 
WORKDIR /code
COPY . /code
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
CMD ["uvicorn", "--host", "0.0.0.0", "main:app"]