FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.2.2
ENV HNSWLIB_NO_NATIVE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl build-essential\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure Poetry is in the PATH
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY . /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
