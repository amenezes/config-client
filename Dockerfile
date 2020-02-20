FROM python:3.6.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements-dev.txt

ENTRYPOINT ["python", "-m", "config"]
CMD ["-h"]
