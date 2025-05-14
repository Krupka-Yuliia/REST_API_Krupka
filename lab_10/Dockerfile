FROM python:3.10

WORKDIR /lab_10

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8089

CMD ["locust", "-f", "locustfile.py", "--host", "http://app10:5050"]

