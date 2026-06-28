FROM python:3.13-slim

WORKDIR /lub

RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    python3-dev \
    gcc

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /lub/requirements.txt
RUN pip install -r /lub/requirements.txt

COPY ./alembic.ini /lub/alembic.ini
COPY ./app /lub/app

EXPOSE 8000

CMD [ "uvicorn", "app.main:create_app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--factory" ]