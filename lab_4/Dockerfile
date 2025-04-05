FROM python:3.9

WORKDIR /lab_4

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5050
CMD ["python3", "main.py"]

