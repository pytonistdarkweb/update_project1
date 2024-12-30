FROM python:3.12-slim


RUN apt-get update && apt-get install -y curl build-essential && apt-get clean


RUN curl -sSL https://install.python-poetry.org | python3 -


ENV PATH="/root/.local/bin:$PATH"


RUN echo $PATH && poetry --version


WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root


COPY . /app

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]