FROM python:3.9.16-slim-buster
COPY ./src /api
RUN pip install fastapi uvicorn
WORKDIR ./api
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
