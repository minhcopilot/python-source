FROM python:3.9.16-slim-buster



COPY . /api

RUN pip3 install fastapi uvicorn

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]